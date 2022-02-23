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
from functools import wraps
from typing import Union

from supertokens_python import Supertokens
from supertokens_python.exceptions import SuperTokensError
from supertokens_python.async_to_sync_wrapper import sync
from supertokens_python.framework.falcon.falcon_request import FalconRequest
from supertokens_python.framework.falcon.falcon_response import FalconResponse
from supertokens_python.recipe.session import SessionRecipe


def verify_session(
    req: FalconRequest,
    anti_csrf_check: Union[bool, None] = None,
    session_required: bool = True
):
    request = FalconRequest(req)
    recipe = SessionRecipe.get_instance()
    session = sync(
        recipe.verify_session(
            request,
            anti_csrf_check,
            session_required
        )
    )
    request.set_session(session)

# def verify_session(
#     anti_csrf_check: Union[bool, None] = None, session_required: bool = True
# ):
#     def session_verify(f):
#         @wraps(f)
#         def wrapped_function(resource, req, resp, **kwargs):
#             from falcon.response import Response
#             print(f"FUNCTION: {f}")
#             print(f"RESOURCE: {resource}")
#             print(f"REQUEST: {req}")
#             print(f"RESPONSE: {resp}")
#             try:
#                 print("STEP 1")
#                 request = FalconRequest(req)
#                 print("STEP 2")
#                 recipe = SessionRecipe.get_instance()
#                 print("STEP 3")
#                 session = sync(
#                     recipe.verify_session(
#                         request,
#                         anti_csrf_check,
#                         session_required
#                     )
#                 )
#                 print("STEP 4")
#                 print(session)
#                 request.set_session(session)
#                 print("STEP 5")
#                 print(f"RUNNING FUNCTION {f}")
#                 return f(resource, request.request, resp, **kwargs)
#             except SuperTokensError as e:
#                 print("EXCEPTION 1")
#                 response = FalconResponse(Response())
#                 print("EXCEPTION 2")
#                 result = sync(
#                     Supertokens.get_instance().handle_supertokens_error(
#                         FalconRequest(request), e, response
#                     )
#                 )
#                 print("EXCEPTION 3")
#                 print(f"RESULT: {result}")
#                 return result.response

#         return wrapped_function

#     return session_verify
