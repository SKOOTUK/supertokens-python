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
from supertokens_python.async_to_sync_wrapper import sync


class Middleware:

    @staticmethod
    def error_handler(req, resp, error, params):
        from supertokens_python import Supertokens
        from supertokens_python.framework.falcon.falcon_request import FalconRequest
        from supertokens_python.framework.falcon.falcon_response import FalconResponse

        st = Supertokens.get_instance()
        response = FalconResponse(resp)
        result = sync(st.handle_supertokens_error(FalconRequest(req), error, response))
        return result.response

    def process_resource(self, req, resp, resource, params):
        from supertokens_python import Supertokens
        from supertokens_python.framework.falcon.falcon_request import FalconRequest
        from supertokens_python.framework.falcon.falcon_response import FalconResponse

        st = Supertokens.get_instance()

        request_ = FalconRequest(req)
        response_ = FalconResponse(resp)
        result = sync(st.middleware(request_, response_))

        if result is not None:
            return result.response

    def process_response(self, req, resp, resource, req_succeeded):
        from supertokens_python.framework.falcon.falcon_request import FalconRequest
        from supertokens_python.framework.falcon.falcon_response import FalconResponse
        from supertokens_python.recipe.session import Session
        from supertokens_python.supertokens import manage_cookies_post_response

        response_ = FalconResponse(resp)
        request_ = FalconRequest(req)
        session = request_.get_session()

        if isinstance(session, Session):
            manage_cookies_post_response(session, response_)

        return response_.response
