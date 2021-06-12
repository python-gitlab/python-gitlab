import inspect
from typing import Dict

import gitlab
import gitlab.v4.objects


def test_managers_annotated():
    """Ensure _managers have been type annotated"""

    failed_messages = []
    for module_name, module_value in inspect.getmembers(gitlab.v4.objects):
        if not inspect.ismodule(module_value):
            # We only care about the modules
            continue
        # Iterate through all the classes in our module
        for class_name, class_value in sorted(inspect.getmembers(module_value)):
            if not inspect.isclass(class_value):
                continue

            # Ignore imported classes from gitlab.base
            if class_value.__module__ == "gitlab.base":
                continue

            # A '_managers' attribute is only on a RESTObject
            if not issubclass(class_value, gitlab.base.RESTObject):
                continue

            if class_value._managers is None:
                continue

            # Collect all of our annotations into a Dict[str, str]
            annotations: Dict[str, str] = {}
            for attr, annotation in sorted(class_value.__annotations__.items()):
                if isinstance(annotation, type):
                    type_name = annotation.__name__
                else:
                    type_name = annotation
                annotations[attr] = type_name

            for attr, manager_class_name in sorted(class_value._managers):
                # All of our managers need to end with "Manager" for example
                # "ProjectManager"
                if not manager_class_name.endswith("Manager"):
                    failed_messages.append(
                        (
                            f"ERROR: Class: {class_name!r} for '_managers' attribute "
                            f"{attr!r} The specified manager class "
                            f"{manager_class_name!r} does not have a name ending in "
                            f"'Manager'. Manager class names are required to end in "
                            f"'Manager'"
                        )
                    )
                    continue
                if attr not in annotations:
                    failed_messages.append(
                        (
                            f"ERROR: Class: {class_name!r}: Type annotation missing "
                            f"for '_managers' attribute {attr!r}"
                        )
                    )
                    continue
                if manager_class_name != annotations[attr]:
                    failed_messages.append(
                        (
                            f"ERROR: Class: {class_name!r}: Type annotation mismatch "
                            f"for '_managers' attribute {attr!r}. Type annotation is "
                            f"{annotations[attr]!r} while '_managers' is "
                            f"{manager_class_name!r}"
                        )
                    )

    failed_msg = "\n".join(failed_messages)
    assert not failed_messages, failed_msg
