# Auto login for http://readfree.me
# Sign up and get random credit!
import requests
import http.cookiejar
import os

url = "http://readfree.me"
current_path = os.path.dirname(os.path.abspath(__file__))
cookies_path = os.path.join(current_path, "readfree.cookies")
headers = {}
headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/51.0"


def login():
    s = requests.Session()
    s.headers.update(headers)
    ck = load_cookies()
    s.cookies.update(ck)
    s.get(url)
    save_cookies(s.cookies)


def save_cookies(cookies):
    """
    No need to change cookies, it seems.
    """
    save_cj = http.cookiejar.LWPCookieJar()
    save_ck = {c.name: c.value for c in cookies}
    requests.utils.cookiejar_from_dict(save_ck, save_cj)
    save_cj.save(cookies_path, ignore_expires=True, ignore_discard=True)


def load_cookies():
    load_cj = http.cookiejar.LWPCookieJar()
    load_cj.load(cookies_path, ignore_expires=True, ignore_discard=True)
    load_ck = requests.utils.dict_from_cookiejar(load_cj)
    return load_ck


def process_cookies():
    """
    To process the very first cookies.
    """
    save_cj = http.cookiejar.LWPCookieJar()
    save_ck = {
        "csrftoken": "",
        "sessionid": ""
    }
    requests.utils.cookiejar_from_dict(save_ck, save_cj)
    save_cj.save(cookies_path, ignore_expires=True, ignore_discard=True)


login()
