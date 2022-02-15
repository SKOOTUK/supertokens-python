from .constants import ACCESS_CONTROL_EXPOSE_HEADERS as ACCESS_CONTROL_EXPOSE_HEADERS, ACCESS_TOKEN_COOKIE_KEY as ACCESS_TOKEN_COOKIE_KEY, ANTI_CSRF_HEADER_KEY as ANTI_CSRF_HEADER_KEY, FRONT_TOKEN_HEADER_SET_KEY as FRONT_TOKEN_HEADER_SET_KEY, ID_REFRESH_TOKEN_COOKIE_KEY as ID_REFRESH_TOKEN_COOKIE_KEY, ID_REFRESH_TOKEN_HEADER_SET_KEY as ID_REFRESH_TOKEN_HEADER_SET_KEY, REFRESH_TOKEN_COOKIE_KEY as REFRESH_TOKEN_COOKIE_KEY, RID_HEADER_KEY as RID_HEADER_KEY
from .recipe import SessionRecipe as SessionRecipe
from supertokens_python.exceptions import raise_general_exception as raise_general_exception
from supertokens_python.framework.request import BaseRequest as BaseRequest
from supertokens_python.framework.response import BaseResponse as BaseResponse
from supertokens_python.utils import get_header as get_header, utf_base64encode as utf_base64encode
from typing import Any, Dict, Union
from typing_extensions import Literal

def set_front_token_in_headers(response: BaseResponse, user_id: str, expires_at: int, jwt_payload: Union[None, Dict[str, Any]] = ...): ...
def get_cors_allowed_headers(): ...
def set_header(response: BaseResponse, key: str, value: str, allow_duplicate: bool): ...
def get_cookie(request: BaseRequest, key: str): ...
def set_cookie(recipe: SessionRecipe, response: BaseResponse, key: str, value: str, expires: int, path_type: Literal['refresh_token_path', 'access_token_path']): ...
def attach_anti_csrf_header(response: BaseResponse, value: str): ...
def get_anti_csrf_header(request: BaseRequest): ...
def get_rid_header(request: BaseRequest): ...
def attach_access_token_to_cookie(recipe: SessionRecipe, response: BaseResponse, token: str, expires_at: int): ...
def attach_refresh_token_to_cookie(recipe: SessionRecipe, response: BaseResponse, token: str, expires_at: int): ...
def attach_id_refresh_token_to_cookie_and_header(recipe: SessionRecipe, response: BaseResponse, token: str, expires_at: int): ...
def get_access_token_from_cookie(request: BaseRequest): ...
def get_refresh_token_from_cookie(request: BaseRequest): ...
def get_id_refresh_token_from_cookie(request: BaseRequest): ...
def clear_cookies(recipe: SessionRecipe, response: BaseResponse): ...