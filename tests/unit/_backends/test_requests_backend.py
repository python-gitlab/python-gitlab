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
    def test_prepare_send_data_str_parentid(self) -> None:
        file = "12345"
        files = {"file": ("file.tar.gz", file, "application/octet-stream")}
        post_data = {"parent_id": "12"}

        result = requests_backend.RequestsBackend.prepare_send_data(
            files=files, post_data=post_data, raw=False
        )
        assert result.json is None
        assert result.content_type.startswith("multipart/form-data")
        assert isinstance(result.data, MultipartEncoder)
