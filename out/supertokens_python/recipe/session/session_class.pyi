from .interfaces import SessionContainer as SessionContainer
from typing import Any, Dict, Union

class Session(SessionContainer):
    remove_cookies: bool
    async def revoke_session(self, user_context: Union[Any, None] = ...) -> None: ...
    async def get_session_data(self, user_context: Union[Dict[str, Any], None] = ...) -> Dict[str, Any]: ...
    async def update_session_data(self, new_session_data: Dict[str, Any], user_context: Union[Dict[str, Any], None] = ...) -> None: ...
    access_token_payload: Any
    access_token: Any
    new_access_token_info: Any
    async def update_access_token_payload(self, new_access_token_payload: Dict[str, Any], user_context: Union[Dict[str, Any], None] = ...) -> None: ...
    def get_user_id(self, user_context: Union[Dict[str, Any], None] = ...) -> str: ...
    def get_access_token_payload(self, user_context: Union[Dict[str, Any], None] = ...) -> Dict[str, Any]: ...
    def get_handle(self, user_context: Union[Dict[str, Any], None] = ...) -> str: ...
    def get_access_token(self, user_context: Union[Dict[str, Any], None] = ...) -> str: ...
    async def get_time_created(self, user_context: Union[Dict[str, Any], None] = ...) -> int: ...
    async def get_expiry(self, user_context: Union[Dict[str, Any], None] = ...) -> int: ...