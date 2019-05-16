#!/usr/bin/env python

import sys

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

from bs4 import BeautifulSoup
import requests

endpoint = "http://localhost:8080"
root_route = urljoin(endpoint, "/")
sign_in_route = urljoin(endpoint, "/users/sign_in")
pat_route = urljoin(endpoint, "/profile/personal_access_tokens")

login = "root"
password = "5iveL!fe"


def find_csrf_token(text):
    soup = BeautifulSoup(text, "lxml")
    token = soup.find(attrs={"name": "csrf-token"})
    param = soup.find(attrs={"name": "csrf-param"})
    data = {param.get("content"): token.get("content")}
    return data


def obtain_csrf_token():
    r = requests.get(root_route)
    token = find_csrf_token(r.text)
    return token, r.cookies


def sign_in(csrf, cookies):
    data = {"user[login]": login, "user[password]": password}
    data.update(csrf)
    r = requests.post(sign_in_route, data=data, cookies=cookies)
    token = find_csrf_token(r.text)
    return token, r.history[0].cookies


def obtain_personal_access_token(name, csrf, cookies):
    data = {
        "personal_access_token[name]": name,
        "personal_access_token[scopes][]": ["api", "sudo"],
    }
    data.update(csrf)
    r = requests.post(pat_route, data=data, cookies=cookies)
    soup = BeautifulSoup(r.text, "lxml")
    token = soup.find("input", id="created-personal-access-token").get("value")
    return token


def main():
    csrf1, cookies1 = obtain_csrf_token()
    csrf2, cookies2 = sign_in(csrf1, cookies1)

    token = obtain_personal_access_token("default", csrf2, cookies2)
    print(token)


if __name__ == "__main__":
    main()
