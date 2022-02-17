# Copyright (c) 2021, VRAI Labs and/or its affiliates. All rights reserved.
#
# This software is licensed under the Apache License, Version 2.0 (the
# "License") as published by the Apache Software Foundation.
#
# You may not use this file except in compliance with the License. You may
# obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import json
from math import ceil
from time import time

from supertokens_python.framework.response import BaseResponse


class FalconResponse(BaseResponse):

    def __init__(self, resp=None):
        super().__init__({})
        self.response = resp
        self.headers = dict()
        self.response_sent = False
        self.status_set = False

    def set_html_content(self, content):
        if not self.response_sent:
            self.response.text = content
            self.set_header('Content-Type', 'text/html')
            self.response_sent = True

    def set_cookie(
        self,
        key: str,
        value: str = "",
        max_age: int = None,
        expires: int = None,
        path: str = "/",
        domain: str = None,
        secure: bool = False,
        httponly: bool = False,
        samesite: str = "lax"
    ):
        self.response.set_cookie(
            key,
            value,
            expires=ceil((expires - int(time() * 1000)) / 1000),
            max_age=max_age,
            domain=domain,
            path=path,
            secure=secure,
            http_only=httponly,
            same_site=samesite
        )

    def set_header(self, key, value):
        self.response.set_header(key, value)

    def get_header(self, key):
        return self.response.get_header(key, None)

    def set_status_code(self, status_code):
        if not self.status_set:
            self.response.status = status_code
            self.status_set = True

    def get_headers(self):
        return self.response.headers

    def set_json_content(self, content):
        if not self.response_sent:
            self.set_header('Content-Type', 'application/json; charset=utf-8')
            self.response.data = json.dumps(
                content,
                ensure_ascii=False,
                allow_nan=False,
                indent=None,
                separators=(",", ":"),
            ).encode("utf-8")
            self.response_sent = True
