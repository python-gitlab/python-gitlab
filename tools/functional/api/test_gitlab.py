"""
Temporary module to run legacy tests as a single pytest test case
as they're all plain asserts at module level.
"""


def test_api_v4(gl):
    from tools.functional import python_test_v4
