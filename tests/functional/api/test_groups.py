import pytest

import gitlab


def test_groups(gl):
    # TODO: This one still needs lots of work
    user = gl.users.create(
        {
            "email": "user@test.com",
            "username": "user",
            "name": "user",
            "password": "E4596f8be406Bc3a14a4ccdb1df80587#!1",
        }
    )
    user2 = gl.users.create(
        {
            "email": "user2@test.com",
            "username": "user2",
            "name": "user2",
            "password": "E4596f8be406Bc3a14a4ccdb1df80587#!#2",
        }
    )
    group1 = gl.groups.create(
        {"name": "gitlab-test-group1", "path": "gitlab-test-group1"}
    )
    group2 = gl.groups.create(
        {"name": "gitlab-test-group2", "path": "gitlab-test-group2"}
    )

    p_id = gl.groups.list(search="gitlab-test-group2")[0].id
    group3 = gl.groups.create(
        {"name": "gitlab-test-group3", "path": "gitlab-test-group3", "parent_id": p_id}
    )
    group4 = gl.groups.create(
        {"name": "gitlab-test-group4", "path": "gitlab-test-group4"}
    )

    assert {group1, group2, group3, group4} <= set(gl.groups.list())
    assert gl.groups.list(search="gitlab-test-group1")[0].id == group1.id
    assert group3.parent_id == p_id
    assert group2.subgroups.list()[0].id == group3.id
    assert group2.descendant_groups.list()[0].id == group3.id

    filtered_groups = gl.groups.list(skip_groups=[group3.id, group4.id])
    assert group3 not in filtered_groups
    assert group4 not in filtered_groups

    filtered_groups = gl.groups.list(skip_groups=[group3.id])
    assert group3 not in filtered_groups
    assert group4 in filtered_groups

    group1.members.create(
        {"access_level": gitlab.const.AccessLevel.OWNER, "user_id": user.id}
    )
    group1.members.create(
        {"access_level": gitlab.const.AccessLevel.GUEST, "user_id": user2.id}
    )
    group2.members.create(
        {"access_level": gitlab.const.AccessLevel.OWNER, "user_id": user2.id}
    )

    group4.share(group1.id, gitlab.const.AccessLevel.DEVELOPER)
    group4.share(group2.id, gitlab.const.AccessLevel.MAINTAINER)
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
    assert membership.access_level == gitlab.const.AccessLevel.OWNER

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

    # Test `user_ids` array
    result = group1.members.list(user_ids=[user.id, 99999])
    assert len(result) == 1
    assert result[0].id == user.id

    group1.members.delete(user.id)

    assert group1.members_all.list()

    member = group1.members.get(user2.id)
    member.access_level = gitlab.const.AccessLevel.OWNER
    member.save()
    member = group1.members.get(user2.id)
    assert member.access_level == gitlab.const.AccessLevel.OWNER

    gl.auth()
    group2.members.delete(gl.user.id)


def test_group_labels(group):
    group.labels.create({"name": "foo", "description": "bar", "color": "#112233"})
    label = group.labels.get("foo")
    assert label.description == "bar"

    label.description = "baz"
    label.save()
    label = group.labels.get("foo")
    assert label.description == "baz"
    assert label in group.labels.list()

    label.new_name = "Label:that requires:encoding"
    label.save()
    assert label.name == "Label:that requires:encoding"
    label = group.labels.get("Label:that requires:encoding")
    assert label.name == "Label:that requires:encoding"

    label.delete()


@pytest.mark.gitlab_premium
@pytest.mark.xfail(reason="/ldap/groups endpoint not documented")
def test_ldap_groups(gl):
    assert isinstance(gl.ldapgroups.list(), list)


@pytest.mark.gitlab_premium
def test_group_ldap_links(group):
    ldap_cn = "common-name"
    ldap_provider = "ldap-provider"

    ldap_cn_link = group.ldap_group_links.create(
        {"provider": ldap_provider, "group_access": 30, "cn": ldap_cn}
    )
    ldap_filter_link = group.ldap_group_links.create(
        {"provider": ldap_provider, "group_access": 30, "filter": "(cn=Common Name)"}
    )

    ldap_links = group.ldap_group_links.list()

    assert ldap_cn_link.cn == ldap_links[0].cn
    assert ldap_filter_link.filter == ldap_links[1].filter

    with pytest.raises(gitlab.GitlabCreateError):
        # todo - can we configure dummy LDAP in the container?
        group.ldap_sync()

    ldap_filter_link.delete()
    group.ldap_group_links.delete(provider=ldap_provider, cn=ldap_cn)

    with pytest.raises(gitlab.GitlabListError, match="No linked LDAP groups found"):
        group.ldap_group_links.list()


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
    assert badge in group.badges.list()

    badge.image_url = "http://another.example.com"
    badge.save()

    badge = group.badges.get(badge.id)
    assert badge.image_url == "http://another.example.com"

    badge.delete()


def test_group_milestones(group):
    milestone = group.milestones.create({"title": "groupmilestone1"})
    assert milestone in group.milestones.list()

    milestone.due_date = "2020-01-01T00:00:00Z"
    milestone.save()
    milestone.state_event = "close"
    milestone.save()

    milestone = group.milestones.get(milestone.id)
    assert milestone.state == "closed"
    assert not milestone.issues()
    assert not milestone.merge_requests()


def test_group_custom_attributes(gl, group):
    attrs = group.customattributes.list()
    assert not attrs

    attr = group.customattributes.set("key", "value1")
    assert group in gl.groups.list(custom_attributes={"key": "value1"})
    assert attr.key == "key"
    assert attr.value == "value1"
    assert attr in group.customattributes.list()

    attr = group.customattributes.set("key", "value2")
    attr = group.customattributes.get("key")
    assert attr.value == "value2"
    assert attr in group.customattributes.list()

    attr.delete()


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

    gr1_project.delete()
    gr2_project.delete()
    group3.delete()
    group4.delete()


@pytest.mark.gitlab_premium
def test_group_wiki(group):
    content = "Group Wiki page content"
    wiki = group.wikis.create({"title": "groupwikipage", "content": content})
    assert wiki in group.wikis.list()

    wiki = group.wikis.get(wiki.slug)
    assert wiki.content == content

    wiki.content = "new content"
    wiki.save()

    wiki.delete()


@pytest.mark.gitlab_premium
def test_group_hooks(group):
    hook = group.hooks.create({"url": "http://hook.url"})
    assert hook in group.hooks.list()

    hook.note_events = True
    hook.save()

    hook = group.hooks.get(hook.id)
    assert hook.note_events is True

    hook.delete()


def test_group_transfer(gl, group):
    transfer_group = gl.groups.create(
        {"name": "transfer-test-group", "path": "transfer-test-group"}
    )
    transfer_group = gl.groups.get(transfer_group.id)
    assert transfer_group.parent_id != group.id

    transfer_group.transfer(group.id)

    transferred_group = gl.groups.get(transfer_group.id)
    assert transferred_group.parent_id == group.id

    transfer_group.transfer()

    transferred_group = gl.groups.get(transfer_group.id)
    assert transferred_group.path == transferred_group.full_path


@pytest.mark.gitlab_premium
@pytest.mark.xfail(reason="need to setup an identity provider or it's mock")
def test_group_saml_group_links(group):
    group.saml_group_links.create(
        {"saml_group_name": "saml-group-1", "access_level": 10}
    )


@pytest.mark.gitlab_premium
def test_group_service_account(group):
    service_account = group.service_accounts.create(
        {"name": "gitlab-service-account", "username": "gitlab-service-account"}
    )
    assert service_account.name == "gitlab-service-account"
    assert service_account.username == "gitlab-service-account"
