import selenium.common.exceptions

from .decorators import with_timer
from .elements import QR_CODE, CHATS_SIDEBAR, CURRENT_CHAT, POPUP, PROFILE_SIDEBAR, IMAGE, PROFILE_SMALL_PIC
from .exceptions import NoProfilePicture, NoSuchProfile, NotAuthenticated
from .whatsapp_mixins import BaseWhatsAppBrowser

from typing import Optional
import time
import requests

from selenium.common import NoSuchElementException


class WhatsAppBrowser(BaseWhatsAppBrowser):
    @with_timer
    def __init__(self, user_data_dir: Optional[str] = "user-data-dir"):
        super().__init__(user_data_dir)

    @with_timer
    def save_login_qr(self, filename: Optional[str] = "qr-code.png", timeout: float = 10) -> bool:
        self._get(self._WP_LINK)
        self._wait_unit_page_loaded(timeout)
        qr_code = self._find_element(QR_CODE)
        if qr_code:
            qr_code.screenshot(filename)
            return True
        return False

    @with_timer
    def verify_session(self, timeout: float = 10) -> bool:
        self._get(self._WP_LINK)
        self._wait_unit_page_loaded(timeout)
        if self._find_element(CHATS_SIDEBAR):
            return True
        return False

    @with_timer
    def get_profile_picture_bytes(self, phone: str) -> Optional[bytes]:
        picture_url = self.get_profile_picture_url(phone)
        if picture_url is None:
            return None
        return requests.get(picture_url).content

    @with_timer
    def get_profile_picture_url(self, phone: str) -> str:
        self._open_profile_chat(phone)
        picture_url = self._get_big_picture_url()
        return picture_url

    @with_timer
    def _open_profile_chat(self, phone: str) -> bool:
        POLL_FREQUENCY = 0.5
        TIMEOUT = 20

        self._get_profile_page(phone)

        is_page_loaded = self._wait_unit_page_loaded()
        if not is_page_loaded:
            raise NotAuthenticated()

        start_time = time.time()

        while True:
            popup_text = self._get_popup_text()
            chat_container = self._find_element(CURRENT_CHAT)

            if chat_container is not None:
                return True

            if popup_text == "Неверный номер телефона." or time.time() - start_time >= TIMEOUT:
                raise NoSuchProfile(f"Profile with phone {phone!r} not found!")

            time.sleep(POLL_FREQUENCY)

    def _get_popup_text(self):
        popup = self._find_element(POPUP)
        try:
            return getattr(popup, "text", None)
        except selenium.common.exceptions.StaleElementReferenceException:
            return None

    @with_timer
    def _get_big_picture_url(self) -> str:
        self._open_profile_sidebar()
        return self._find_big_picture_url()

    @with_timer
    def _open_profile_sidebar(self):
        profile_pic = self._get_element_until(PROFILE_SMALL_PIC, timeout=10)
        time.sleep(1)
        profile_pic.click()

    @with_timer
    def _find_big_picture_url(self) -> str:
        profile_sidebar = self._get_element_until(PROFILE_SIDEBAR, timeout=10)
        try:
            time.sleep(2)
            if profile_sidebar is None:
                raise NoProfilePicture('Can`t open profile sidebar')

            image = profile_sidebar.find_element(*IMAGE)
            image_url = image.get_attribute("src")
            if image_url.startswith("http"):
                return image_url

            raise NoSuchElementException()
        except NoSuchElementException:
            raise NoProfilePicture('Profile picture not found')
