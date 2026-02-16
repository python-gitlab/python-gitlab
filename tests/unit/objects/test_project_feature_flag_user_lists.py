"""
Unit tests for Project Feature Flag User Lists.
"""

import responses


def test_create_user_list_with_list_conversion(project):
    """
    Verify that passing a list of integers for user_xids is converted
    to a comma-separated string in the API payload.
    """
    with responses.RequestsMock() as rs:
        rs.add(
            responses.POST,
            "http://localhost/api/v4/projects/1/feature_flags_user_lists",
            json={"iid": 1, "name": "list", "user_xids": "1,2,3"},
            status=201,
            match=[
                responses.matchers.json_params_matcher(
                    {"name": "list", "user_xids": "1,2,3"}
                )
            ],
        )

        project.feature_flags_user_lists.create(
            {"name": "list", "user_xids": [1, 2, 3]}
        )

        assert len(rs.calls) == 1
