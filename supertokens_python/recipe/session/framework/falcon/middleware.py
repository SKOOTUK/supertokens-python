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
import falcon
from typing import Union

from supertokens_python.async_to_sync_wrapper import sync
from supertokens_python.framework.falcon.falcon_request import FalconRequest
from supertokens_python.framework.falcon.falcon_response import FalconResponse
from supertokens_python.recipe.session import SessionRecipe
from supertokens_python.recipe.session.exceptions import UnauthorisedError
from supertokens_python.recipe.session.framework.falcon.log import set_logger

logger = set_logger()


def verify_session(
    req: FalconRequest,
    resp: FalconResponse,
    resource,
    params,
    anti_csrf_check: Union[bool, None] = None,
    session_required: bool = True
):
    request = FalconRequest(req)
    recipe = SessionRecipe.get_instance()

    try:
        session = sync(
            recipe.verify_session(
                request,
                anti_csrf_check,
                session_required
            )
        )
    except UnauthorisedError as e:
        logger.info(f"Authorization Error: {e}")
        raise falcon.HTTPUnauthorized(
            title="401 Unauthorized",
            description="Authorization data is incorrect or missing"
        )
    else:
        request.set_session(session)
