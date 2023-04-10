import datetime
import io
import json
from typing import Optional

import requests
import responses

from gitlab import base

MATCH_EMPTY_QUERY_PARAMS = [responses.matchers.query_param_matcher({})]


class FakeObject(base.RESTObject):
    pass


class FakeObjectWithoutId(base.RESTObject):
    _id_attr = None


class FakeObjectWithLongRepr(base.RESTObject):
    _id_attr = None
    _repr_attr = "test"


class OtherFakeObject(FakeObject):
    _id_attr = "foo"


class FakeManager(base.RESTManager):
    _path = "/tests"
    _obj_cls = FakeObject


class FakeParent(FakeObject):
    id = 42


class FakeManagerWithParent(base.RESTManager):
    _path = "/tests/{test_id}/cases"
    _obj_cls = FakeObject
    _from_parent_attrs = {"test_id": "id"}


# NOTE: The function `httmock_response` and the class `Headers` is taken from
# https://github.com/patrys/httmock/ which is licensed under the Apache License, Version
# 2.0. Thus it is allowed to be used in this project.
# https://www.apache.org/licenses/GPL-compatibility.html
class Headers(object):
    def __init__(self, res):
        self.headers = res.headers

    def get_all(self, name, failobj=None):
        return self.getheaders(name)

    def getheaders(self, name):
        return [self.headers.get(name)]


def httmock_response(
    status_code: int = 200,
    content: str = "",
    headers=None,
    reason=None,
    elapsed=0,
    request: Optional[requests.models.PreparedRequest] = None,
    stream: bool = False,
    http_vsn=11,
) -> requests.models.Response:
    res = requests.Response()
    res.status_code = status_code
    if isinstance(content, (dict, list)):
        content = json.dumps(content).encode("utf-8")
    if isinstance(content, str):
        content = content.encode("utf-8")
    res._content = content
    res._content_consumed = content
    res.headers = requests.structures.CaseInsensitiveDict(headers or {})
    res.encoding = requests.utils.get_encoding_from_headers(res.headers)
    res.reason = reason
    res.elapsed = datetime.timedelta(elapsed)
    res.request = request
    if hasattr(request, "url"):
        res.url = request.url
        if isinstance(request.url, bytes):
            res.url = request.url.decode("utf-8")
    if "set-cookie" in res.headers:
        res.cookies.extract_cookies(
            requests.cookies.MockResponse(Headers(res)),
            requests.cookies.MockRequest(request),
        )
    if stream:
        res.raw = io.BytesIO(content)
    else:
        res.raw = io.BytesIO(b"")
    res.raw.version = http_vsn

    # normally this closes the underlying connection,
    #  but we have nothing to free.
    res.close = lambda *args, **kwargs: None

    return res
