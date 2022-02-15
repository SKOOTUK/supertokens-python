import abc
from .types import User as User
from abc import ABC, abstractmethod
from supertokens_python.recipe.emailpassword.interfaces import APIOptions as EmailPasswordApiOptions, CreateResetPasswordResult as CreateResetPasswordResult, EmailExistsGetResponse as EmailExistsGetResponse, GeneratePasswordResetTokenPostResponse as GeneratePasswordResetTokenPostResponse, PasswordResetPostResponse as PasswordResetPostResponse, ResetPasswordUsingTokenResult as ResetPasswordUsingTokenResult, SignInPostResponse as SignInPostResponse, SignInResult as SignInResult, SignUpPostResponse as SignUpPostResponse, SignUpResult as SignUpResult, UpdateEmailOrPasswordResult as UpdateEmailOrPasswordResult
from supertokens_python.recipe.emailpassword.types import FormField as FormField
from supertokens_python.recipe.thirdparty.interfaces import APIOptions as ThirdPartyApiOptions, AuthorisationUrlGetResponse as AuthorisationUrlGetResponse, SignInUpPostResponse as SignInUpPostResponse, SignInUpResult as SignInUpResult
from supertokens_python.recipe.thirdparty.provider import Provider as Provider
from typing import Any, Dict, List, Union

class RecipeInterface(ABC, metaclass=abc.ABCMeta):
    def __init__(self) -> None: ...
    @abstractmethod
    async def get_user_by_id(self, user_id: str, user_context: Dict[str, Any]) -> Union[User, None]: ...
    @abstractmethod
    async def get_users_by_email(self, email: str, user_context: Dict[str, Any]) -> List[User]: ...
    @abstractmethod
    async def get_user_by_thirdparty_info(self, third_party_id: str, third_party_user_id: str, user_context: Dict[str, Any]) -> Union[User, None]: ...
    @abstractmethod
    async def sign_in_up(self, third_party_id: str, third_party_user_id: str, email: str, email_verified: bool, user_context: Dict[str, Any]) -> SignInUpResult: ...
    @abstractmethod
    async def sign_in(self, email: str, password: str, user_context: Dict[str, Any]) -> SignInResult: ...
    @abstractmethod
    async def sign_up(self, email: str, password: str, user_context: Dict[str, Any]) -> SignUpResult: ...
    @abstractmethod
    async def create_reset_password_token(self, user_id: str, user_context: Dict[str, Any]) -> CreateResetPasswordResult: ...
    @abstractmethod
    async def reset_password_using_token(self, token: str, new_password: str, user_context: Dict[str, Any]) -> ResetPasswordUsingTokenResult: ...
    @abstractmethod
    async def update_email_or_password(self, user_id: str, email: Union[str, None], password: Union[str, None], user_context: Dict[str, Any]) -> UpdateEmailOrPasswordResult: ...

class APIInterface(ABC, metaclass=abc.ABCMeta):
    disable_thirdparty_sign_in_up_post: bool
    disable_emailpassword_sign_up_post: bool
    disable_emailpassword_sign_in_post: bool
    disable_authorisation_url_get: bool
    disable_email_exists_get: bool
    disable_generate_password_reset_token_post: bool
    disable_password_reset_post: bool
    disable_apple_redirect_handler_post: bool
    def __init__(self) -> None: ...
    @abstractmethod
    async def authorisation_url_get(self, provider: Provider, api_options: ThirdPartyApiOptions, user_context: Dict[str, Any]) -> AuthorisationUrlGetResponse: ...
    @abstractmethod
    async def thirdparty_sign_in_up_post(self, provider: Provider, code: str, redirect_uri: str, client_id: Union[str, None], auth_code_response: Union[Dict[str, Any], None], api_options: ThirdPartyApiOptions, user_context: Dict[str, Any]) -> SignInUpPostResponse: ...
    @abstractmethod
    async def emailpassword_sign_in_post(self, form_fields: List[FormField], api_options: EmailPasswordApiOptions, user_context: Dict[str, Any]) -> SignInPostResponse: ...
    @abstractmethod
    async def emailpassword_sign_up_post(self, form_fields: List[FormField], api_options: EmailPasswordApiOptions, user_context: Dict[str, Any]) -> SignUpPostResponse: ...
    @abstractmethod
    async def email_exists_get(self, email: str, api_options: EmailPasswordApiOptions, user_context: Dict[str, Any]) -> EmailExistsGetResponse: ...
    @abstractmethod
    async def generate_password_reset_token_post(self, form_fields: List[FormField], api_options: EmailPasswordApiOptions, user_context: Dict[str, Any]) -> GeneratePasswordResetTokenPostResponse: ...
    @abstractmethod
    async def password_reset_post(self, form_fields: List[FormField], token: str, api_options: EmailPasswordApiOptions, user_context: Dict[str, Any]) -> PasswordResetPostResponse: ...
    @abstractmethod
    async def apple_redirect_handler_post(self, code: str, state: str, api_options: ThirdPartyApiOptions, user_context: Dict[str, Any]): ...