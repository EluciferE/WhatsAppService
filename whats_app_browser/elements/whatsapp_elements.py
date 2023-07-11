from ..types import SearchElement
from .elements_xpath import ELEMENT_XPATH

from selenium.webdriver.common.by import By

QR_CODE = SearchElement(By.TAG_NAME, "canvas")
QR_PRELOAD = SearchElement(By.XPATH, ELEMENT_XPATH.QR_PRELOAD)

CHATS_SIDEBAR = SearchElement(By.ID, "side")
CURRENT_CHAT = SearchElement(By.ID, "main")
POPUP = SearchElement(By.XPATH, ELEMENT_XPATH.CHAT_POPUP)

PROFILE_SMALL_PIC = SearchElement(By.XPATH, ELEMENT_XPATH.PROFILE_SMALL_PIC)
PROFILE_SIDEBAR = SearchElement(By.XPATH, ELEMENT_XPATH.PROFILE_SIDEBAR)

LOGOUT_BUTTON = SearchElement(By.XPATH, ELEMENT_XPATH.LOGOUT_BUTTON)
