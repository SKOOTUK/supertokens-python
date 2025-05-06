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

from typing import Any, Dict, Union
from supertokens_python.framework.request import BaseRequest


class FalconRequest(BaseRequest):
    def __init__(self, req):
        super().__init__()
        self.request = req

    def get_query_param(self, key: str, default: Union[str, None] = None) -> Union[str, None]:
        return self.request.params.get(key, default)

    def get_query_params(self) -> Dict[str, str]:
        return self.request.params

    async def json(self) -> Union[Dict[str, Any], None]:
        try:
            return self.request.media
        except Exception:
            return None

    def method(self) -> str:
        return self.request.method

    def form_data(self) -> Dict[str, Any]:
        return self.request.media  # or self.request.get_media() depending on your Falcon version

    def get_cookie(self, key: str) -> Union[str, None]:
        return self.request.cookies.get(key)

    def get_header(self, key: str) -> Union[str, None]:
        return self.request.get_header(key)

    def get_path(self) -> str:
        return self.request.path

    def get_original_url(self) -> str:
        return self.request.url

    def set_session_as_none(self) -> None:
        self.request.context.supertokens = None

    def get_session(self):
        return getattr(self.request.context, "supertokens", None)

    def set_session(self, session):
        self.request.context.supertokens = session
