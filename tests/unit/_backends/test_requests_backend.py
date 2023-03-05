import pytest
from requests_toolbelt.multipart.encoder import MultipartEncoder  # type: ignore

from gitlab._backends import requests_backend


class TestSendData:
    def test_senddata_json(self) -> None:
        result = requests_backend.SendData(
            json={"a": 1}, content_type="application/json"
        )
        assert result.data is None

    def test_senddata_data(self) -> None:
        result = requests_backend.SendData(
            data={"b": 2}, content_type="application/octet-stream"
        )
        assert result.json is None

    def test_senddata_json_and_data(self) -> None:
        with pytest.raises(ValueError, match=r"json={'a': 1}  data={'b': 2}"):
            requests_backend.SendData(
                json={"a": 1}, data={"b": 2}, content_type="application/json"
            )


class TestRequestsBackend:
    @pytest.mark.parametrize(
        "test_data,expected",
        [
            (False, "0"),
            (True, "1"),
            ("12", "12"),
            (12, "12"),
            (12.0, "12.0"),
            (complex(-2, 7), "(-2+7j)"),
        ],
    )
    def test_prepare_send_data_non_strings(self, test_data, expected) -> None:
        assert isinstance(expected, str)
        files = {"file": ("file.tar.gz", "12345", "application/octet-stream")}
        post_data = {"test_data": test_data}

        result = requests_backend.RequestsBackend.prepare_send_data(
            files=files, post_data=post_data, raw=False
        )
        assert result.json is None
        assert result.content_type.startswith("multipart/form-data")
        assert isinstance(result.data, MultipartEncoder)
        assert isinstance(result.data.fields["test_data"], str)
        assert result.data.fields["test_data"] == expected
