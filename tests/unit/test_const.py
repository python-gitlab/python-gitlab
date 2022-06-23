from gitlab import const


def test_access_level():
    assert 50 == const.AccessLevel.OWNER
    assert "OWNER" == const.AccessLevel(50)
