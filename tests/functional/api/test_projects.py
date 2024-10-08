import time
import uuid

import pytest

import gitlab
from gitlab.const import AccessLevel
from gitlab.v4.objects.projects import ProjectStorage


def test_projects_head(gl):
    headers = gl.projects.head()
    assert headers["x-total"]


def test_project_head(gl, project):
    headers = gl.projects.head(project.id)
    assert headers["content-type"] == "application/json"


def test_create_project(gl, user):
    # Moved from group tests chunk in legacy tests, TODO cleanup
    admin_project = gl.projects.create({"name": "admin_project"})
    assert isinstance(admin_project, gitlab.v4.objects.Project)
    assert admin_project in gl.projects.list(search="admin_project")

    sudo_project = gl.projects.create({"name": "sudo_project"}, sudo=user.id)

    created = gl.projects.list()
    created_gen = gl.projects.list(iterator=True)
    owned = gl.projects.list(owned=True)

    assert admin_project in created and sudo_project in created
    assert admin_project in owned and sudo_project not in owned
    assert len(created) == len(list(created_gen))

    admin_project.delete()
    sudo_project.delete()


def test_project_members(user, project):
    member = project.members.create(
        {"user_id": user.id, "access_level": AccessLevel.DEVELOPER}
    )
    assert member in project.members.list()
    assert member.access_level == 30

    member.delete()


def test_project_badges(project):
    badge_image = "http://example.com"
    badge_link = "http://example/img.svg"

    badge = project.badges.create({"link_url": badge_link, "image_url": badge_image})
    assert badge in project.badges.list()

    badge.image_url = "http://another.example.com"
    badge.save()

    badge = project.badges.get(badge.id)
    assert badge.image_url == "http://another.example.com"

    badge.delete()


@pytest.mark.skip(reason="Commented out in legacy test")
def test_project_boards(project):
    boards = project.boards.list()
    assert boards

    board = boards[0]
    lists = board.lists.list()

    last_list = lists[-1]
    last_list.position = 0
    last_list.save()

    last_list.delete()


def test_project_custom_attributes(gl, project):
    attrs = project.customattributes.list()
    assert not attrs

    attr = project.customattributes.set("key", "value1")
    assert attr.key == "key"
    assert attr.value == "value1"
    assert attr in project.customattributes.list()
    assert project in gl.projects.list(custom_attributes={"key": "value1"})

    attr = project.customattributes.set("key", "value2")
    attr = project.customattributes.get("key")
    assert attr.value == "value2"
    assert attr in project.customattributes.list()

    attr.delete()


def test_project_environments(project):
    environment = project.environments.create(
        {"name": "env1", "external_url": "http://fake.env/whatever"}
    )
    environments = project.environments.list()
    assert environment in environments

    environment = environments[0]
    environment.external_url = "http://new.env/whatever"
    environment.save()

    environment = project.environments.list()[0]
    assert environment.external_url == "http://new.env/whatever"

    environment.stop()

    environment.delete()


def test_project_events(project):
    events = project.events.list()
    assert isinstance(events, list)


def test_project_file_uploads(project):
    filename = "test.txt"
    file_contents = "testing contents"

    uploaded_file = project.upload(filename, file_contents)
    alt, url = uploaded_file["alt"], uploaded_file["url"]
    assert alt == filename
    assert url.startswith("/uploads/")
    assert url.endswith(f"/{filename}")
    assert uploaded_file["markdown"] == f"[{alt}]({url})"


def test_project_forks(gl, project, user):
    fork = project.forks.create({"namespace": user.username})
    fork_project = gl.projects.get(fork.id)
    assert fork_project.forked_from_project["id"] == project.id

    forks = project.forks.list()
    assert fork.id in [fork_project.id for fork_project in forks]


def test_project_hooks(project):
    hook = project.hooks.create({"url": "http://hook.url"})
    assert hook in project.hooks.list()

    hook.note_events = True
    hook.save()

    hook = project.hooks.get(hook.id)
    assert hook.note_events is True

    hook.delete()


def test_project_housekeeping(project):
    project.housekeeping()


def test_project_labels(project):
    label = project.labels.create({"name": "label", "color": "#778899"})
    labels = project.labels.list()
    assert label in labels

    label = project.labels.get("label")
    assert label == labels[0]

    label.new_name = "Label:that requires:encoding"
    label.save()
    assert label.name == "Label:that requires:encoding"
    label = project.labels.get("Label:that requires:encoding")
    assert label.name == "Label:that requires:encoding"

    label.subscribe()
    assert label.subscribed is True

    label.unsubscribe()
    assert label.subscribed is False

    label.delete()


def test_project_label_promotion(gl, group):
    """
    Label promotion requires the project to be a child of a group (not in a user namespace)

    """
    _id = uuid.uuid4().hex
    data = {
        "name": f"test-project-{_id}",
        "namespace_id": group.id,
    }
    project = gl.projects.create(data)

    label_name = "promoteme"
    promoted_label = project.labels.create({"name": label_name, "color": "#112233"})
    promoted_label.promote()

    assert any(label.name == label_name for label in group.labels.list())

    group.labels.delete(label_name)


def test_project_milestones(project):
    milestone = project.milestones.create({"title": "milestone1"})
    assert milestone in project.milestones.list()

    milestone.due_date = "2020-01-01T00:00:00Z"
    milestone.save()

    milestone.state_event = "close"
    milestone.save()

    milestone = project.milestones.get(milestone.id)
    assert milestone.state == "closed"
    assert not milestone.issues()
    assert not milestone.merge_requests()


def test_project_milestone_promotion(gl, group):
    """
    Milestone promotion requires the project to be a child of a group (not in a user namespace)

    """
    _id = uuid.uuid4().hex
    data = {
        "name": f"test-project-{_id}",
        "namespace_id": group.id,
    }
    project = gl.projects.create(data)

    milestone_title = "promoteme"
    promoted_milestone = project.milestones.create({"title": milestone_title})
    promoted_milestone.promote()

    assert any(
        milestone.title == milestone_title for milestone in group.milestones.list()
    )


def test_project_pages(project):
    pages = project.pages.get()
    assert pages.is_unique_domain_enabled is True

    project.pages.update(new_data={"pages_unique_domain_enabled": False})

    pages.refresh()
    assert pages.is_unique_domain_enabled is False

    project.pages.delete()


def test_project_pages_domains(gl, project):
    domain = project.pagesdomains.create({"domain": "foo.domain.com"})
    assert domain in project.pagesdomains.list()
    assert domain in gl.pagesdomains.list()

    domain = project.pagesdomains.get("foo.domain.com")
    assert domain.domain == "foo.domain.com"

    domain.delete()


def test_project_protected_branches(project, gitlab_version):
    # Updating a protected branch is possible from Gitlab 15.6
    # https://docs.gitlab.com/ee/api/protected_branches.html#update-a-protected-branch
    can_update_prot_branch = gitlab_version.major > 15 or (
        gitlab_version.major == 15 and gitlab_version.minor >= 6
    )

    p_b = project.protectedbranches.create(
        {
            "name": "*-stable",
            "allow_force_push": False,
        }
    )
    assert p_b.name == "*-stable"
    assert not p_b.allow_force_push
    assert p_b in project.protectedbranches.list()

    if can_update_prot_branch:
        p_b.allow_force_push = True
        p_b.save()
        # Pause to let GL catch up (happens on hosted too, sometimes takes a while for server to be ready to merge)
        time.sleep(5)

    p_b = project.protectedbranches.get("*-stable")
    if can_update_prot_branch:
        assert p_b.allow_force_push

        p_b.delete()


def test_project_remote_mirrors(project):
    mirror_url = "https://gitlab.example.com/root/mirror.git"

    mirror = project.remote_mirrors.create({"url": mirror_url})
    assert mirror.url == mirror_url

    mirror.enabled = True
    mirror.save()

    mirror = project.remote_mirrors.list()[0]
    assert isinstance(mirror, gitlab.v4.objects.ProjectRemoteMirror)
    assert mirror.url == mirror_url
    assert mirror.enabled is True

    mirror.delete()


def test_project_services(project):
    # Use 'update' to create a service as we don't have a 'create' method and
    # to add one is somewhat complicated so it hasn't been done yet.
    project.services.update("asana", api_key="foo")

    service = project.services.get("asana")
    assert service.active is True
    service.api_key = "whatever"
    service.save()

    service = project.services.get("asana")
    assert service.active is True

    service.delete()


def test_project_stars(project):
    project.star()
    assert project.star_count == 1

    project.unstar()
    assert project.star_count == 0


def test_project_storage(project):
    storage = project.storage.get()
    assert isinstance(storage, ProjectStorage)
    assert storage.repository_storage == "default"


def test_project_tags(project, project_file):
    tag = project.tags.create({"tag_name": "v1.0", "ref": "main"})
    assert tag in project.tags.list()

    tag.delete()


def test_project_triggers(project):
    trigger = project.triggers.create({"description": "trigger1"})
    assert trigger in project.triggers.list()

    trigger.delete()


def test_project_wiki(project):
    content = "Wiki page content"
    wiki = project.wikis.create({"title": "wikipage", "content": content})
    assert wiki in project.wikis.list()

    wiki = project.wikis.get(wiki.slug)
    assert wiki.content == content

    # update and delete seem broken
    wiki.content = "new content"
    wiki.save()

    wiki.delete()


def test_project_groups_list(gl, group):
    """Test listing groups of a project"""
    # Create a subgroup of our top-group, we will place our new project inside
    # this group.
    group2 = gl.groups.create(
        {"name": "group2_proj", "path": "group2_proj", "parent_id": group.id}
    )
    data = {
        "name": "test-project-tpsg",
        "namespace_id": group2.id,
    }
    project = gl.projects.create(data)

    groups = project.groups.list()
    group_ids = set([x.id for x in groups])
    assert {group.id, group2.id} == group_ids


def test_project_transfer(gl, project, group):
    assert project.namespace["path"] != group.full_path
    project.transfer(group.id)

    project = gl.projects.get(project.id)
    assert project.namespace["path"] == group.full_path

    gl.auth()
    project.transfer(gl.user.username)

    project = gl.projects.get(project.id)
    assert project.namespace["path"] == gl.user.username
