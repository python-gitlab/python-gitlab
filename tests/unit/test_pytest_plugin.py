"""Tests for the pytest-gitlab plugin."""

from importlib.metadata import entry_points

import pytest


@pytest.mark.skip(reason="pytest-gitlab plugin is disabled in tox")
def test_gitlab_plugin_is_loaded(request):
    """'gitlab' is a loaded pytest plugin."""
    assert request.config.pluginmanager.hasplugin("gitlab")


def test_gitlab_plugin_is_registered():
    """'gitlab' is registered as a pytest11 entry point."""
    pytest11_entry_points = entry_points(group="pytest11")
    assert any(ep.value == "gitlab.testing.plugin" for ep in pytest11_entry_points)
