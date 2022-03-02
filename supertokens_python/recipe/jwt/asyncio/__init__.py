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

from supertokens_python.recipe.jwt.interfaces import (CreateJwtResult,
                                                      GetJWKSResult)
from supertokens_python.recipe.jwt.recipe import JWTRecipe


async def create_jwt(payload: Union[None, Dict[str, Any]] = None, validity_seconds: Union[None, int] = None, user_context: Union[Dict[str, Any], None] = None) -> CreateJwtResult:
    if user_context is None:
        user_context = {}
    if payload is None:
        payload = {}

    return await JWTRecipe.get_instance().recipe_implementation.create_jwt(payload, validity_seconds, user_context)


async def get_jwks(user_context: Union[Dict[str, Any], None] = None) -> GetJWKSResult:
    if user_context is None:
        user_context = {}
    return await JWTRecipe.get_instance().recipe_implementation.get_jwks(user_context)
