from ..types import SearchElement
from .elements_xpath import ELEMENT_XPATH

from selenium.webdriver.common.by import By

QR_CODE = SearchElement(By.XPATH, ELEMENT_XPATH.QR_CODE)
QR_PRELOAD = SearchElement(By.XPATH, ELEMENT_XPATH.QR_PRELOAD)

CHATS_SIDEBAR = SearchElement(By.ID, "side")
CURRENT_CHAT = SearchElement(By.ID, "main")
POPUP = SearchElement(By.XPATH, ELEMENT_XPATH.CHAT_POPUP)

PROFILE_HEADER = SearchElement(By.XPATH, ELEMENT_XPATH.PROFILE_HEADER)
PROFILE_BIG_PIC = SearchElement(By.XPATH, ELEMENT_XPATH.PROFILE_BIG_PIC)
PROFILE_SIDEBAR = SearchElement(By.XPATH, ELEMENT_XPATH.PROFILE_SIDEBAR)

LOADING_SCREEN = SearchElement(By.XPATH, ELEMENT_XPATH.LOADING_SCREEN)
