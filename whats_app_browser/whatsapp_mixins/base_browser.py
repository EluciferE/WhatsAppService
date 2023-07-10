import os
from typing import Optional
from ..mixins import Locked
import logging

from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
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
        chrome_options.add_argument(f"user-data-dir={user_data_dir}")
        chrome_options.add_argument(f"start-maximized")
        chrome_options.add_argument(f"ignore-certificate-errors")

        self._browser = webdriver.Chrome(service=service, options=chrome_options)
        self._logger = logging.getLogger("WhatsApp Browser")

    def sing_to_wp(self):
        self._get(self._WP_LINK)

    def _get(self, url: str):
        if not self._lock.locked():
            self._logger.warning("Using browser without lock is unsafe. Please use `async with browser`")
        return self._browser.get(url)

    def _find_element(self, by: str, value: str) -> Optional[WebElement]:
        try:
            return self._browser.find_element(by, value)
        except NoSuchElementException:
            return

    def _get_element_until(self, timeout: float, by: By, value: str) -> Optional[WebElement]:
        try:
            return WebDriverWait(self._browser, timeout=timeout).until(
                lambda x: x.find_element(by, value)
            )
        except TimeoutException:
            return
