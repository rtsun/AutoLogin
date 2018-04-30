import requests
import http.cookiejar
import os
import time
import re
import logging
from config import account
from config import cookies
from urllib.parse import urljoin

url = "http://readfree.me"
post_url = "http://readfree.me/accounts/login/?next=/"
current_path = os.path.dirname(os.path.abspath(__file__))
cookies_path = os.path.join(current_path, "readfree.cookies")
logfile_path = os.path.join(current_path, "readfree.log")
captcha_path = os.path.join(current_path, "captcha.png")

headers = {}
headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/51.0"
s = requests.Session()
s.headers.update(headers)

logging.basicConfig(filename=logfile_path, level='DEBUG')
date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
logging.info("===============Log Started at " + date + "===============")


def load_cookies():
    load_cj = http.cookiejar.LWPCookieJar()
    load_cj.load(cookies_path, ignore_expires=True, ignore_discard=True)
    load_ck = requests.utils.dict_from_cookiejar(load_cj)
    return load_ck


def save_cookies(cookies):
    save_cj = http.cookiejar.LWPCookieJar()
    save_ck = {c.name: c.value for c in cookies}
    requests.utils.cookiejar_from_dict(save_ck, save_cj)
    save_cj.save(cookies_path, ignore_expires=True, ignore_discard=True)
    logging.info('Cookies updated.')


def process_cookies():
    save_cj = http.cookiejar.LWPCookieJar()
    requests.utils.cookiejar_from_dict(cookies, save_cj)
    save_cj.save(cookies_path, ignore_expires=True, ignore_discard=True)
    logging.info('Cookies generated.')


def login_by_cookies():
    ck = load_cookies()
    s.cookies.update(ck)
    req = s.get(url)
    if req.status_code == 200:
        save_cookies(s.cookies)
        logging.info("=============Login by cookies successfully at %s =============" % date)
    else:
        logging.warning('Cookies expired, please update the cookies')


def login():
    req = s.get(url)
    captcha_url = re.findall(r'<img src="(.*?)"', req.text)[0]
    captcha_url = urljoin(url, captcha_url)
    req2 = s.get(captcha_url)
    with open(captcha_path, 'wb') as f:
        f.write(req2.content)
        logging.info('Captcha saved.')

    form_data = {}
    form_data['email'] = account['email']
    form_data['password'] = account['password']
    form_data['captcha_0'] = re.findall(r'name="captcha_0".*?value="(.*?)"', req.text)[0]
    form_data['csrfmiddlewaretoken'] = re.findall(r"name='csrfmiddlewaretoken' value='(.*?)'", req.text)[0]
    form_data['captcha_1'] = input('Please open captcha.png and input it:')

    req2 = s.post(post_url, form_data, allow_redirects=False)
    if req2.status_code != 302:
        logging.info('Login failed.')
        return False
    else:
        s.get(req2.url)
        logging.error('Login successfully.')
        save_cookies(s.cookies)
        return True


def main():
    if os.path.exists('readfree.cookies'):
        login_by_cookies()
    elif (cookies["csrftoken"] != "") & (cookies["sessionid"] != ""):
        process_cookies()
        login_by_cookies()
    else:
        while True:
            flag = login()
            if flag is True:
                break


if __name__ == '__main__':
    main()
