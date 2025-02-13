"""
GitLab API:
https://docs.gitlab.com/ee/api/member_roles.html
"""


def test_instance_member_role(gl):
    member_role = gl.member_roles.create(
        {
            "name": "Custom webhook manager role",
            "base_access_level": 20,
            "description": "Custom reporter that can manage webhooks",
            "admin_web_hook": True,
        }
    )
    assert member_role.id > 0
    assert member_role in gl.member_roles.list()
    gl.member_roles.delete(member_role.id)
