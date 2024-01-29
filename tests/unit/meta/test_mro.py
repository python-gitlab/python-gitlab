"""
Ensure objects defined in gitlab.v4.objects have REST* as last item in class
definition

Original notes by John L. Villalovos

An example of an incorrect definition:
    class ProjectPipeline(RESTObject, RefreshMixin, ObjectDeleteMixin):
                          ^^^^^^^^^^ This should be at the end.

Correct way would be:
    class ProjectPipeline(RefreshMixin, ObjectDeleteMixin, RESTObject):
                                      Correctly at the end ^^^^^^^^^^


Why this is an issue:

  When we do type-checking for gitlab/mixins.py we make RESTObject or
  RESTManager the base class for the mixins

  Here is how our classes look when type-checking:

      class RESTObject:
          def __init__(self, manager: "RESTManager", attrs: Dict[str, Any]) -> None:
              ...

      class Mixin(RESTObject):
          ...

      # Wrong ordering here
      class Wrongv4Object(RESTObject, RefreshMixin):
          ...

  If we actually ran this in Python we would get the following error:
         class Wrongv4Object(RESTObject, Mixin):
    TypeError: Cannot create a consistent method resolution
    order (MRO) for bases RESTObject, Mixin

  When we are type-checking it fails to understand the class Wrongv4Object
  and thus we can't type check it correctly.

Almost all classes in gitlab/v4/objects/*py were already correct before this
check was added.
"""

import inspect

import pytest

import gitlab.v4.objects


def test_show_issue() -> None:
    """Test case to demonstrate the TypeError that occurs"""

    class RESTObject:
        def __init__(self, manager: str, attrs: int) -> None: ...

    class Mixin(RESTObject): ...

    with pytest.raises(TypeError) as exc_info:
        # Wrong ordering here
        class Wrongv4Object(RESTObject, Mixin):  # type: ignore
            ...

    # The error message in the exception should be:
    #   TypeError: Cannot create a consistent method resolution
    #   order (MRO) for bases RESTObject, Mixin

    # Make sure the exception string contains "MRO"
    assert "MRO" in exc_info.exconly()

    # Correctly ordered class, no exception
    class Correctv4Object(Mixin, RESTObject): ...


def test_mros() -> None:
    """Ensure objects defined in gitlab.v4.objects have REST* as last item in
    class definition.

    We do this as we need to ensure the MRO (Method Resolution Order) is
    correct.
    """

    failed_messages = []
    for module_name, module_value in inspect.getmembers(gitlab.v4.objects):
        if not inspect.ismodule(module_value):
            # We only care about the modules
            continue
        # Iterate through all the classes in our module
        for class_name, class_value in inspect.getmembers(module_value):
            if not inspect.isclass(class_value):
                continue

            # Ignore imported classes from gitlab.base
            if class_value.__module__ == "gitlab.base":
                continue

            mro = class_value.mro()

            # We only check classes which have a 'gitlab.base' class in their MRO
            has_base = False
            for count, obj in enumerate(mro, start=1):
                if obj.__module__ == "gitlab.base":
                    has_base = True
                    base_classname = obj.__name__
            if has_base:
                filename = inspect.getfile(class_value)
                # NOTE(jlvillal): The very last item 'mro[-1]' is always going
                # to be 'object'. That is why we are checking 'mro[-2]'.
                if mro[-2].__module__ != "gitlab.base":
                    failed_messages.append(
                        (
                            f"class definition for {class_name!r} in file {filename!r} "
                            f"must have {base_classname!r} as the last class in the "
                            f"class definition"
                        )
                    )
    failed_msg = "\n".join(failed_messages)
    assert not failed_messages, failed_msg
