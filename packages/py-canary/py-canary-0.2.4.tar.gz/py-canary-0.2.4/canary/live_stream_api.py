import logging
import requests

COOKIE_XSRF_TOKEN = "XSRF-TOKEN"
COOKIE_SSESYRANAC = "ssesyranac"

COOKIE_VALUE_SSESYRANAC = "token={}"

HEADER_XSRF_TOKEN = "X-XSRF-TOKEN"
HEADER_SSESYRANAC = "ssesyranac"
HEADER_AUTHORIZATION = "Authorization"

HEADER_VALUE_AUTHORIZATION = "Bearer {}"

URL_LOGIN_PAGE = "https://my.canary.is/login"
URL_LOGIN_API = "https://my.canary.is/api/auth/login"
URL_GET_SESSION = "https://my.canary.is/api/watchlive/{device_uuid}/session"
URL_START_SESSION = "https://my.canary.is/api/watchlive/{device_uuid}/send"
URL_LIVE_STREAM = "https://my.canary.is/api/watchlive/{device_id}/{session_id}/stream.m3u8"

ATTR_USERNAME = "username"
ATTR_PASSWORD = "password"
ATTR_ACCESS_TOKEN = "access_token"
ATTR_SESSION_ID = "sessionId"

_LOGGER = logging.getLogger(__name__)


class LiveStreamApi:
    def __init__(self, username, password, timeout=10):
        self._username = username
        self._password = password
        self._timeout = timeout
        self._token = None
        self._xsrf_token = None

    def login(self):
        r = requests.get(URL_LOGIN_PAGE)

        xsrf_token = r.cookies[COOKIE_XSRF_TOKEN]
        ssesyranac = r.cookies[COOKIE_SSESYRANAC]

        r = requests.post(URL_LOGIN_API, {
            ATTR_USERNAME: self._username,
            ATTR_PASSWORD: self._password
        }, headers={
            HEADER_XSRF_TOKEN: xsrf_token
        }, cookies={
            COOKIE_XSRF_TOKEN: xsrf_token,
            COOKIE_SSESYRANAC: ssesyranac
        })

        self._token = r.json()[ATTR_ACCESS_TOKEN]
        self._xsrf_token = xsrf_token

    def get_session(self, device_uuid):
        r = requests.post(URL_GET_SESSION.format(device_uuid=device_uuid),
                          headers=self._api_headers(),
                          cookies=self._api_cookies())
        r.raise_for_status()

        return r.json().get(ATTR_SESSION_ID)

    def start_session(self, device_uuid, session_id):
        r = requests.post(URL_START_SESSION.format(device_uuid=device_uuid),
                          headers=self._api_headers(),
                          cookies=self._api_cookies(),
                          json={
                              ATTR_SESSION_ID: session_id
                          })
        r.raise_for_status()

        json = r.json()

        return "message" in json and json["message"] == "success"

    def get_live_stream_url(self, device_id, session_id):
        return URL_LIVE_STREAM.format(device_id=device_id,
                                      session_id=session_id);

    def _api_cookies(self):
        return {
            COOKIE_XSRF_TOKEN: self._xsrf_token,
            COOKIE_SSESYRANAC: COOKIE_VALUE_SSESYRANAC.format(self._token)
        }

    def _api_headers(self):
        return {
            HEADER_XSRF_TOKEN: self._xsrf_token,
            HEADER_AUTHORIZATION: HEADER_VALUE_AUTHORIZATION.format(
                self._token)
        }
