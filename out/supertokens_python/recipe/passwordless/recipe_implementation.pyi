from .interfaces import ConsumeCodeExpiredUserInputCodeErrorResult as ConsumeCodeExpiredUserInputCodeErrorResult, ConsumeCodeIncorrectUserInputCodeErrorResult as ConsumeCodeIncorrectUserInputCodeErrorResult, ConsumeCodeOkResult as ConsumeCodeOkResult, ConsumeCodeRestartFlowErrorResult as ConsumeCodeRestartFlowErrorResult, ConsumeCodeResult as ConsumeCodeResult, CreateCodeOkResult as CreateCodeOkResult, CreateCodeResult as CreateCodeResult, CreateNewCodeForDeviceOkResult as CreateNewCodeForDeviceOkResult, CreateNewCodeForDeviceRestartFlowErrorResult as CreateNewCodeForDeviceRestartFlowErrorResult, CreateNewCodeForDeviceResult as CreateNewCodeForDeviceResult, CreateNewCodeForDeviceUserInputCodeAlreadyUsedErrorResult as CreateNewCodeForDeviceUserInputCodeAlreadyUsedErrorResult, RecipeInterface as RecipeInterface, RevokeAllCodesOkResult as RevokeAllCodesOkResult, RevokeAllCodesResult as RevokeAllCodesResult, RevokeCodeOkResult as RevokeCodeOkResult, RevokeCodeResult as RevokeCodeResult, UpdateUserEmailAlreadyExistsErrorResult as UpdateUserEmailAlreadyExistsErrorResult, UpdateUserOkResult as UpdateUserOkResult, UpdateUserPhoneNumberAlreadyExistsErrorResult as UpdateUserPhoneNumberAlreadyExistsErrorResult, UpdateUserResult as UpdateUserResult, UpdateUserUnknownUserIdErrorResult as UpdateUserUnknownUserIdErrorResult
from .types import DeviceCode as DeviceCode, DeviceType as DeviceType, User as User
from supertokens_python.normalised_url_path import NormalisedURLPath as NormalisedURLPath
from supertokens_python.querier import Querier as Querier
from typing import Any, Dict, List, Union

class RecipeImplementation(RecipeInterface):
    querier: Any
    def __init__(self, querier: Querier) -> None: ...
    async def create_code(self, email: Union[None, str], phone_number: Union[None, str], user_input_code: Union[None, str], user_context: Dict[str, Any]) -> CreateCodeResult: ...
    async def create_new_code_for_device(self, device_id: str, user_input_code: Union[str, None], user_context: Dict[str, Any]) -> CreateNewCodeForDeviceResult: ...
    async def consume_code(self, pre_auth_session_id: str, user_input_code: Union[str, None], device_id: Union[str, None], link_code: Union[str, None], user_context: Dict[str, Any]) -> ConsumeCodeResult: ...
    async def get_user_by_id(self, user_id: str, user_context: Dict[str, Any]) -> Union[User, None]: ...
    async def get_user_by_email(self, email: str, user_context: Dict[str, Any]) -> Union[User, None]: ...
    async def get_user_by_phone_number(self, phone_number: str, user_context: Dict[str, Any]) -> Union[User, None]: ...
    async def update_user(self, user_id: str, email: Union[str, None], phone_number: Union[str, None], user_context: Dict[str, Any]) -> UpdateUserResult: ...
    async def revoke_all_codes(self, email: Union[str, None], phone_number: Union[str, None], user_context: Dict[str, Any]) -> RevokeAllCodesResult: ...
    async def revoke_code(self, code_id: str, user_context: Dict[str, Any]) -> RevokeCodeResult: ...
    async def list_codes_by_email(self, email: str, user_context: Dict[str, Any]) -> List[DeviceType]: ...
    async def list_codes_by_phone_number(self, phone_number: str, user_context: Dict[str, Any]) -> List[DeviceType]: ...
    async def list_codes_by_device_id(self, device_id: str, user_context: Dict[str, Any]) -> Union[DeviceType, None]: ...
    async def list_codes_by_pre_auth_session_id(self, pre_auth_session_id: str, user_context: Dict[str, Any]) -> Union[DeviceType, None]: ...