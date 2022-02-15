from supertokens_python.framework.request import BaseRequest as BaseRequest
from supertokens_python.recipe.thirdparty.provider import Provider as Provider
from supertokens_python.recipe.thirdparty.types import AccessTokenAPI as AccessTokenAPI, AuthorisationRedirectAPI as AuthorisationRedirectAPI, UserInfo as UserInfo, UserInfoEmail as UserInfoEmail
from supertokens_python.utils import get_filtered_list as get_filtered_list
from typing import Any, Callable, Dict, List, Union

class Github(Provider):
    client_secret: Any
    scopes: Any
    access_token_api_url: str
    authorisation_redirect_url: str
    authorisation_redirect_params: Any
    def __init__(self, client_id: str, client_secret: str, scope: Union[None, List[str]] = ..., authorisation_redirect: Union[None, Dict[str, Union[str, Callable[[BaseRequest], str]]]] = ..., is_default: bool = ...) -> None: ...
    async def get_profile_info(self, auth_code_response: Dict[str, Any], user_context: Dict[str, Any]) -> UserInfo: ...
    def get_authorisation_redirect_api_info(self, user_context: Dict[str, Any]) -> AuthorisationRedirectAPI: ...
    def get_access_token_api_info(self, redirect_uri: str, auth_code_from_request: str, user_context: Dict[str, Any]) -> AccessTokenAPI: ...
    def get_redirect_uri(self, user_context: Dict[str, Any]) -> Union[None, str]: ...