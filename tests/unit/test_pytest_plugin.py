"""Tests for the gitlab pytest plugin."""


def test_gitlab_plugin_is_registered(request):
    """'gitlab' is a registered pytest plugin."""
    assert request.config.pluginmanager.hasplugin("gitlab")
