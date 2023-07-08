from .utils import with_timer
from .element_xpath import ELEMENT_XPATH
from .exceptions import NoProfilePicture, NoSuchProfile

from typing import Optional
import os
import time
import requests

from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class WhatsAppBrowser:
    _WP_LINK = "https://web.whatsapp.com"
    _USER_LINK = "send/?phone=%s&text&type=phone_number&app_absent=0"

    @with_timer
    def __init__(self, user_data_dir: Optional[str] = "user-data-dir"):
        user_data_dir = os.path.join(os.getcwd(), user_data_dir)

        service = Service(executable_path=ChromeDriverManager().install())
        chrome_options = Options()
        chrome_options.add_argument(
            f"user-data-dir={user_data_dir}"
        )

        self.browser = webdriver.Chrome(service=service, options=chrome_options)

    @with_timer
    def save_login_qr(self, filename: Optional[str] = None, timeout: float = 10) -> bool:
        if filename is None:
            filename = "qr-code.png"

        self._get(self._WP_LINK)
        qr_code = self._get_element_until(timeout, By.TAG_NAME, "canvas")
        if qr_code:
            qr_code.screenshot(filename)
            return True
        return False

    @with_timer
    def verify_session(self, timeout: float = 10) -> bool:
        self._get(self._WP_LINK)
        if self._get_element_until(timeout, By.TAG_NAME, "header"):
            return True
        return False

    @with_timer
    def get_profile_picture_bytes(self, phone: str) -> Optional[bytes]:
        picture_url = self.get_profile_picture_url(phone)
        if picture_url is None:
            return None
        return requests.get(picture_url).content

    @with_timer
    def get_profile_picture_url(self, phone: str) -> Optional[str]:
        try:
            self._open_profile_chat(phone)
            picture_url = self._get_big_picture_url()
            return picture_url
        except (NoSuchProfile, NoProfilePicture) as e:
            print(e)
            return

    def _open_profile_chat(self, phone: str) -> bool:
        POLL_FREQUENCY = 0.5
        TIMEOUT = 15

        self._get_profile_page(phone)
        start_time = time.time()
        is_popup_loaded = False

        while True:
            chat_popup = self._find_element(By.XPATH, ELEMENT_XPATH.CHAT_POPUP)
            popup_text = getattr(chat_popup, "text", None)

            if popup_text == "Начало чата":
                is_popup_loaded = True

            elif popup_text == "Неверный номер телефона." or time.time() - start_time >= TIMEOUT:
                raise NoSuchProfile(f"Profile with phone {phone!r} not found!")

            elif is_popup_loaded:
                return True

            time.sleep(POLL_FREQUENCY)

    def _get_big_picture_url(self) -> str:
        self._open_profile_sidebar()
        return self.__find_big_picture_url()

    def _open_profile_sidebar(self):
        profile_pic = self._get_element_until(timeout=10, by=By.XPATH, value=ELEMENT_XPATH.PROFILE_SMALL_PIC)
        profile_pic.click()

    def __find_big_picture_url(self) -> str:
        picture_div = self._get_element_until(5, by=By.XPATH, value=ELEMENT_XPATH.PROFILE_BIG_PIC)
        try:
            image = picture_div.find_element(by=By.TAG_NAME, value="img")
            return image.get_attribute("src")
        except NoSuchElementException:
            raise NoProfilePicture('Profile picture not found')

    def _get(self, url: str):
        return self.browser.get(url)

    def _get_profile_page(self, phone: str):
        return self._get(f"{self._WP_LINK}/{self._USER_LINK}" % phone)

    def _find_element(self, by: str, value: str) -> Optional[WebElement]:
        try:
            return self.browser.find_element(by, value)
        except NoSuchElementException:
            return
        except Exception:
            raise

    def _get_element_until(self, timeout: float, by: By, value: str) -> Optional[WebElement]:
        try:
            return WebDriverWait(self.browser, timeout=timeout).until(
                lambda x: x.find_element(by, value)
            )
        except TimeoutException:
            return None
        except Exception:
            raise
