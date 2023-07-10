import selenium.common.exceptions

from .utils import with_timer
from .element_xpath import ELEMENT_XPATH
from .exceptions import NoProfilePicture, NoSuchProfile, NotAuthenticated

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
    def __init__(self, user_data_dir: Optional[str] = "user-data-dir", fullscreen: bool = True):
        user_data_dir = os.path.join(os.getcwd(), user_data_dir)

        service = Service(executable_path=ChromeDriverManager().install())
        chrome_options = Options()
        chrome_options.add_argument(f"user-data-dir={user_data_dir}")
        if fullscreen:
            chrome_options.add_argument(f"--start-maximized")

        self.browser = webdriver.Chrome(service=service, options=chrome_options)
        self.browser.get(self._WP_LINK)

    @with_timer
    def save_login_qr(self, filename: Optional[str] = "qr-code.png", timeout: float = 10) -> bool:
        self._get(self._WP_LINK)
        qr_code = self._get_element_until(timeout, By.TAG_NAME, "canvas")
        if qr_code:
            qr_code.screenshot(filename)
            return True
        return False

    @with_timer
    def verify_session(self, timeout: float = 10) -> bool:
        self._get(self._WP_LINK)
        if self._get_element_until(timeout, By.ID, "side"):
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
        except (NoSuchProfile, NoProfilePicture, NotAuthenticated) as e:
            print(e)
            return

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
            chat_container = self._find_element(By.ID, "main")

            if chat_container is not None:
                return True

            if popup_text == "Неверный номер телефона." or time.time() - start_time >= TIMEOUT:
                raise NoSuchProfile(f"Profile with phone {phone!r} not found!")

            time.sleep(POLL_FREQUENCY)

    def _get_popup_text(self):
        popup = self._find_element(By.XPATH, ELEMENT_XPATH.CHAT_POPUP)
        try:
            return getattr(popup, "text", None)
        except selenium.common.exceptions.StaleElementReferenceException:
            return None

    @with_timer
    def _get_big_picture_url(self) -> str:
        self._open_profile_sidebar()
        return self.__find_big_picture_url()

    @with_timer
    def _open_profile_sidebar(self):
        profile_pic = self._get_element_until(timeout=10, by=By.XPATH, value=ELEMENT_XPATH.PROFILE_SMALL_PIC)
        time.sleep(1)
        profile_pic.click()

    @with_timer
    def __find_big_picture_url(self) -> str:
        profile_sidebar = self._get_element_until(10, by=By.TAG_NAME, value="section")
        try:
            time.sleep(2)
            if profile_sidebar is None:
                raise NoProfilePicture('Can`t open profile sidebar')

            image = profile_sidebar.find_element(by=By.TAG_NAME, value="img")
            image_url = image.get_attribute("src")
            if image_url.startswith("http"):
                return image_url

            raise NoSuchElementException()
        except NoSuchElementException:
            raise NoProfilePicture('Profile picture not found')

    def _wait_unit_page_loaded(self, timeout: float = 20) -> bool:
        is_page_loaded = self._get_element_until(timeout=timeout, by=By.ID, value="side")
        return bool(is_page_loaded)

    def _get(self, url: str):
        return self.browser.get(url)

    def _get_profile_page(self, phone: str):
        return self._get(f"{self._WP_LINK}/{self._USER_LINK}" % phone)

    def _find_element(self, by: str, value: str) -> Optional[WebElement]:
        try:
            return self.browser.find_element(by, value)
        except NoSuchElementException:
            return

    def _get_element_until(self, timeout: float, by: By, value: str) -> Optional[WebElement]:
        try:
            return WebDriverWait(self.browser, timeout=timeout).until(
                lambda x: x.find_element(by, value)
            )
        except TimeoutException:
            return
