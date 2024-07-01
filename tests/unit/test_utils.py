import json
import logging
import warnings

import pytest
import requests
import responses

from gitlab import types, utils


@pytest.mark.parametrize(
    "content_type,expected_type",
    [
        ("application/json", "application/json"),
        ("application/json; charset=utf-8", "application/json"),
        ("", "text/plain"),
        (None, "text/plain"),
    ],
)
def test_get_content_type(content_type, expected_type):
    parsed_type = utils.get_content_type(content_type)
    assert parsed_type == expected_type


@responses.activate
def test_response_content(capsys):
    responses.add(
        method="GET",
        url="https://example.com",
        status=200,
        body="test",
        content_type="application/octet-stream",
    )

    resp = requests.get("https://example.com", stream=True)
    utils.response_content(
        resp, streamed=True, action=None, chunk_size=1024, iterator=False
    )

    captured = capsys.readouterr()
    assert "test" in captured.out


class TestEncodedId:
    def test_init_str(self):
        obj = utils.EncodedId("Hello")
        assert "Hello" == obj
        assert "Hello" == str(obj)
        assert "Hello" == f"{obj}"
        assert isinstance(obj, utils.EncodedId)

        obj = utils.EncodedId("this/is a/path")
        assert "this%2Fis%20a%2Fpath" == str(obj)
        assert "this%2Fis%20a%2Fpath" == f"{obj}"
        assert isinstance(obj, utils.EncodedId)

    def test_init_int(self):
        obj = utils.EncodedId(23)
        assert "23" == obj
        assert "23" == f"{obj}"
        assert isinstance(obj, utils.EncodedId)

    def test_init_invalid_type_raises(self):
        with pytest.raises(TypeError):
            utils.EncodedId(None)

    def test_init_encodeid_str(self):
        value = "Goodbye"
        obj_init = utils.EncodedId(value)
        obj = utils.EncodedId(obj_init)
        assert value == str(obj)
        assert value == f"{obj}"

        value = "we got/a/path"
        expected = "we%20got%2Fa%2Fpath"
        obj_init = utils.EncodedId(value)
        assert expected == str(obj_init)
        assert expected == f"{obj_init}"
        # Show that no matter how many times we recursively call it we still only
        # URL-encode it once.
        obj = utils.EncodedId(
            utils.EncodedId(utils.EncodedId(utils.EncodedId(utils.EncodedId(obj_init))))
        )
        assert expected == str(obj)
        assert expected == f"{obj}"

        # Show assignments still only encode once
        obj2 = obj
        assert expected == str(obj2)
        assert expected == f"{obj2}"

    def test_init_encodeid_int(self):
        value = 23
        expected = f"{value}"
        obj_init = utils.EncodedId(value)
        obj = utils.EncodedId(obj_init)
        assert expected == str(obj)
        assert expected == f"{obj}"

    def test_json_serializable(self):
        obj = utils.EncodedId("someone")
        assert '"someone"' == json.dumps(obj)

        obj = utils.EncodedId("we got/a/path")
        assert '"we%20got%2Fa%2Fpath"' == json.dumps(obj)


class TestWarningsWrapper:
    def test_warn(self):
        warn_message = "short and stout"
        warn_source = "teapot"

        with warnings.catch_warnings(record=True) as caught_warnings:
            utils.warn(message=warn_message, category=UserWarning, source=warn_source)
        assert len(caught_warnings) == 1
        warning = caught_warnings[0]
        # File name is this file as it is the first file outside of the `gitlab/` path.
        assert __file__ == warning.filename
        assert warning.category == UserWarning
        assert isinstance(warning.message, UserWarning)
        assert warn_message in str(warning.message)
        assert __file__ in str(warning.message)
        assert warn_source == warning.source

    def test_warn_no_show_caller(self):
        warn_message = "short and stout"
        warn_source = "teapot"

        with warnings.catch_warnings(record=True) as caught_warnings:
            utils.warn(
                message=warn_message,
                category=UserWarning,
                source=warn_source,
                show_caller=False,
            )
        assert len(caught_warnings) == 1
        warning = caught_warnings[0]
        # File name is this file as it is the first file outside of the `gitlab/` path.
        assert __file__ == warning.filename
        assert warning.category == UserWarning
        assert isinstance(warning.message, UserWarning)
        assert warn_message in str(warning.message)
        assert __file__ not in str(warning.message)
        assert warn_source == warning.source


@pytest.mark.parametrize(
    "source,expected",
    [
        ({"a": "", "b": "spam", "c": None}, {"a": "", "b": "spam", "c": None}),
        ({"a": "", "b": {"c": "spam"}}, {"a": "", "b[c]": "spam"}),
    ],
)
def test_copy_dict(source, expected):
    dest = {}

    utils.copy_dict(src=source, dest=dest)
    assert dest == expected


@pytest.mark.parametrize(
    "dictionary,expected",
    [
        ({"a": None, "b": "spam"}, {"b": "spam"}),
        ({"a": "", "b": "spam"}, {"a": "", "b": "spam"}),
        ({"a": None, "b": None}, {}),
    ],
)
def test_remove_none_from_dict(dictionary, expected):
    result = utils.remove_none_from_dict(dictionary)
    assert result == expected


def test_transform_types_copies_data_with_empty_files():
    data = {"attr": "spam"}
    new_data, files = utils._transform_types(data, {}, transform_data=True)

    assert new_data is not data
    assert new_data == data
    assert files == {}


def test_transform_types_with_transform_files_populates_files():
    custom_types = {"attr": types.FileAttribute}
    data = {"attr": "spam"}
    new_data, files = utils._transform_types(data, custom_types, transform_data=True)

    assert new_data == {}
    assert files["attr"] == ("attr", "spam")


def test_transform_types_without_transform_files_populates_data_with_empty_files():
    custom_types = {"attr": types.FileAttribute}
    data = {"attr": "spam"}
    new_data, files = utils._transform_types(
        data, custom_types, transform_files=False, transform_data=True
    )

    assert new_data == {"attr": "spam"}
    assert files == {}


def test_transform_types_params_array():
    data = {"attr": [1, 2, 3]}
    custom_types = {"attr": types.ArrayAttribute}
    new_data, files = utils._transform_types(data, custom_types, transform_data=True)

    assert new_data is not data
    assert new_data == {"attr[]": [1, 2, 3]}
    assert files == {}


def test_transform_types_not_params_array():
    data = {"attr": [1, 2, 3]}
    custom_types = {"attr": types.ArrayAttribute}
    new_data, files = utils._transform_types(data, custom_types, transform_data=False)

    assert new_data is not data
    assert new_data == data
    assert files == {}


def test_masking_formatter_masks_token(capsys: pytest.CaptureFixture):
    token = "glpat-private-token"

    logger = logging.getLogger()
    handler = logging.StreamHandler()
    handler.setFormatter(utils.MaskingFormatter(masked=token))
    logger.handlers.clear()
    logger.addHandler(handler)

    logger.info(token)
    captured = capsys.readouterr()

    assert "[MASKED]" in captured.err
    assert token not in captured.err
