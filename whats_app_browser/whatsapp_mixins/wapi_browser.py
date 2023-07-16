from typing import Optional, Union

from .base_browser import BaseWhatsAppBrowser
from ..types import Profile
from ..exceptions import NoSuchProfile, NoProfilePicture


class WAPIBrowser(BaseWhatsAppBrowser):
    def __init__(self, user_data_dir: Optional[str] = "user-data-dir"):
        super().__init__(user_data_dir)

    @property
    def injected(self):
        return self._browser.execute_script(
            "return "
            "typeof window.WAPI !== 'undefined' && "
            "typeof window.Store !== 'undefined'"
        )

    def inject_api(self):
        if self.injected:
            return

        self._wait_whatsapp_js_load()
        self._init_wppconnect()
        self._init_wapi()

    def _init_wppconnect(self):
        # https://github.com/wppconnect-team/wa-js/releases/download/nightly/wppconnect-wa.js
        self._add_script_file("axios.js")
        self._add_script_file("wppconnect-wa.js")

        self._execute_script_until_value("return window.WPP?.isReady", True)
        self._browser.execute_script(
            "WPP.chat.defaultSendMessageOptions.createChat = true;"
            "WPP.conn.setKeepAlive(true);"
        )

    def _init_wapi(self):
        # https://github.com/3mora2/WPP_Whatsapp/blob/main/WPP_Whatsapp/js_lib/wapi.js
        self._add_script_file("wapi.js")
        self._execute_script_until_value(
            "return "
            "typeof window.WAPI !== 'undefined' && "
            "typeof window.Store !== 'undefined' && "
            "window.WPP.isReady;",
            True
        )

    def _wait_whatsapp_js_load(self):
        self._execute_script_until_value(
            "return (window?.webpackChunkwhatsapp_web_client?.length || 0) > 3",
            True
        )

    def is_profile_exists(self, phone: str) -> bool:
        return self._get_profile(phone).numberExists

    def get_profile_picture(self, phone: str):
        profile = self._get_profile(phone)
        if not profile.numberExists:
            raise NoSuchProfile(phone)

        picture = self._get_profile_picture(profile.id)
        if not picture:
            raise NoProfilePicture()

        return picture

    def _get_profile(self, phone: str) -> Profile:
        print("Getting profile", phone)
        phone = self._format_phone(phone)
        print("Getting format_profile", phone)
        ans = self._browser.execute_async_script("""
            var callback = arguments[arguments.length - 1];
            WAPI.checkNumberStatus(`${arguments[0]}@c.us`)
                .then(function(result) {
                    callback(result);
                })
                .catch(function(error) {
                    callback(null);
                });
        """, phone)

        print("Getting ans", ans)

        if ans is None:
            raise Exception("Error getting profile")

        return Profile.from_dict(ans)

    @classmethod
    def _format_phone(cls, phone: str) -> str:
        return ''.join([c for c in phone if c.isdigit()])

    def _get_profile_picture(self, profile_id: dict) -> Union[str, bool]:
        ans = self._browser.execute_async_script("""
            var callback = arguments[arguments.length - 1];
            WAPI.getProfilePicFromId(arguments[0])
                .then(function(result) {
                    callback(result);
                })
                .catch(function(error) {
                    callback(null);
                });
        """, profile_id)
        if ans is None:
            raise Exception("Error getting profile picture")

        return ans
