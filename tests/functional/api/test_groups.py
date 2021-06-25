import pytest

import gitlab


def test_groups(gl):
    # TODO: This one still needs lots of work
    user = gl.users.create(
        {
            "email": "user@test.com",
            "username": "user",
            "name": "user",
            "password": "user_pass",
        }
    )
    user2 = gl.users.create(
        {
            "email": "user2@test.com",
            "username": "user2",
            "name": "user2",
            "password": "user2_pass",
        }
    )
    group1 = gl.groups.create({"name": "group1", "path": "group1"})
    group2 = gl.groups.create({"name": "group2", "path": "group2"})

    p_id = gl.groups.list(search="group2")[0].id
    group3 = gl.groups.create({"name": "group3", "path": "group3", "parent_id": p_id})
    group4 = gl.groups.create({"name": "group4", "path": "group4"})

    assert len(gl.groups.list()) == 4
    assert len(gl.groups.list(search="oup1")) == 1
    assert group3.parent_id == p_id
    assert group2.subgroups.list()[0].id == group3.id
    assert group2.descendant_groups.list()[0].id == group3.id

    filtered_groups = gl.groups.list(skip_groups=[group3.id, group4.id])
    assert group3 not in filtered_groups
    assert group3 not in filtered_groups

    group1.members.create(
        {"access_level": gitlab.const.OWNER_ACCESS, "user_id": user.id}
    )
    group1.members.create(
        {"access_level": gitlab.const.GUEST_ACCESS, "user_id": user2.id}
    )
    group2.members.create(
        {"access_level": gitlab.const.OWNER_ACCESS, "user_id": user2.id}
    )

    group4.share(group1.id, gitlab.const.DEVELOPER_ACCESS)
    group4.share(group2.id, gitlab.const.MAINTAINER_ACCESS)
    # Reload group4 to have updated shared_with_groups
    group4 = gl.groups.get(group4.id)
    assert len(group4.shared_with_groups) == 2
    group4.unshare(group1.id)
    # Reload group4 to have updated shared_with_groups
    group4 = gl.groups.get(group4.id)
    assert len(group4.shared_with_groups) == 1

    # User memberships (admin only)
    memberships1 = user.memberships.list()
    assert len(memberships1) == 1

    memberships2 = user2.memberships.list()
    assert len(memberships2) == 2

    membership = memberships1[0]
    assert membership.source_type == "Namespace"
    assert membership.access_level == gitlab.const.OWNER_ACCESS

    project_memberships = user.memberships.list(type="Project")
    assert len(project_memberships) == 0

    group_memberships = user.memberships.list(type="Namespace")
    assert len(group_memberships) == 1

    with pytest.raises(gitlab.GitlabListError) as e:
        membership = user.memberships.list(type="Invalid")
    assert "type does not have a valid value" in str(e.value)

    with pytest.raises(gitlab.GitlabListError) as e:
        user.memberships.list(sudo=user.name)
    assert "403 Forbidden" in str(e.value)

    # Administrator belongs to the groups
    assert len(group1.members.list()) == 3
    assert len(group2.members.list()) == 2

    group1.members.delete(user.id)
    assert len(group1.members.list()) == 2
    assert len(group1.members.all())  # Deprecated
    assert len(group1.members_all.list())
    member = group1.members.get(user2.id)
    member.access_level = gitlab.const.OWNER_ACCESS
    member.save()
    member = group1.members.get(user2.id)
    assert member.access_level == gitlab.const.OWNER_ACCESS

    group2.members.delete(gl.user.id)


@pytest.mark.skip(reason="Commented out in legacy test")
def test_group_labels(group):
    group.labels.create({"name": "foo", "description": "bar", "color": "#112233"})
    label = group.labels.get("foo")
    assert label.description == "bar"

    label.description = "baz"
    label.save()
    label = group.labels.get("foo")
    assert label.description == "baz"
    assert len(group.labels.list()) == 1

    label.delete()
    assert len(group.labels.list()) == 0


def test_group_notification_settings(group):
    settings = group.notificationsettings.get()
    settings.level = "disabled"
    settings.save()

    settings = group.notificationsettings.get()
    assert settings.level == "disabled"


def test_group_badges(group):
    badge_image = "http://example.com"
    badge_link = "http://example/img.svg"
    badge = group.badges.create({"link_url": badge_link, "image_url": badge_image})
    assert len(group.badges.list()) == 1

    badge.image_url = "http://another.example.com"
    badge.save()

    badge = group.badges.get(badge.id)
    assert badge.image_url == "http://another.example.com"

    badge.delete()
    assert len(group.badges.list()) == 0


def test_group_milestones(group):
    milestone = group.milestones.create({"title": "groupmilestone1"})
    assert len(group.milestones.list()) == 1

    milestone.due_date = "2020-01-01T00:00:00Z"
    milestone.save()
    milestone.state_event = "close"
    milestone.save()

    milestone = group.milestones.get(milestone.id)
    assert milestone.state == "closed"
    assert len(milestone.issues()) == 0
    assert len(milestone.merge_requests()) == 0


def test_group_custom_attributes(gl, group):
    attrs = group.customattributes.list()
    assert len(attrs) == 0

    attr = group.customattributes.set("key", "value1")
    assert len(gl.groups.list(custom_attributes={"key": "value1"})) == 1
    assert attr.key == "key"
    assert attr.value == "value1"
    assert len(group.customattributes.list()) == 1

    attr = group.customattributes.set("key", "value2")
    attr = group.customattributes.get("key")
    assert attr.value == "value2"
    assert len(group.customattributes.list()) == 1

    attr.delete()
    assert len(group.customattributes.list()) == 0


def test_group_subgroups_projects(gl, user):
    # TODO: fixture factories
    group1 = gl.groups.list(search="group1")[0]
    group2 = gl.groups.list(search="group2")[0]

    group3 = gl.groups.create(
        {"name": "subgroup1", "path": "subgroup1", "parent_id": group1.id}
    )
    group4 = gl.groups.create(
        {"name": "subgroup2", "path": "subgroup2", "parent_id": group2.id}
    )

    gr1_project = gl.projects.create({"name": "gr1_project", "namespace_id": group1.id})
    gr2_project = gl.projects.create({"name": "gr2_project", "namespace_id": group3.id})

    assert group3.parent_id == group1.id
    assert group4.parent_id == group2.id
    assert gr1_project.namespace["id"] == group1.id
    assert gr2_project.namespace["parent_id"] == group1.id


@pytest.mark.skip
def test_group_wiki(group):
    content = "Group Wiki page content"
    wiki = group.wikis.create({"title": "groupwikipage", "content": content})
    assert len(group.wikis.list()) == 1

    wiki = group.wikis.get(wiki.slug)
    assert wiki.content == content

    wiki.content = "new content"
    wiki.save()
    wiki.delete()
    assert len(group.wikis.list()) == 0


def test_group_hooks(group):
    hook = group.hooks.create({"url": "http://hook.url"})
    assert len(group.hooks.list()) == 1

    hook.note_events = True
    hook.save()

    hook = group.hooks.get(hook.id)
    assert hook.note_events is True
    hook.delete()
