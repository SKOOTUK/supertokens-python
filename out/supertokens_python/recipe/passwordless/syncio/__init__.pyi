from supertokens_python.async_to_sync_wrapper import sync as sync
from supertokens_python.recipe.passwordless import asyncio as asyncio
from supertokens_python.recipe.passwordless.interfaces import ConsumeCodeOkResult as ConsumeCodeOkResult, ConsumeCodeResult as ConsumeCodeResult, CreateCodeResult as CreateCodeResult, CreateNewCodeForDeviceResult as CreateNewCodeForDeviceResult, RevokeAllCodesResult as RevokeAllCodesResult, RevokeCodeResult as RevokeCodeResult, UpdateUserResult as UpdateUserResult
from supertokens_python.recipe.passwordless.types import DeviceType as DeviceType, User as User
from typing import Any, Dict, List, Union

def create_code(email: Union[None, str] = ..., phone_number: Union[None, str] = ..., user_input_code: Union[None, str] = ..., user_context: Union[None, Dict[str, Any]] = ...) -> CreateCodeResult: ...
def create_new_code_for_device(device_id: str, user_input_code: Union[str, None] = ..., user_context: Union[None, Dict[str, Any]] = ...) -> CreateNewCodeForDeviceResult: ...
def consume_code(pre_auth_session_id: str, user_input_code: Union[str, None] = ..., device_id: Union[str, None] = ..., link_code: Union[str, None] = ..., user_context: Union[None, Dict[str, Any]] = ...) -> ConsumeCodeResult: ...
def get_user_by_id(user_id: str, user_context: Union[None, Dict[str, Any]] = ...) -> Union[User, None]: ...
def get_user_by_email(email: str, user_context: Union[None, Dict[str, Any]] = ...) -> Union[User, None]: ...
def get_user_by_phone_number(phone_number: str, user_context: Union[None, Dict[str, Any]] = ...) -> Union[User, None]: ...
def update_user(user_id: str, email: Union[str, None] = ..., phone_number: Union[str, None] = ..., user_context: Union[None, Dict[str, Any]] = ...) -> UpdateUserResult: ...
def revoke_all_codes(email: Union[str, None] = ..., phone_number: Union[str, None] = ..., user_context: Union[None, Dict[str, Any]] = ...) -> RevokeAllCodesResult: ...
def revoke_code(code_id: str, user_context: Union[None, Dict[str, Any]] = ...) -> RevokeCodeResult: ...
def list_codes_by_email(email: str, user_context: Union[None, Dict[str, Any]] = ...) -> List[DeviceType]: ...
def list_codes_by_phone_number(phone_number: str, user_context: Union[None, Dict[str, Any]] = ...) -> List[DeviceType]: ...
def list_codes_by_device_id(device_id: str, user_context: Union[None, Dict[str, Any]] = ...) -> Union[DeviceType, None]: ...
def list_codes_by_pre_auth_session_id(pre_auth_session_id: str, user_context: Union[None, Dict[str, Any]] = ...) -> Union[DeviceType, None]: ...
def create_magic_link(email: Union[str, None], phone_number: Union[str, None], user_context: Union[None, Dict[str, Any]] = ...) -> str: ...
def signinup(email: Union[str, None], phone_number: Union[str, None], user_context: Union[None, Dict[str, Any]] = ...) -> ConsumeCodeOkResult: ...