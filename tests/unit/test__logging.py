import logging

import pytest

from gitlab import _logging


@pytest.fixture
def LOG():
    return logging.getLogger(_logging._module_root_logger_name)


def test_module_root_logger_name():
    assert _logging._module_root_logger_name == "gitlab"


def test_module_name(LOG):
    assert LOG.name == "gitlab"


def test_logger_null_handler(LOG):
    assert len(LOG.handlers) == 1
    handler = LOG.handlers[0]
    assert isinstance(handler, logging.NullHandler)
