from .decorators import with_timer
from .elements import QR_CODE
from .exceptions import Authenticated
from .whatsapp_mixins import WAPIBrowser
from typing import Optional


class WhatsAppBrowser(WAPIBrowser):
    @with_timer
    def __init__(self, user_data_dir: Optional[str] = "user-data-dir"):
        super().__init__(user_data_dir)

    @with_timer
    def get_login_qr_code_as_base64(self, timeout: float = 10) -> str:
        login_status = self.is_authenticated(timeout)
        if login_status is True:
            raise Authenticated()

        qr_code = self._find_element(QR_CODE)
        if qr_code:
            return qr_code.screenshot_as_base64

        raise Exception("Can't find QR-Code on page")

    @with_timer
    def is_authenticated(self, timeout: float = 10) -> bool:
        return self._check_authentication(timeout)

    @with_timer
    def get_profile_picture_url(self, phone: str) -> Optional[str]:
        return self.check_profile_and_get_avatar_url(phone)
