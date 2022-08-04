from gitlab.mixins import (
    AccessRequestMixin,
    SetMixin,
    SubscribableMixin,
    TimeTrackingMixin,
    TodoMixin,
    UserAgentDetailMixin,
)


def test_access_request_mixin():
    class TestClass(AccessRequestMixin):
        pass

    obj = TestClass()
    assert hasattr(obj, "approve")


def test_subscribable_mixin():
    class TestClass(SubscribableMixin):
        pass

    obj = TestClass()
    assert hasattr(obj, "subscribe")
    assert hasattr(obj, "unsubscribe")


def test_todo_mixin():
    class TestClass(TodoMixin):
        pass

    obj = TestClass()
    assert hasattr(obj, "todo")


def test_time_tracking_mixin():
    class TestClass(TimeTrackingMixin):
        pass

    obj = TestClass()
    assert hasattr(obj, "time_stats")
    assert hasattr(obj, "time_estimate")
    assert hasattr(obj, "reset_time_estimate")
    assert hasattr(obj, "add_spent_time")
    assert hasattr(obj, "reset_spent_time")


def test_set_mixin():
    class TestClass(SetMixin):
        pass

    obj = TestClass()
    assert hasattr(obj, "set")


def test_user_agent_detail_mixin():
    class TestClass(UserAgentDetailMixin):
        pass

    obj = TestClass()
    assert hasattr(obj, "user_agent_detail")
