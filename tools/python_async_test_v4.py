import asyncio
import base64
import os

import httpx

import gitlab

LOGIN = "root"
PASSWORD = "5iveL!fe"

SSH_KEY = (
    "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDZAjAX8vTiHD7Yi3/EzuVaDChtih"
    "79HyJZ6H9dEqxFfmGA1YnncE0xujQ64TCebhkYJKzmTJCImSVkOu9C4hZgsw6eE76n"
    "+Cg3VwEeDUFy+GXlEJWlHaEyc3HWioxgOALbUp3rOezNh+d8BDwwqvENGoePEBsz5l"
    "a6WP5lTi/HJIjAl6Hu+zHgdj1XVExeH+S52EwpZf/ylTJub0Bl5gHwf/siVE48mLMI"
    "sqrukXTZ6Zg+8EHAIvIQwJ1dKcXe8P5IoLT7VKrbkgAnolS0I8J+uH7KtErZJb5oZh"
    "S4OEwsNpaXMAr+6/wWSpircV2/e7sFLlhlKBC4Iq1MpqlZ7G3p foo@bar"
)
DEPLOY_KEY = (
    "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDFdRyjJQh+1niBpXqE2I8dzjG"
    "MXFHlRjX9yk/UfOn075IdaockdU58sw2Ai1XIWFpZpfJkW7z+P47ZNSqm1gzeXI"
    "rtKa9ZUp8A7SZe8vH4XVn7kh7bwWCUirqtn8El9XdqfkzOs/+FuViriUWoJVpA6"
    "WZsDNaqINFKIA5fj/q8XQw+BcS92L09QJg9oVUuH0VVwNYbU2M2IRmSpybgC/gu"
    "uWTrnCDMmLItksATifLvRZwgdI8dr+q6tbxbZknNcgEPrI2jT0hYN9ZcjNeWuyv"
    "rke9IepE7SPBT41C+YtUX4dfDZDmczM1cE0YL/krdUCfuZHMa4ZS2YyNd6slufc"
    "vn bar@foo"
)

GPG_KEY = """-----BEGIN PGP PUBLIC KEY BLOCK-----

mQENBFn5mzYBCADH6SDVPAp1zh/hxmTi0QplkOfExBACpuY6OhzNdIg+8/528b3g
Y5YFR6T/HLv/PmeHskUj21end1C0PNG2T9dTx+2Vlh9ISsSG1kyF9T5fvMR3bE0x
Dl6S489CXZrjPTS9SHk1kF+7dwjUxLJyxF9hPiSihFefDFu3NeOtG/u8vbC1mewQ
ZyAYue+mqtqcCIFFoBz7wHKMWjIVSJSyTkXExu4OzpVvy3l2EikbvavI3qNz84b+
Mgkv/kiBlNoCy3CVuPk99RYKZ3lX1vVtqQ0OgNGQvb4DjcpyjmbKyibuZwhDjIOh
au6d1OyEbayTntd+dQ4j9EMSnEvm/0MJ4eXPABEBAAG0G0dpdGxhYlRlc3QxIDxm
YWtlQGZha2UudGxkPokBNwQTAQgAIQUCWfmbNgIbAwULCQgHAgYVCAkKCwIEFgID
AQIeAQIXgAAKCRBgxELHf8f3hF3yB/wNJlWPKY65UsB4Lo0hs1OxdxCDqXogSi0u
6crDEIiyOte62pNZKzWy8TJcGZvznRTZ7t8hXgKFLz3PRMcl+vAiRC6quIDUj+2V
eYfwaItd1lUfzvdCaC7Venf4TQ74f5vvNg/zoGwE6eRoSbjlLv9nqsxeA0rUBUQL
LYikWhVMP3TrlfgfduYvh6mfgh57BDLJ9kJVpyfxxx9YLKZbaas9sPa6LgBtR555
JziUxHmbEv8XCsUU8uoFeP1pImbNBplqE3wzJwzOMSmmch7iZzrAwfN7N2j3Wj0H
B5kQddJ9dmB4BbU0IXGhWczvdpxboI2wdY8a1JypxOdePoph/43iuQENBFn5mzYB
CADnTPY0Zf3d9zLjBNgIb3yDl94uOcKCq0twNmyjMhHzGqw+UMe9BScy34GL94Al
xFRQoaL+7P8hGsnsNku29A/VDZivcI+uxTx4WQ7OLcn7V0bnHV4d76iky2ufbUt/
GofthjDs1SonePO2N09sS4V4uK0d5N4BfCzzXgvg8etCLxNmC9BGt7AaKUUzKBO4
2QvNNaC2C/8XEnOgNWYvR36ylAXAmo0sGFXUsBCTiq1fugS9pwtaS2JmaVpZZ3YT
pMZlS0+SjC5BZYFqSmKCsA58oBRzCxQz57nR4h5VEflgD+Hy0HdW0UHETwz83E6/
U0LL6YyvhwFr6KPq5GxinSvfABEBAAGJAR8EGAEIAAkFAln5mzYCGwwACgkQYMRC
x3/H94SJgwgAlKQb10/xcL/epdDkR7vbiei7huGLBpRDb/L5fM8B5W77Qi8Xmuqj
cCu1j99ZCA5hs/vwVn8j8iLSBGMC5gxcuaar/wtmiaEvT9fO/h6q4opG7NcuiJ8H
wRj8ccJmRssNqDD913PLz7T40Ts62blhrEAlJozGVG/q7T3RAZcskOUHKeHfc2RI
YzGsC/I9d7k6uxAv1L9Nm5F2HaAQDzhkdd16nKkGaPGR35cT1JLInkfl5cdm7ldN
nxs4TLO3kZjUTgWKdhpgRNF5hwaz51ZjpebaRf/ZqRuNyX4lIRolDxzOn/+O1o8L
qG2ZdhHHmSK2LaQLFiSprUkikStNU9BqSQ==
=5OGa
-----END PGP PUBLIC KEY BLOCK-----"""
AVATAR_PATH = os.path.join(os.path.dirname(__file__), "avatar.png")


async def main():
    # token authentication from config file
    gl = gitlab.Gitlab.from_config(config_files=["/tmp/python-gitlab.cfg"])
    gl.enable_debug()
    await gl.auth()
    assert isinstance(gl.user, gitlab.v4.objects.CurrentUser)

    # markdown
    html = await gl.markdown("foo")
    assert "foo" in html

    success, errors = await gl.lint("Invalid")
    assert success is False
    assert errors

    # sidekiq
    out = await gl.sidekiq.queue_metrics()
    assert isinstance(out, dict)
    assert "pages" in out["queues"]
    out = await gl.sidekiq.process_metrics()
    assert isinstance(out, dict)
    assert "hostname" in out["processes"][0]
    out = await gl.sidekiq.job_stats()
    assert isinstance(out, dict)
    assert "processed" in out["jobs"]
    out = await gl.sidekiq.compound_metrics()
    assert isinstance(out, dict)
    assert "jobs" in out
    assert "processes" in out
    assert "queues" in out

    # settings
    settings = await gl.settings.get()
    settings.default_projects_limit = 42
    await settings.save()
    settings = await gl.settings.get()
    assert settings.default_projects_limit == 42

    # users
    new_user = await gl.users.create(
        {
            "email": "foo@bar.com",
            "username": "foo",
            "name": "foo",
            "password": "foo_password",
            "avatar": open(AVATAR_PATH, "rb"),
        }
    )
    avatar_url = new_user.avatar_url.replace("gitlab.test", "localhost:8080")
    uploaded_avatar = httpx.get(avatar_url).content
    assert uploaded_avatar == open(AVATAR_PATH, "rb").read()
    users_list = await gl.users.list()
    for user in users_list:
        if user.username == "foo":
            break
    assert new_user.username == user.username
    assert new_user.email == user.email

    await new_user.block()
    await new_user.unblock()

    # user projects list
    assert len(await new_user.projects.list()) == 0

    # events list
    await new_user.events.list()

    foobar_user = await gl.users.create(
        {
            "email": "foobar@example.com",
            "username": "foobar",
            "name": "Foo Bar",
            "password": "foobar_password",
        }
    )

    assert (await gl.users.list(search="foobar"))[0].id == foobar_user.id
    expected = [new_user, foobar_user]
    actual = list(await gl.users.list(search="foo"))
    assert len(expected) == len(actual)
    assert len(await gl.users.list(search="asdf")) == 0
    foobar_user.bio = "This is the user bio"
    await foobar_user.save()

    # GPG keys
    gkey = await new_user.gpgkeys.create({"key": GPG_KEY})
    assert len(await new_user.gpgkeys.list()) == 1
    # Seems broken on the gitlab side
    # gkey = new_user.gpgkeys.get(gkey.id)
    await gkey.delete()
    assert len(await new_user.gpgkeys.list()) == 0

    # SSH keys
    key = await new_user.keys.create({"title": "testkey", "key": SSH_KEY})
    assert len(await new_user.keys.list()) == 1
    await key.delete()
    assert len(await new_user.keys.list()) == 0

    # emails
    email = await new_user.emails.create({"email": "foo2@bar.com"})
    assert len(await new_user.emails.list()) == 1
    await email.delete()
    assert len(await new_user.emails.list()) == 0

    # custom attributes
    attrs = await new_user.customattributes.list()
    assert len(attrs) == 0
    attr = await new_user.customattributes.set("key", "value1")
    assert len(await gl.users.list(custom_attributes={"key": "value1"})) == 1
    assert attr.key == "key"
    assert attr.value == "value1"
    assert len(await new_user.customattributes.list()) == 1
    attr = await new_user.customattributes.set("key", "value2")
    attr = await new_user.customattributes.get("key")
    assert attr.value == "value2"
    assert len(await new_user.customattributes.list()) == 1
    await attr.delete()
    assert len(await new_user.customattributes.list()) == 0

    # impersonation tokens
    user_token = await new_user.impersonationtokens.create(
        {"name": "token1", "scopes": ["api", "read_user"]}
    )
    l = await new_user.impersonationtokens.list(state="active")
    assert len(l) == 1
    await user_token.delete()
    l = await new_user.impersonationtokens.list(state="active")
    assert len(l) == 0
    l = await new_user.impersonationtokens.list(state="inactive")
    assert len(l) == 1

    await new_user.delete()
    await foobar_user.delete()
    assert len(await gl.users.list()) == 3 + len(
        [u for u in await gl.users.list() if u.username == "ghost"]
    )

    # current user mail
    mail = await gl.user.emails.create({"email": "current@user.com"})
    assert len(await gl.user.emails.list()) == 1
    await mail.delete()
    assert len(await gl.user.emails.list()) == 0

    # current user GPG keys
    gkey = await gl.user.gpgkeys.create({"key": GPG_KEY})
    assert len(await gl.user.gpgkeys.list()) == 1
    # Seems broken on the gitlab side
    gkey = await gl.user.gpgkeys.get(gkey.id)
    await gkey.delete()
    assert len(await gl.user.gpgkeys.list()) == 0

    # current user key
    key = await gl.user.keys.create({"title": "testkey", "key": SSH_KEY})
    assert len(await gl.user.keys.list()) == 1
    await key.delete()
    assert len(await gl.user.keys.list()) == 0

    # templates
    assert await gl.dockerfiles.list()
    dockerfile = await gl.dockerfiles.get("Node")
    assert dockerfile.content is not None

    assert await gl.gitignores.list()
    gitignore = await gl.gitignores.get("Node")
    assert gitignore.content is not None

    assert await gl.gitlabciymls.list()
    gitlabciyml = await gl.gitlabciymls.get("Nodejs")
    assert gitlabciyml.content is not None

    assert await gl.licenses.list()
    license = await gl.licenses.get(
        "bsd-2-clause", project="mytestproject", fullname="mytestfullname"
    )
    assert "mytestfullname" in license.content

    # groups
    user1 = await gl.users.create(
        {
            "email": "user1@test.com",
            "username": "user1",
            "name": "user1",
            "password": "user1_pass",
        }
    )
    user2 = await gl.users.create(
        {
            "email": "user2@test.com",
            "username": "user2",
            "name": "user2",
            "password": "user2_pass",
        }
    )
    group1 = await gl.groups.create({"name": "group1", "path": "group1"})
    group2 = await gl.groups.create({"name": "group2", "path": "group2"})

    p_id = (await gl.groups.list(search="group2"))[0].id
    group3 = await gl.groups.create(
        {"name": "group3", "path": "group3", "parent_id": p_id}
    )

    assert len(await gl.groups.list()) == 3
    assert len(await gl.groups.list(search="oup1")) == 1
    assert group3.parent_id == p_id
    assert (await group2.subgroups.list())[0].id == group3.id

    await group1.members.create(
        {"access_level": gitlab.const.OWNER_ACCESS, "user_id": user1.id}
    )
    await group1.members.create(
        {"access_level": gitlab.const.GUEST_ACCESS, "user_id": user2.id}
    )

    await group2.members.create(
        {"access_level": gitlab.const.OWNER_ACCESS, "user_id": user2.id}
    )

    # Administrator belongs to the groups
    assert len(await group1.members.list()) == 3
    assert len(await group2.members.list()) == 2

    await group1.members.delete(user1.id)
    assert len(await group1.members.list()) == 2
    assert len(await group1.members.all())
    member = await group1.members.get(user2.id)
    member.access_level = gitlab.const.OWNER_ACCESS
    await member.save()
    member = await group1.members.get(user2.id)
    assert member.access_level == gitlab.const.OWNER_ACCESS

    await group2.members.delete(gl.user.id)

    # group custom attributes
    attrs = await group2.customattributes.list()
    assert len(attrs) == 0
    attr = await group2.customattributes.set("key", "value1")
    assert len(await gl.groups.list(custom_attributes={"key": "value1"})) == 1
    assert attr.key == "key"
    assert attr.value == "value1"
    assert len(await group2.customattributes.list()) == 1
    attr = await group2.customattributes.set("key", "value2")
    attr = await group2.customattributes.get("key")
    assert attr.value == "value2"
    assert len(await group2.customattributes.list()) == 1
    await attr.delete()
    assert len(await group2.customattributes.list()) == 0

    # group notification settings
    settings = await group2.notificationsettings.get()
    settings.level = "disabled"
    await settings.save()
    settings = await group2.notificationsettings.get()
    assert settings.level == "disabled"

    # group badges
    badge_image = "http://example.com"
    badge_link = "http://example/img.svg"
    badge = await group2.badges.create(
        {"link_url": badge_link, "image_url": badge_image}
    )
    assert len(await group2.badges.list()) == 1
    badge.image_url = "http://another.example.com"
    await badge.save()
    badge = await group2.badges.get(badge.id)
    assert badge.image_url == "http://another.example.com"
    await badge.delete()
    assert len(await group2.badges.list()) == 0

    # group milestones
    gm1 = await group1.milestones.create({"title": "groupmilestone1"})
    assert len(await group1.milestones.list()) == 1
    gm1.due_date = "2020-01-01T00:00:00Z"
    await gm1.save()
    gm1.state_event = "close"
    await gm1.save()
    gm1 = await group1.milestones.get(gm1.id)
    assert gm1.state == "closed"
    assert len(await gm1.issues()) == 0
    assert len(await gm1.merge_requests()) == 0

    # group variables
    await group1.variables.create({"key": "foo", "value": "bar"})
    g_v = await group1.variables.get("foo")
    assert g_v.value == "bar"
    g_v.value = "baz"
    await g_v.save()
    g_v = await group1.variables.get("foo")
    assert g_v.value == "baz"
    assert len(await group1.variables.list()) == 1
    await g_v.delete()
    assert len(await group1.variables.list()) == 0

    # group labels
    # group1.labels.create({"name": "foo", "description": "bar", "color": "#112233"})
    # g_l = group1.labels.get("foo")
    # assert g_l.description == "bar"
    # g_l.description = "baz"
    # g_l.save()
    # g_l = group1.labels.get("foo")
    # assert g_l.description == "baz"
    # assert len(group1.labels.list()) == 1
    # g_l.delete()
    # assert len(group1.labels.list()) == 0

    # hooks
    hook = await gl.hooks.create({"url": "http://whatever.com"})
    assert len(await gl.hooks.list()) == 1
    await hook.delete()
    assert len(await gl.hooks.list()) == 0

    # projects
    admin_project = await gl.projects.create({"name": "admin_project"})
    gr1_project = await gl.projects.create(
        {"name": "gr1_project", "namespace_id": group1.id}
    )
    gr2_project = await gl.projects.create(
        {"name": "gr2_project", "namespace_id": group2.id}
    )
    sudo_project = await gl.projects.create({"name": "sudo_project"}, sudo=user1.name)

    assert len(await gl.projects.list(owned=True)) == 2
    assert len(await gl.projects.list(search="admin")) == 1

    # test pagination
    l1 = await gl.projects.list(per_page=1, page=1)
    l2 = await gl.projects.list(per_page=1, page=2)
    assert len(l1) == 1
    assert len(l2) == 1
    assert l1[0].id != l2[0].id

    # group custom attributes
    attrs = await admin_project.customattributes.list()
    assert len(attrs) == 0
    attr = await admin_project.customattributes.set("key", "value1")
    assert len(await gl.projects.list(custom_attributes={"key": "value1"})) == 1
    assert attr.key == "key"
    assert attr.value == "value1"
    assert len(await admin_project.customattributes.list()) == 1
    attr = await admin_project.customattributes.set("key", "value2")
    attr = await admin_project.customattributes.get("key")
    assert attr.value == "value2"
    assert len(await admin_project.customattributes.list()) == 1
    await attr.delete()
    assert len(await admin_project.customattributes.list()) == 0

    # project pages domains
    domain = await admin_project.pagesdomains.create({"domain": "foo.domain.com"})
    assert len(await admin_project.pagesdomains.list()) == 1
    assert len(await gl.pagesdomains.list()) == 1
    domain = await admin_project.pagesdomains.get("foo.domain.com")
    assert domain.domain == "foo.domain.com"
    await domain.delete()
    assert len(await admin_project.pagesdomains.list()) == 0

    # project content (files)
    await admin_project.files.create(
        {
            "file_path": "README",
            "branch": "master",
            "content": "Initial content",
            "commit_message": "Initial commit",
        }
    )
    readme = await admin_project.files.get(file_path="README", ref="master")
    readme.content = base64.b64encode(b"Improved README").decode()
    await asyncio.sleep(2)
    await readme.save(branch="master", commit_message="new commit")
    await readme.delete(commit_message="Removing README", branch="master")

    await admin_project.files.create(
        {
            "file_path": "README.rst",
            "branch": "master",
            "content": "Initial content",
            "commit_message": "New commit",
        }
    )
    readme = await admin_project.files.get(file_path="README.rst", ref="master")
    # The first decode() is the ProjectFile method, the second one is the bytes
    # object method
    assert readme.decode().decode() == "Initial content"

    blame = await admin_project.files.blame(file_path="README.rst", ref="master")

    data = {
        "branch": "master",
        "commit_message": "blah blah blah",
        "actions": [{"action": "create", "file_path": "blah", "content": "blah"}],
    }
    await admin_project.commits.create(data)
    assert "@@" in (await (await admin_project.commits.list())[0].diff())[0]["diff"]

    # commit status
    commit = (await admin_project.commits.list())[0]
    # size = len(commit.statuses.list())
    # status = commit.statuses.create({"state": "success", "sha": commit.id})
    # assert len(commit.statuses.list()) == size + 1

    # assert commit.refs()
    # assert commit.merge_requests()

    # commit comment
    await commit.comments.create({"note": "This is a commit comment"})
    # assert len(commit.comments.list()) == 1

    # commit discussion
    count = len(await commit.discussions.list())
    discussion = await commit.discussions.create({"body": "Discussion body"})
    # assert len(commit.discussions.list()) == (count + 1)
    d_note = await discussion.notes.create({"body": "first note"})
    d_note_from_get = await discussion.notes.get(d_note.id)
    d_note_from_get.body = "updated body"
    await d_note_from_get.save()
    discussion = await commit.discussions.get(discussion.id)
    # assert discussion.attributes["notes"][-1]["body"] == "updated body"
    await d_note_from_get.delete()
    discussion = await commit.discussions.get(discussion.id)
    # assert len(discussion.attributes["notes"]) == 1

    # housekeeping
    await admin_project.housekeeping()

    # repository
    tree = await admin_project.repository_tree()
    assert len(tree) != 0
    assert tree[0]["name"] == "README.rst"
    blob_id = tree[0]["id"]
    blob = await admin_project.repository_raw_blob(blob_id)
    assert blob.decode() == "Initial content"
    archive1 = await admin_project.repository_archive()
    archive2 = await admin_project.repository_archive("master")
    assert archive1 == archive2
    snapshot = await admin_project.snapshot()

    # project file uploads
    filename = "test.txt"
    file_contents = "testing contents"
    uploaded_file = await admin_project.upload(filename, file_contents)
    assert uploaded_file["alt"] == filename
    assert uploaded_file["url"].startswith("/uploads/")
    assert uploaded_file["url"].endswith("/" + filename)
    assert uploaded_file["markdown"] == "[{}]({})".format(
        uploaded_file["alt"], uploaded_file["url"]
    )

    # environments
    await admin_project.environments.create(
        {"name": "env1", "external_url": "http://fake.env/whatever"}
    )
    envs = await admin_project.environments.list()
    assert len(envs) == 1
    env = envs[0]
    env.external_url = "http://new.env/whatever"
    await env.save()
    env = (await admin_project.environments.list())[0]
    assert env.external_url == "http://new.env/whatever"
    await env.stop()
    await env.delete()
    assert len(await admin_project.environments.list()) == 0

    # Project clusters
    await admin_project.clusters.create(
        {
            "name": "cluster1",
            "platform_kubernetes_attributes": {
                "api_url": "http://url",
                "token": "tokenval",
            },
        }
    )
    clusters = await admin_project.clusters.list()
    assert len(clusters) == 1
    cluster = clusters[0]
    cluster.platform_kubernetes_attributes = {"api_url": "http://newurl"}
    await cluster.save()
    cluster = (await admin_project.clusters.list())[0]
    assert cluster.platform_kubernetes["api_url"] == "http://newurl"
    await cluster.delete()
    assert len(await admin_project.clusters.list()) == 0

    # Group clusters
    await group1.clusters.create(
        {
            "name": "cluster1",
            "platform_kubernetes_attributes": {
                "api_url": "http://url",
                "token": "tokenval",
            },
        }
    )
    clusters = await group1.clusters.list()
    assert len(clusters) == 1
    cluster = clusters[0]
    cluster.platform_kubernetes_attributes = {"api_url": "http://newurl"}
    await cluster.save()
    cluster = (await group1.clusters.list())[0]
    assert cluster.platform_kubernetes["api_url"] == "http://newurl"
    await cluster.delete()
    assert len(await group1.clusters.list()) == 0

    # project events
    await admin_project.events.list()

    # forks
    fork = await admin_project.forks.create({"namespace": user1.username})
    p = await gl.projects.get(fork.id)
    assert p.forked_from_project["id"] == admin_project.id

    forks = await admin_project.forks.list()
    assert fork.id in map(lambda p: p.id, forks)

    # project hooks
    hook = await admin_project.hooks.create({"url": "http://hook.url"})
    assert len(await admin_project.hooks.list()) == 1
    hook.note_events = True
    await hook.save()
    hook = await admin_project.hooks.get(hook.id)
    assert hook.note_events is True
    await hook.delete()

    # deploy keys
    deploy_key = await admin_project.keys.create(
        {"title": "foo@bar", "key": DEPLOY_KEY}
    )
    project_keys = list(await admin_project.keys.list())
    assert len(project_keys) == 1

    await sudo_project.keys.enable(deploy_key.id)
    assert len(await sudo_project.keys.list()) == 1
    await sudo_project.keys.delete(deploy_key.id)
    assert len(await sudo_project.keys.list()) == 0

    # labels
    # label1 = admin_project.labels.create({"name": "label1", "color": "#778899"})
    # label1 = admin_project.labels.list()[0]
    # assert len(admin_project.labels.list()) == 1
    # label1.new_name = "label1updated"
    # label1.save()
    # assert label1.name == "label1updated"
    # label1.subscribe()
    # assert label1.subscribed == True
    # label1.unsubscribe()
    # assert label1.subscribed == False
    # label1.delete()

    # milestones
    m1 = await admin_project.milestones.create({"title": "milestone1"})
    assert len(await admin_project.milestones.list()) == 1
    m1.due_date = "2020-01-01T00:00:00Z"
    await m1.save()
    m1.state_event = "close"
    await m1.save()
    m1 = await admin_project.milestones.get(m1.id)
    assert m1.state == "closed"
    assert len(await m1.issues()) == 0
    assert len(await m1.merge_requests()) == 0

    # issues
    issue1 = await admin_project.issues.create(
        {"title": "my issue 1", "milestone_id": m1.id}
    )
    issue2 = await admin_project.issues.create({"title": "my issue 2"})
    issue3 = await admin_project.issues.create({"title": "my issue 3"})
    assert len(await admin_project.issues.list()) == 3
    issue3.state_event = "close"
    await issue3.save()
    assert len(await admin_project.issues.list(state="closed")) == 1
    assert len(await admin_project.issues.list(state="opened")) == 2
    assert len(await admin_project.issues.list(milestone="milestone1")) == 1
    assert (await (await m1.issues()).next()).title == "my issue 1"
    size = len(await issue1.notes.list())
    note = await issue1.notes.create({"body": "This is an issue note"})
    assert len(await issue1.notes.list()) == size + 1
    emoji = await note.awardemojis.create({"name": "tractor"})
    assert len(await note.awardemojis.list()) == 1
    await emoji.delete()
    assert len(await note.awardemojis.list()) == 0
    await note.delete()
    assert len(await issue1.notes.list()) == size
    assert isinstance(await issue1.user_agent_detail(), dict)

    assert (await issue1.user_agent_detail())["user_agent"]
    assert await issue1.participants()
    assert type(await issue1.closed_by()) == list
    assert type(await issue1.related_merge_requests()) == list

    # issues labels and events
    label2 = await admin_project.labels.create({"name": "label2", "color": "#aabbcc"})
    issue1.labels = ["label2"]
    await issue1.save()
    events = await issue1.resourcelabelevents.list()
    assert events
    event = await issue1.resourcelabelevents.get(events[0].id)
    assert event

    size = len(await issue1.discussions.list())
    discussion = await issue1.discussions.create({"body": "Discussion body"})
    assert len(await issue1.discussions.list()) == size + 1
    d_note = await discussion.notes.create({"body": "first note"})
    d_note_from_get = await discussion.notes.get(d_note.id)
    d_note_from_get.body = "updated body"
    await d_note_from_get.save()
    discussion = await issue1.discussions.get(discussion.id)
    assert discussion.attributes["notes"][-1]["body"] == "updated body"
    await d_note_from_get.delete()
    discussion = await issue1.discussions.get(discussion.id)
    assert len(discussion.attributes["notes"]) == 1

    # tags
    tag1 = await admin_project.tags.create({"tag_name": "v1.0", "ref": "master"})
    assert len(await admin_project.tags.list()) == 1
    await tag1.set_release_description("Description 1")
    await tag1.set_release_description("Description 2")
    assert tag1.release["description"] == "Description 2"
    await tag1.delete()

    # project snippet
    admin_project.snippets_enabled = True
    await admin_project.save()
    snippet = await admin_project.snippets.create(
        {
            "title": "snip1",
            "file_name": "foo.py",
            "content": "initial content",
            "visibility": gitlab.v4.objects.VISIBILITY_PRIVATE,
        }
    )

    assert (await snippet.user_agent_detail())["user_agent"]

    size = len(await snippet.discussions.list())
    discussion = await snippet.discussions.create({"body": "Discussion body"})
    assert len(await snippet.discussions.list()) == size + 1
    d_note = await discussion.notes.create({"body": "first note"})
    d_note_from_get = await discussion.notes.get(d_note.id)
    d_note_from_get.body = "updated body"
    await d_note_from_get.save()
    discussion = await snippet.discussions.get(discussion.id)
    assert discussion.attributes["notes"][-1]["body"] == "updated body"
    await d_note_from_get.delete()
    discussion = await snippet.discussions.get(discussion.id)
    assert len(discussion.attributes["notes"]) == 1

    snippet.file_name = "bar.py"
    await snippet.save()
    snippet = await admin_project.snippets.get(snippet.id)
    assert (await snippet.content()).decode() == "initial content"
    assert snippet.file_name == "bar.py"
    size = len(await admin_project.snippets.list())
    await snippet.delete()
    assert len(await admin_project.snippets.list()) == (size - 1)

    # triggers
    tr1 = await admin_project.triggers.create({"description": "trigger1"})
    assert len(await admin_project.triggers.list()) == 1
    await tr1.delete()

    # variables
    v1 = await admin_project.variables.create({"key": "key1", "value": "value1"})
    assert len(await admin_project.variables.list()) == 1
    v1.value = "new_value1"
    await v1.save()
    v1 = await admin_project.variables.get(v1.key)
    assert v1.value == "new_value1"
    await v1.delete()

    # branches and merges
    to_merge = await admin_project.branches.create(
        {"branch": "branch1", "ref": "master"}
    )
    await admin_project.files.create(
        {
            "file_path": "README2.rst",
            "branch": "branch1",
            "content": "Initial content",
            "commit_message": "New commit in new branch",
        }
    )
    mr = await admin_project.mergerequests.create(
        {"source_branch": "branch1", "target_branch": "master", "title": "MR readme2"}
    )

    # discussion
    size = len(await mr.discussions.list())
    discussion = await mr.discussions.create({"body": "Discussion body"})
    assert len(await mr.discussions.list()) == size + 1
    d_note = await discussion.notes.create({"body": "first note"})
    d_note_from_get = await discussion.notes.get(d_note.id)
    d_note_from_get.body = "updated body"
    await d_note_from_get.save()
    discussion = await mr.discussions.get(discussion.id)
    assert discussion.attributes["notes"][-1]["body"] == "updated body"
    await d_note_from_get.delete()
    discussion = await mr.discussions.get(discussion.id)
    assert len(discussion.attributes["notes"]) == 1

    # mr labels and events
    mr.labels = ["label2"]
    await mr.save()
    events = await mr.resourcelabelevents.list()
    assert events
    event = await mr.resourcelabelevents.get(events[0].id)
    assert event

    # rebasing
    assert await mr.rebase()

    # basic testing: only make sure that the methods exist
    await mr.commits()
    await mr.changes()
    assert await mr.participants()

    await mr.merge()
    await admin_project.branches.delete("branch1")

    try:
        await mr.merge()
    except gitlab.GitlabMRClosedError:
        pass

    # protected branches
    p_b = await admin_project.protectedbranches.create({"name": "*-stable"})
    assert p_b.name == "*-stable"
    p_b = await admin_project.protectedbranches.get("*-stable")
    # master is protected by default when a branch has been created
    assert len(await admin_project.protectedbranches.list()) == 2
    await admin_project.protectedbranches.delete("master")
    await p_b.delete()
    assert len(await admin_project.protectedbranches.list()) == 0

    # stars
    await admin_project.star()
    assert admin_project.star_count == 1
    await admin_project.unstar()
    assert admin_project.star_count == 0

    # project boards
    # boards = admin_project.boards.list()
    # assert(len(boards))
    # board = boards[0]
    # lists = board.lists.list()
    # begin_size = len(lists)
    # last_list = lists[-1]
    # last_list.position = 0
    # last_list.save()
    # last_list.delete()
    # lists = board.lists.list()
    # assert(len(lists) == begin_size - 1)

    # project badges
    badge_image = "http://example.com"
    badge_link = "http://example/img.svg"
    badge = await admin_project.badges.create(
        {"link_url": badge_link, "image_url": badge_image}
    )
    assert len(await admin_project.badges.list()) == 1
    badge.image_url = "http://another.example.com"
    await badge.save()
    badge = await admin_project.badges.get(badge.id)
    assert badge.image_url == "http://another.example.com"
    await badge.delete()
    assert len(await admin_project.badges.list()) == 0

    # project wiki
    wiki_content = "Wiki page content"
    wp = await admin_project.wikis.create(
        {"title": "wikipage", "content": wiki_content}
    )
    assert len(await admin_project.wikis.list()) == 1
    wp = await admin_project.wikis.get(wp.slug)
    assert wp.content == wiki_content
    # update and delete seem broken
    # wp.content = 'new content'
    # wp.save()
    # wp.delete()
    # assert(len(admin_project.wikis.list()) == 0)

    # namespaces
    ns = await gl.namespaces.list(all=True)
    assert len(ns) != 0
    ns = (await gl.namespaces.list(search="root", all=True))[0]
    assert ns.kind == "user"

    # features
    # Disabled as this fails with GitLab 11.11
    # feat = gl.features.set("foo", 30)
    # assert feat.name == "foo"
    # assert len(gl.features.list()) == 1
    # feat.delete()
    # assert len(gl.features.list()) == 0

    # broadcast messages
    msg = await gl.broadcastmessages.create({"message": "this is the message"})
    msg.color = "#444444"
    await msg.save()
    msg_id = msg.id
    msg = (await gl.broadcastmessages.list(all=True))[0]
    assert msg.color == "#444444"
    msg = await gl.broadcastmessages.get(msg_id)
    assert msg.color == "#444444"
    await msg.delete()
    assert len(await gl.broadcastmessages.list()) == 0

    # notification settings
    settings = await gl.notificationsettings.get()
    settings.level = gitlab.NOTIFICATION_LEVEL_WATCH
    await settings.save()
    settings = await gl.notificationsettings.get()
    assert settings.level == gitlab.NOTIFICATION_LEVEL_WATCH

    # services
    service = await admin_project.services.get("asana")
    service.api_key = "whatever"
    await service.save()
    service = await admin_project.services.get("asana")
    assert service.active == True
    await service.delete()
    service = await admin_project.services.get("asana")
    assert service.active == False

    # snippets
    snippets = await gl.snippets.list(all=True)
    assert len(snippets) == 0
    snippet = await gl.snippets.create(
        {"title": "snippet1", "file_name": "snippet1.py", "content": "import gitlab"}
    )
    snippet = await gl.snippets.get(snippet.id)
    snippet.title = "updated_title"
    await snippet.save()
    snippet = await gl.snippets.get(snippet.id)
    assert snippet.title == "updated_title"
    content = await snippet.content()
    assert content.decode() == "import gitlab"

    assert (await snippet.user_agent_detail())["user_agent"]

    await snippet.delete()
    snippets = await gl.snippets.list(all=True)
    assert len(snippets) == 0

    # user activities
    await gl.user_activities.list(query_parameters={"from": "2019-01-01"})

    # events
    await gl.events.list()

    # rate limit
    settings = await gl.settings.get()
    settings.throttle_authenticated_api_enabled = True
    settings.throttle_authenticated_api_requests_per_period = 1
    settings.throttle_authenticated_api_period_in_seconds = 3
    await settings.save()
    projects = list()
    for i in range(0, 20):
        projects.append(await gl.projects.create({"name": str(i) + "ok"}))

    error_message = None
    for i in range(20, 40):
        try:
            projects.append(
                await gl.projects.create(
                    {"name": str(i) + "shouldfail"}, obey_rate_limit=False
                )
            )
        except gitlab.GitlabCreateError as e:
            error_message = e.error_message
            break
    assert "Retry later" in error_message
    settings.throttle_authenticated_api_enabled = False
    await settings.save()
    [await current_project.delete() for current_project in projects]

    # project import/export
    ex = await admin_project.exports.create({})
    await ex.refresh()
    count = 0
    while ex.export_status != "finished":
        await asyncio.sleep(1)
        await ex.refresh()
        count += 1
        if count == 10:
            raise Exception("Project export taking too much time")
    with open("/tmp/gitlab-export.tgz", "wb") as f:
        await ex.download(streamed=True, action=f.write)

    output = await gl.projects.import_project(
        open("/tmp/gitlab-export.tgz", "rb"), "imported_project"
    )
    project_import = await (
        await gl.projects.get(output["id"], lazy=True)
    ).imports.get()
    count = 0
    while project_import.import_status != "finished":
        await asyncio.sleep(1)
        await project_import.refresh()
        count += 1
        if count == 10:
            raise Exception("Project import taking too much time")

    # project releases
    release_test_project = await gl.projects.create(
        {"name": "release-test-project", "initialize_with_readme": True}
    )
    release_name = "Demo Release"
    release_tag_name = "v1.2.3"
    release_description = "release notes go here"
    await release_test_project.releases.create(
        {
            "name": release_name,
            "tag_name": release_tag_name,
            "description": release_description,
            "ref": "master",
        }
    )
    assert len(await release_test_project.releases.list()) == 1

    # get single release
    retrieved_project = await release_test_project.releases.get(release_tag_name)
    assert retrieved_project.name == release_name
    assert retrieved_project.tag_name == release_tag_name
    assert retrieved_project.description == release_description

    # delete release
    await release_test_project.releases.delete(release_tag_name)
    assert len(await release_test_project.releases.list()) == 0
    await release_test_project.delete()

    # status
    message = "Test"
    emoji = "thumbsup"
    status = await gl.user.status.get()
    status.message = message
    status.emoji = emoji
    await status.save()
    new_status = await gl.user.status.get()
    assert new_status.message == message
    assert new_status.emoji == emoji


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
