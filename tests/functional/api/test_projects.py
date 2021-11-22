import uuid

import pytest

import gitlab


def test_create_project(gl, user):
    # Moved from group tests chunk in legacy tests, TODO cleanup
    admin_project = gl.projects.create({"name": "admin_project"})
    assert isinstance(admin_project, gitlab.v4.objects.Project)
    assert len(gl.projects.list(search="admin")) == 1

    sudo_project = gl.projects.create({"name": "sudo_project"}, sudo=user.id)

    created = gl.projects.list()
    created_gen = gl.projects.list(as_list=False)
    owned = gl.projects.list(owned=True)

    assert admin_project in created and sudo_project in created
    assert admin_project in owned and sudo_project not in owned
    assert len(created) == len(list(created_gen))

    admin_project.delete()
    sudo_project.delete()


def test_project_badges(project):
    badge_image = "http://example.com"
    badge_link = "http://example/img.svg"

    badge = project.badges.create({"link_url": badge_link, "image_url": badge_image})
    assert len(project.badges.list()) == 1

    badge.image_url = "http://another.example.com"
    badge.save()

    badge = project.badges.get(badge.id)
    assert badge.image_url == "http://another.example.com"

    badge.delete()
    assert len(project.badges.list()) == 0


@pytest.mark.skip(reason="Commented out in legacy test")
def test_project_boards(project):
    boards = project.boards.list()
    assert len(boards)

    board = boards[0]
    lists = board.lists.list()
    begin_size = len(lists)
    last_list = lists[-1]
    last_list.position = 0
    last_list.save()
    last_list.delete()
    lists = board.lists.list()
    assert len(lists) == begin_size - 1


def test_project_custom_attributes(gl, project):
    attrs = project.customattributes.list()
    assert len(attrs) == 0

    attr = project.customattributes.set("key", "value1")
    assert attr.key == "key"
    assert attr.value == "value1"
    assert len(project.customattributes.list()) == 1
    assert len(gl.projects.list(custom_attributes={"key": "value1"})) == 1

    attr = project.customattributes.set("key", "value2")
    attr = project.customattributes.get("key")
    assert attr.value == "value2"
    assert len(project.customattributes.list()) == 1

    attr.delete()
    assert len(project.customattributes.list()) == 0


def test_project_environments(project):
    project.environments.create(
        {"name": "env1", "external_url": "http://fake.env/whatever"}
    )
    environments = project.environments.list()
    assert len(environments) == 1

    environment = environments[0]
    environment.external_url = "http://new.env/whatever"
    environment.save()

    environment = project.environments.list()[0]
    assert environment.external_url == "http://new.env/whatever"

    environment.stop()
    environment.delete()
    assert len(project.environments.list()) == 0


def test_project_events(project):
    events = project.events.list()
    assert isinstance(events, list)


def test_project_file_uploads(project):
    filename = "test.txt"
    file_contents = "testing contents"

    uploaded_file = project.upload(filename, file_contents)
    assert uploaded_file["alt"] == filename
    assert uploaded_file["url"].startswith("/uploads/")
    assert uploaded_file["url"].endswith(f"/{filename}")
    assert uploaded_file["markdown"] == "[{}]({})".format(
        uploaded_file["alt"], uploaded_file["url"]
    )


def test_project_forks(gl, project, user):
    fork = project.forks.create({"namespace": user.username})
    fork_project = gl.projects.get(fork.id)
    assert fork_project.forked_from_project["id"] == project.id

    forks = project.forks.list()
    assert fork.id in map(lambda fork_project: fork_project.id, forks)


def test_project_hooks(project):
    hook = project.hooks.create({"url": "http://hook.url"})
    assert len(project.hooks.list()) == 1

    hook.note_events = True
    hook.save()

    hook = project.hooks.get(hook.id)
    assert hook.note_events is True
    hook.delete()


def test_project_housekeeping(project):
    project.housekeeping()


def test_project_labels(project):
    print("JLV: project.id:", project.id)
    print("JLV: project.labels:", project.labels)
    label = project.labels.create({"name": "label", "color": "#778899"})
    print("JLV: type(label):", type(label))
    print("JLV: label.manager._computed_path:", label.manager._computed_path)
    print("JLV: label.manager._parent:", label.manager._parent)
    labels = project.labels.list()
    assert len(labels) == 1

    label = project.labels.get("label")
    assert label == labels[0]

    print("JLV: type(label):", type(label))
    print("JLV: label.manager._computed_path:", label.manager._computed_path)
    print("JLV: label.manager._parent:", label.manager._parent)
    label.new_name = "labelupdated"
    label.save()
    assert label.name == "labelupdated"

    label.subscribe()
    assert label.subscribed is True

    label.unsubscribe()
    assert label.subscribed is False

    label.delete()
    assert len(project.labels.list()) == 0

    assert "1" is None


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
    assert not any(label.name == label_name for label in group.labels.list())


def test_project_milestones(project):
    milestone = project.milestones.create({"title": "milestone1"})
    assert len(project.milestones.list()) == 1

    milestone.due_date = "2020-01-01T00:00:00Z"
    milestone.save()

    milestone.state_event = "close"
    milestone.save()

    milestone = project.milestones.get(milestone.id)
    assert milestone.state == "closed"
    assert len(milestone.issues()) == 0
    assert len(milestone.merge_requests()) == 0


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


def test_project_pages_domains(gl, project):
    domain = project.pagesdomains.create({"domain": "foo.domain.com"})
    assert len(project.pagesdomains.list()) == 1
    assert len(gl.pagesdomains.list()) == 1

    domain = project.pagesdomains.get("foo.domain.com")
    assert domain.domain == "foo.domain.com"

    domain.delete()
    assert len(project.pagesdomains.list()) == 0


def test_project_protected_branches(project):
    p_b = project.protectedbranches.create({"name": "*-stable"})
    assert p_b.name == "*-stable"
    assert len(project.protectedbranches.list()) == 1

    p_b = project.protectedbranches.get("*-stable")
    p_b.delete()
    assert len(project.protectedbranches.list()) == 0


def test_project_remote_mirrors(project):
    mirror_url = "http://gitlab.test/root/mirror.git"

    mirror = project.remote_mirrors.create({"url": mirror_url})
    assert mirror.url == mirror_url

    mirror.enabled = True
    mirror.save()

    mirror = project.remote_mirrors.list()[0]
    assert isinstance(mirror, gitlab.v4.objects.ProjectRemoteMirror)
    assert mirror.url == mirror_url
    assert mirror.enabled is True


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

    service = project.services.get("asana")
    assert service.active is False


def test_project_stars(project):
    project.star()
    assert project.star_count == 1

    project.unstar()
    assert project.star_count == 0


def test_project_tags(project, project_file):
    tag = project.tags.create({"tag_name": "v1.0", "ref": "main"})
    assert len(project.tags.list()) == 1

    tag.delete()
    assert len(project.tags.list()) == 0


def test_project_triggers(project):
    trigger = project.triggers.create({"description": "trigger1"})
    assert len(project.triggers.list()) == 1
    trigger.delete()


def test_project_wiki(project):
    content = "Wiki page content"
    wiki = project.wikis.create({"title": "wikipage", "content": content})
    assert len(project.wikis.list()) == 1

    wiki = project.wikis.get(wiki.slug)
    assert wiki.content == content

    # update and delete seem broken
    wiki.content = "new content"
    wiki.save()
    wiki.delete()
    assert len(project.wikis.list()) == 0
