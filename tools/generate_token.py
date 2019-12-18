#!/usr/bin/env python

from urllib.parse import urljoin
from requests_html import HTMLSession

ENDPOINT = "http://localhost:8080"
LOGIN = "root"
PASSWORD = "5iveL!fe"


class GitlabSession(HTMLSession):
    def __init__(self, endpoint, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.endpoint = endpoint
        self.csrf = None

    def find_csrf_token(self, html):
        param = html.find("meta[name=csrf-param]")[0].attrs["content"]
        token = html.find("meta[name=csrf-token]")[0].attrs["content"]
        self.csrf = {param: token}

    def obtain_csrf_token(self):
        r = self.get(urljoin(self.endpoint, "/"))
        self.find_csrf_token(r.html)

    def sign_in(self, login, password):
        data = {"user[login]": login, "user[password]": password, **self.csrf}
        r = self.post(urljoin(self.endpoint, "/users/sign_in"), data=data)
        self.find_csrf_token(r.html)

    def obtain_personal_access_token(self, name):
        data = {
            "personal_access_token[name]": name,
            "personal_access_token[scopes][]": ["api", "sudo"],
            **self.csrf,
        }
        r = self.post(
            urljoin(self.endpoint, "/profile/personal_access_tokens"), data=data
        )
        return r.html.find("#created-personal-access-token")[0].attrs["value"]


def main():
    with GitlabSession(ENDPOINT) as s:
        s.obtain_csrf_token()
        s.sign_in(LOGIN, PASSWORD)
        print(s.obtain_personal_access_token("default"))


if __name__ == "__main__":
    main()
