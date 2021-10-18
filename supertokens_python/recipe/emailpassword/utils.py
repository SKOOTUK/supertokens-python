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
from __future__ import annotations

from os import environ
from re import fullmatch
from typing import List, Union, Callable, Awaitable, TYPE_CHECKING

from .interfaces import RecipeInterface, APIInterface
from .types import User, FormField, NormalisedFormField, INPUT_SCHEMA

if TYPE_CHECKING:
    from .recipe import EmailPasswordRecipe
    from supertokens_python.supertokens import AppInfo
from .constants import (
    FORM_FIELD_EMAIL_ID,
    FORM_FIELD_PASSWORD_ID,
    RESET_PASSWORD
)
from supertokens_python.utils import get_filtered_list, validate_the_structure_of_user_input
from httpx import AsyncClient


async def default_validator(_):
    return None


async def default_handle_post_sign_up(_: User, __: List[FormField]):
    pass


async def default_handle_post_sign_in(_: User):
    pass


async def default_password_validator(value) -> Union[str, None]:
    # length >= 8 && < 100
    # must have a number and a character
    # as per
    # https://github.com/supertokens/supertokens-auth-react/issues/5#issuecomment-709512438
    if not isinstance(value, str):
        return 'Development bug: Please make sure the password field yields a string'

    if len(value) < 8:
        return 'Password must contain at least 8 characters, including a number'

    if len(value) >= 100:
        return 'Password\'s length must be lesser than 100 characters'

    if fullmatch(r'^.*[A-Za-z]+.*$', value) is None:
        return 'Password must contain at least one alphabet'

    if fullmatch(r'^.*[0-9]+.*$', value) is None:
        return 'Password must contain at least one number'

    return None


async def default_email_validator(value) -> Union[str, None]:
    # We check if the email syntax is correct
    # As per https://github.com/supertokens/supertokens-auth-react/issues/5#issuecomment-709512438
    # Regex from https://stackoverflow.com/a/46181/3867175
    if not isinstance(value, str):
        return 'Development bug: Please make sure the email field yields a string'

    if fullmatch(r'^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,'
                 r'3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$', value) is None:
        return 'Email is not valid'

    return None


def default_get_reset_password_url(
        app_info: AppInfo) -> Callable[[User], Awaitable[str]]:
    async def func(_: User):
        return app_info.website_domain.get_as_string_dangerous(
        ) + app_info.website_base_path.get_as_string_dangerous() + RESET_PASSWORD

    return func


def default_create_and_send_custom_email(
        app_info: AppInfo) -> Callable[[User, str], Awaitable]:
    async def func(user: User, password_reset_url_with_token: str):
        if ('SUPERTOKENS_ENV' in environ) and (
                environ['SUPERTOKENS_ENV'] == 'testing'):
            return
        try:
            data = {
                'email': user.email,
                'appName': app_info.app_name,
                'passwordResetURL': password_reset_url_with_token
            }
            async with AsyncClient() as client:
                await client.post('https://api.supertokens.io/0/st/auth/password/reset', json=data,
                                  headers={'api-version': '0'})
        except Exception:
            pass

    return func


class SignUpFeature:
    def __init__(self, form_fields: List[NormalisedFormField]):
        self.form_fields = form_fields


def normalise_sign_up_form_fields(form_fields) -> List[NormalisedFormField]:
    normalised_form_fields = []
    if form_fields is not None and isinstance(form_fields, list):
        for field in form_fields:
            if 'id' in field and field['id'] == FORM_FIELD_PASSWORD_ID:
                validator = field['validate'] if 'validate' in field else default_password_validator
                normalised_form_fields.append(
                    NormalisedFormField(
                        field['id'], validator, False))
            elif 'id' in field and field['id'] == FORM_FIELD_EMAIL_ID:
                validator = field['validate'] if 'validate' in field else default_email_validator
                normalised_form_fields.append(
                    NormalisedFormField(
                        field['id'], validator, False))
            else:
                validator = field['validate'] if 'validate' in field else default_validator
                optional = field['optional'] if 'optional' in field else False
                normalised_form_fields.append(
                    NormalisedFormField(
                        field['id'], validator, optional))
    if len(get_filtered_list(lambda x: x.id ==
           FORM_FIELD_PASSWORD_ID, normalised_form_fields)) == 0:
        normalised_form_fields.append(
            NormalisedFormField(
                FORM_FIELD_PASSWORD_ID,
                default_password_validator,
                False))
    if len(get_filtered_list(lambda x: x.id ==
           FORM_FIELD_EMAIL_ID, normalised_form_fields)) == 0:
        normalised_form_fields.append(
            NormalisedFormField(
                FORM_FIELD_EMAIL_ID,
                default_email_validator,
                False))
    return normalised_form_fields


def validate_and_normalise_sign_up_config(config=None) -> SignUpFeature:
    if config is None:
        config = {}
    form_fields = normalise_sign_up_form_fields(
        config['form_fields'] if 'form_fields' in config else None)
    return SignUpFeature(form_fields)


class SignInFeature:
    def __init__(self, form_fields: List[NormalisedFormField]):
        self.form_fields = form_fields


def normalise_sign_in_form_fields(
        form_fields: List[NormalisedFormField]) -> List[NormalisedFormField]:
    return list(map(
        lambda y: NormalisedFormField(
            y.id, y.validate if y.id == FORM_FIELD_EMAIL_ID else default_validator, False),
        get_filtered_list(lambda x: x.id == FORM_FIELD_PASSWORD_ID or x.id == FORM_FIELD_EMAIL_ID, form_fields)))


def validate_and_normalise_sign_in_config(
        sign_up_config: SignUpFeature) -> SignInFeature:
    form_fields = normalise_sign_in_form_fields(sign_up_config.form_fields)
    return SignInFeature(form_fields)


class ResetPasswordUsingTokenFeature:
    def __init__(self,
                 form_fields_for_password_reset_form: List[NormalisedFormField],
                 form_fields_for_generate_token_form: List[NormalisedFormField],
                 get_reset_password_url: Callable[[User], Awaitable[str]],
                 create_and_send_custom_email: Callable[[User, str], Awaitable]):
        self.form_fields_for_password_reset_form = form_fields_for_password_reset_form
        self.form_fields_for_generate_token_form = form_fields_for_generate_token_form
        self.get_reset_password_url = get_reset_password_url
        self.create_and_send_custom_email = create_and_send_custom_email


def validate_and_normalise_reset_password_using_token_config(app_info: AppInfo, sign_up_config: SignUpFeature,
                                                             config=None) -> ResetPasswordUsingTokenFeature:
    if config is None:
        config = {}
    form_fields_for_password_reset_form = list(map(lambda y: NormalisedFormField(y.id, y.validate, False),
                                                   get_filtered_list(lambda x: x.id == FORM_FIELD_PASSWORD_ID,
                                                                     sign_up_config.form_fields)))
    form_fields_for_generate_token_form = list(map(lambda y: NormalisedFormField(y.id, y.validate, False),
                                                   get_filtered_list(lambda x: x.id == FORM_FIELD_EMAIL_ID,
                                                                     sign_up_config.form_fields)))
    get_reset_password_url = config[
        'get_reset_password_url'] if 'get_reset_password_url' in config else default_get_reset_password_url(app_info)
    create_and_send_custom_email = config[
        'create_and_send_custom_email'] if 'create_and_send_custom_email' in config else default_create_and_send_custom_email(
        app_info)
    return ResetPasswordUsingTokenFeature(form_fields_for_password_reset_form,
                                          form_fields_for_generate_token_form, get_reset_password_url,
                                          create_and_send_custom_email)


def email_verification_create_and_send_custom_email(
        recipe: EmailPasswordRecipe, create_and_send_custom_email):
    async def func(user, link):
        user_info = await recipe.recipe_implementation.get_user_by_id(user.user_id)
        if user_info is None:
            raise Exception('Unknown User ID provided')
        return await create_and_send_custom_email(user_info, link)

    return func


def email_verification_get_email_verification_url(
        recipe: EmailPasswordRecipe, get_email_verification_url):
    async def func(user):
        user_info = await recipe.recipe_implementation.get_user_by_id(user.id)
        if user_info is None:
            raise Exception('Unknown User ID provided')
        return await get_email_verification_url(user_info)

    return func


def validate_and_normalise_email_verification_config(
        recipe: EmailPasswordRecipe, config=None, override=None):
    create_and_send_custom_email = None
    get_email_verification_url = None
    if config is None:
        config = {}
    if override is None:
        override = {}
    if 'create_and_send_custom_email' in config:
        create_and_send_custom_email = email_verification_create_and_send_custom_email(recipe, config[
            'create_and_send_custom_email'])
    if 'get_email_verification_url' in config:
        get_email_verification_url = email_verification_get_email_verification_url(recipe,
                                                                                   config['get_email_verification_url'])
    return {
        'get_email_for_user_id': recipe.get_email_for_user_id,
        'create_and_send_custom_email': create_and_send_custom_email,
        'get_email_verification_url': get_email_verification_url,
        'override': override
    }


class OverrideConfig:
    def __init__(self, functions: Union[Callable[[RecipeInterface], RecipeInterface], None],
                 apis: Union[Callable[[APIInterface], APIInterface], None]):
        self.functions = functions
        self.apis = apis


class EmailPasswordConfig:
    def __init__(self,
                 sign_up_feature: SignUpFeature,
                 sign_in_feature: SignInFeature,
                 reset_token_using_password_feature: ResetPasswordUsingTokenFeature,
                 email_verification_feature: any,
                 override: OverrideConfig):
        self.sign_up_feature = sign_up_feature
        self.sign_in_feature = sign_in_feature
        self.reset_token_using_password_feature = reset_token_using_password_feature
        self.email_verification_feature = email_verification_feature
        self.override = override


def validate_and_normalise_user_input(recipe: EmailPasswordRecipe, app_info: AppInfo,
                                      config) -> EmailPasswordConfig:
    validate_the_structure_of_user_input(
        config, INPUT_SCHEMA, 'emailpassword recipe', recipe)
    sign_up_feature = validate_and_normalise_sign_up_config(
        config['sign_up_feature'] if 'sign_up_feature' in config else None)
    sign_in_feature = validate_and_normalise_sign_in_config(sign_up_feature)
    reset_token_using_password_feature = validate_and_normalise_reset_password_using_token_config(
        app_info,
        sign_up_feature,
        config['reset_password_using_token_feature'] if 'reset_password_using_token_feature' in config else None)
    email_verification_feature = validate_and_normalise_email_verification_config(
        recipe,
        config['email_verification_feature'] if 'email_verification_feature' in config else None,
        config['override']['email_verification_feature'] if 'override' in config and 'email_verification_feature' in
                                                            config['override'] else None)
    override_functions = config['override']['functions'] if 'override' in config and 'functions' in config[
        'override'] else None
    override_apis = config['override']['apis'] if 'override' in config and 'apis' in config[
        'override'] else None
    override = OverrideConfig(override_functions, override_apis)
    return EmailPasswordConfig(sign_up_feature, sign_in_feature,
                               reset_token_using_password_feature, email_verification_feature, override)
