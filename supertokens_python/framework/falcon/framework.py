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

from supertokens_python.framework.falcon.falcon_request import FalconRequest
from supertokens_python.framework.falcon.falcon_response import FalconResponse
from supertokens_python.framework.types import Framework


class FalconFramework(Framework):
    from falcon import Request, Response

    def wrap_request(self, unwrapped: Request):
        return FalconRequest(unwrapped)

    def wrap_response(self, unwrapped: Response):
        return FalconResponse(unwrapped)
