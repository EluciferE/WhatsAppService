import os
from typing import Optional, List, Tuple
from ..mixins import Locked
from ..types import SearchElement
from ..elements import QR_CODE, CHATS_SIDEBAR
import logging

import time
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class BaseWhatsAppBrowser(Locked):
    _WP_LINK = "https://web.whatsapp.com"
    _USER_LINK = "send/?phone=%s&text&type=phone_number&app_absent=0"

    def __init__(self, user_data_dir: str):
        super().__init__()
        user_data_dir = os.path.join(os.getcwd(), user_data_dir)

        service = Service(executable_path=ChromeDriverManager().install())
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument(f"user-data-dir={user_data_dir}")
        chrome_options.add_argument(f"start-maximized")
        chrome_options.add_argument(f"ignore-certificate-errors")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument(f'--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                                    f' (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')

        self._browser = webdriver.Chrome(service=service, options=chrome_options)
        self._logger = logging.getLogger("WhatsApp Browser")

    def sing_to_wp(self):
        self._get(self._WP_LINK)

    def _wait_unit_page_loaded(self, timeout: float = 20) -> bool:
        elements = [CHATS_SIDEBAR, QR_CODE]

        is_page_loaded = self._get_at_least_one_element(elements, timeout)
        return bool(is_page_loaded)

    @staticmethod
    def _force_click(element: WebElement):
        while True:
            try:
                element.click()
                break
            except ElementClickInterceptedException:
                continue

    def _get(self, url: str):
        if not self._lock.locked():
            self._logger.warning("Using browser without lock is unsafe. Please use `async with browser`")
        return self._browser.get(url)

    def _get_profile_page(self, phone: str):
        return self._get(f"{self._WP_LINK}/{self._USER_LINK}" % phone)

    def _find_element(self, element: SearchElement) -> Optional[WebElement]:
        try:
            return self._browser.find_element(*element)
        except NoSuchElementException:
            return

    def _get_element_until(self, element: SearchElement, timeout: float) -> Optional[WebElement]:
        try:
            return WebDriverWait(self._browser, timeout=timeout).until(
                lambda x: x.find_element(*element)
            )
        except TimeoutException:
            return

    def _get_at_least_one_element(self, elements: List[SearchElement], timeout: float = 20) -> Optional[
        Tuple[SearchElement, WebElement]
    ]:
        POLL_FREQ = 0.5
        start_time = time.monotonic()
        while True:
            if time.monotonic() - start_time >= timeout:
                return

            for element in elements:
                web_element = self._find_element(element)
                if web_element:
                    return element, web_element

            time.sleep(POLL_FREQ)
