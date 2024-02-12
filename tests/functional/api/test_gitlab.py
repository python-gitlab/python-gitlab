import pytest
import requests

import gitlab


@pytest.fixture(
    scope="session",
    params=[{"get_all": True}, {"all": True}],
    ids=["get_all=True", "all=True"],
)
def get_all_kwargs(request):
    """A tiny parametrized fixture to inject both `get_all=True` and
    `all=True` to ensure they behave the same way for pagination."""
    return request.param


def test_auth_from_config(gl, gitlab_config, temp_dir):
    """Test token authentication from config file"""
    test_gitlab = gitlab.Gitlab.from_config(config_files=[gitlab_config])
    test_gitlab.auth()
    assert isinstance(test_gitlab.user, gitlab.v4.objects.CurrentUser)


def test_no_custom_session(gl, temp_dir):
    """Test no custom session"""
    custom_session = requests.Session()
    test_gitlab = gitlab.Gitlab.from_config(
        config_files=[temp_dir / "python-gitlab.cfg"]
    )
    assert test_gitlab.session != custom_session


def test_custom_session(gl, temp_dir):
    """Test custom session"""
    custom_session = requests.Session()
    test_gitlab = gitlab.Gitlab.from_config(
        config_files=[temp_dir / "python-gitlab.cfg"], session=custom_session
    )
    assert test_gitlab.session == custom_session


def test_broadcast_messages(gl, get_all_kwargs):
    msg = gl.broadcastmessages.create({"message": "this is the message"})
    msg.color = "#444444"
    msg.save()
    msg_id = msg.id

    msg = gl.broadcastmessages.list(**get_all_kwargs)[0]
    assert msg.color == "#444444"

    msg = gl.broadcastmessages.get(msg_id)
    assert msg.color == "#444444"

    msg.delete()


def test_markdown(gl):
    html = gl.markdown("foo")
    assert "foo" in html


def test_markdown_in_project(gl, project):
    html = gl.markdown("foo", project=project.path_with_namespace)
    assert "foo" in html


def test_sidekiq_queue_metrics(gl):
    out = gl.sidekiq.queue_metrics()
    assert isinstance(out, dict)
    assert "default" in out["queues"]


def test_sidekiq_process_metrics(gl):
    out = gl.sidekiq.process_metrics()
    assert isinstance(out, dict)
    assert "hostname" in out["processes"][0]


def test_sidekiq_job_stats(gl):
    out = gl.sidekiq.job_stats()
    assert isinstance(out, dict)
    assert "processed" in out["jobs"]


def test_sidekiq_compound_metrics(gl):
    out = gl.sidekiq.compound_metrics()
    assert isinstance(out, dict)
    assert "jobs" in out
    assert "processes" in out
    assert "queues" in out


@pytest.mark.gitlab_premium
def test_geo_nodes(gl):
    # Very basic geo nodes tests because we only have 1 node.
    nodes = gl.geonodes.list()
    assert isinstance(nodes, list)

    status = gl.geonodes.status()
    assert isinstance(status, list)


@pytest.mark.gitlab_premium
def test_gitlab_license(gl):
    license = gl.get_license()
    assert "user_limit" in license

    with pytest.raises(gitlab.GitlabLicenseError, match="The license key is invalid."):
        gl.set_license("dummy key")


def test_gitlab_settings(gl):
    settings = gl.settings.get()
    settings.default_projects_limit = 42
    settings.save()
    settings = gl.settings.get()
    assert settings.default_projects_limit == 42


def test_template_dockerfile(gl):
    assert gl.dockerfiles.list()

    dockerfile = gl.dockerfiles.get("Node")
    assert dockerfile.content is not None


def test_template_gitignore(gl, get_all_kwargs):
    assert gl.gitignores.list(**get_all_kwargs)
    gitignore = gl.gitignores.get("Node")
    assert gitignore.content is not None


def test_template_gitlabciyml(gl, get_all_kwargs):
    assert gl.gitlabciymls.list(**get_all_kwargs)
    gitlabciyml = gl.gitlabciymls.get("Nodejs")
    assert gitlabciyml.content is not None


def test_template_license(gl):
    assert gl.licenses.list()
    license = gl.licenses.get(
        "bsd-2-clause", project="mytestproject", fullname="mytestfullname"
    )
    assert "mytestfullname" in license.content


def test_hooks(gl):
    hook = gl.hooks.create({"url": "http://whatever.com"})
    assert hook in gl.hooks.list()

    hook.delete()


def test_namespaces(gl, get_all_kwargs):
    gl.auth()
    current_user = gl.user.username

    namespaces = gl.namespaces.list(**get_all_kwargs)
    assert namespaces

    namespaces = gl.namespaces.list(search=current_user, **get_all_kwargs)
    assert namespaces[0].kind == "user"

    namespace = gl.namespaces.get(current_user)
    assert namespace.kind == "user"

    namespace = gl.namespaces.exists(current_user)
    assert namespace.exists


def test_notification_settings(gl):
    settings = gl.notificationsettings.get()
    settings.level = gitlab.const.NotificationLevel.WATCH
    settings.save()

    settings = gl.notificationsettings.get()
    assert settings.level == gitlab.const.NotificationLevel.WATCH


def test_search(gl):
    result = gl.search(scope=gitlab.const.SearchScope.USERS, search="Administrator")
    assert result[0]["id"] == 1


def test_user_activities(gl):
    activities = gl.user_activities.list(query_parameters={"from": "2019-01-01"})
    assert isinstance(activities, list)


def test_events(gl):
    events = gl.events.list()
    assert isinstance(events, list)


@pytest.mark.skip
def test_features(gl):
    feat = gl.features.set("foo", 30)
    assert feat.name == "foo"
    assert feat in gl.features.list()

    feat.delete()


def test_pagination(gl, project):
    project2 = gl.projects.create({"name": "project-page-2"})

    list1 = gl.projects.list(per_page=1, page=1)
    list2 = gl.projects.list(per_page=1, page=2)
    assert len(list1) == 1
    assert len(list2) == 1
    assert list1[0].id != list2[0].id

    project2.delete()


def test_rate_limits(gl):
    settings = gl.settings.get()
    settings.throttle_authenticated_api_enabled = True
    settings.throttle_authenticated_api_requests_per_period = 1
    settings.throttle_authenticated_api_period_in_seconds = 3
    settings.save()

    projects = []
    for i in range(0, 20):
        projects.append(gl.projects.create({"name": f"{str(i)}ok"}))

    with pytest.raises(gitlab.GitlabCreateError) as e:
        for i in range(20, 40):
            projects.append(
                gl.projects.create(
                    {"name": f"{str(i)}shouldfail"}, obey_rate_limit=False
                )
            )

    assert "Retry later" in str(e.value)

    settings.throttle_authenticated_api_enabled = False
    settings.save()
    [project.delete() for project in projects]


def test_list_default_warning(gl):
    """When there are more than 20 items and use default `list()` then warning is
    generated"""
    with pytest.warns(UserWarning, match="python-gitlab.readthedocs.io") as record:
        gl.gitlabciymls.list()

    assert len(record) == 1
    warning = record[0]
    assert __file__ == warning.filename
    assert __file__ in str(warning.message)


def test_list_page_nowarning(gl, recwarn):
    """Using `page=X` will disable the warning"""
    gl.gitlabciymls.list(page=1)
    assert not recwarn


def test_list_all_false_nowarning(gl, recwarn):
    """Using `all=False` will disable the warning"""
    gl.gitlabciymls.list(all=False)
    assert not recwarn


def test_list_all_true_nowarning(gl, get_all_kwargs, recwarn):
    """Using `get_all=True` will disable the warning"""
    items = gl.gitlabciymls.list(**get_all_kwargs)
    for warn in recwarn:
        if issubclass(warn.category, UserWarning):
            # Our warning has a link to the docs in it, make sure we don't have
            # that.
            assert "python-gitlab.readthedocs.io" not in str(warn.message)
    assert len(items) > 20


def test_list_iterator_true_nowarning(gl, recwarn):
    """Using `iterator=True` will disable the warning"""
    items = gl.gitlabciymls.list(iterator=True)
    assert not recwarn
    assert len(list(items)) > 20
