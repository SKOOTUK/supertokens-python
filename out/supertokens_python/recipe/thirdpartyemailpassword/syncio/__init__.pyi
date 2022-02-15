from supertokens_python.async_to_sync_wrapper import sync as sync
from typing import Any, Dict, Union

def create_email_verification_token(user_id: str, user_context: Union[None, Dict[str, Any]] = ...): ...
def verify_email_using_token(token: str, user_context: Union[None, Dict[str, Any]] = ...): ...
def is_email_verified(user_id: str, user_context: Union[None, Dict[str, Any]] = ...): ...
def unverify_email(user_id: str, user_context: Union[None, Dict[str, Any]] = ...): ...
def get_user_by_id(user_id: str, user_context: Union[None, Dict[str, Any]] = ...): ...
def get_user_by_third_party_info(third_party_id: str, third_party_user_id: str, user_context: Union[None, Dict[str, Any]] = ...): ...
def sign_in_up(third_party_id: str, third_party_user_id: str, email: str, email_verified: bool, user_context: Union[None, Dict[str, Any]] = ...): ...
def create_reset_password_token(user_id: str, user_context: Union[None, Dict[str, Any]] = ...): ...
def reset_password_using_token(token: str, new_password: str, user_context: Union[None, Dict[str, Any]] = ...): ...
def sign_in(email: str, password: str, user_context: Union[None, Dict[str, Any]] = ...): ...
def sign_up(email: str, password: str, user_context: Union[None, Dict[str, Any]] = ...): ...
def update_email_or_password(user_id: str, email: Union[None, str] = ..., password: Union[None, str] = ..., user_context: Union[None, Dict[str, Any]] = ...): ...
def get_users_by_email(email: str, user_context: Union[None, Dict[str, Any]] = ...): ...
async def revoke_email_verification_tokens(user_id: str, user_context: Union[None, Dict[str, Any]] = ...): ...