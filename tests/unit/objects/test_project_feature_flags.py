"""
Unit tests for Project Feature Flags.
"""

import responses

from gitlab.v4.objects import ProjectFeatureFlag


def test_feature_flag_rename(project):
    """
    Verify that renaming a feature flag uses the old name in the URL
    and the new name in the payload.
    """
    flag_content = {"name": "old_name", "version": "new_version_flag", "active": True}
    flag = ProjectFeatureFlag(project.feature_flags, flag_content)

    # Simulate fetching from API (populates _attrs)
    flag._attrs = flag_content.copy()
    flag._updated_attrs = {}

    # Rename locally
    flag.name = "new_name"

    with responses.RequestsMock() as rs:
        rs.add(
            responses.PUT,
            "http://localhost/api/v4/projects/1/feature_flags/old_name",
            json={"name": "new_name", "version": "new_version_flag", "active": True},
            status=200,
        )

        flag.save()

        assert len(rs.calls) == 1
        # URL should use the old name (ID)
        assert rs.calls[0].request.url.endswith("/feature_flags/old_name")
        # Body should contain the new name
        assert b'"name": "new_name"' in rs.calls[0].request.body
        assert flag.name == "new_name"
