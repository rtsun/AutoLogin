# For my roommate Kang

import requests
import re
import os
import time
import logging
import subprocess
import http.cookiejar
from urllib.parse import urljoin
from config import account

loginUrl = 'http://aixinwu.sjtu.edu.cn/index.php/login'
captUrl = 'https://jaccount.sjtu.edu.cn/jaccount/captcha?'
postUrl = 'https://jaccount.sjtu.edu.cn/jaccount/ulogin'
homeUrl = 'http://aixinwu.sjtu.edu.cn/index.php/home'
currentPath = os.path.dirname(os.path.abspath(__file__))
accountPath = os.path.join(currentPath, "account.dat")
cookiesPath = os.path.join(currentPath, "aixinwu.cookies")
logfilePath = os.path.join(currentPath, "aixinwu.log")
captPath = os.path.join(currentPath, "captcha.png")


def checkNetwork(address):
    p = subprocess.Popen(["ping.exe", address],
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         shell=True)
    out = p.stdout.read()
    if 'TTL' in out.decode('gbk'):
        return 1


class SJTUer(object):
    def __init__(self):
        self.headers = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/51.0'}
        self.s = requests.session()
        self.s.headers.update(self.headers)
        self.usr = account['username']
        self.psw = account['password']

    def login_by_cookies(self):
        if os.path.exists(cookiesPath):
            logging.info("cookies file exist.")
        else:
            logging.info("cookies file does't exist.")
            return
        ck = self.load_cookies()
        if ck is None:
            logging.error("cookies not loaded.")
            return
        self.s.cookies.update(ck)
        info = self.s.get(loginUrl).text
        self.save_cookies(self.s.cookies)
        if self.usr in info:
            return 1

    def save_cookies(self, cookies):
        save_cj = http.cookiejar.LWPCookieJar()
        save_ck = {c.name: c.value for c in cookies}
        requests.utils.cookiejar_from_dict(save_ck, save_cj)
        save_cj.save(cookiesPath, ignore_expires=True, ignore_discard=True)

    def load_cookies(self):
        try:
            load_cj = http.cookiejar.LWPCookieJar()
            load_cj.load(cookiesPath, ignore_expires=True, ignore_discard=True)
            load_ck = requests.utils.dict_from_cookiejar(load_cj)
            return load_ck
        except:
            return

    def process_cookies(self):
        """
        To process the very first cookies.
        """
        save_cj = http.cookiejar.LWPCookieJar()
        save_ck = {
            "JASiteCookie": "",
            "PHPSESSID": "",
            "__utma": "",
            "__utmb": "",
            "__utmc": "",
            "__utmt": "1",
            "__utmv": "",
            "__utmz": "",
            "ci_session": ""
        }
        requests.utils.cookiejar_from_dict(save_ck, save_cj)
        save_cj.save(cookiesPath, ignore_expires=True, ignore_discard=True)

    def login(self):
        try:
            html0 = self.s.get(loginUrl).text
            url1 = re.findall(r'URL=(.*?)">', html0)[0]
            html = self.s.get(url1).text
            self.download(captUrl)
            formdata = {}
            formdata['user'] = self.usr
            formdata['pass'] = self.psw
            formdata['sid'] = re.findall(r'name="sid" value="(.+?)"', html)[0]
            formdata['returl'] = re.findall(r'name="returl" value="(.+?)"', html)[0]
            formdata['se'] = re.findall(r'name="se" value="(.+?)"', html)[0]
            formdata['v'] = re.findall(r'name="v" value="(.*?)"', html)[0]
            formdata['captcha'] = self.captcha_rec(captPath)
            login = self.s.post(postUrl, data=formdata, allow_redirects=False)
            redUrl = urljoin('https://jaccount.sjtu.edu.cn', login.headers['Location'], )
            redUrl2 = self.s.get(redUrl, allow_redirects=False).headers['Location']
            req = self.s.get(redUrl2, allow_redirects=False)
            redUrl3 = urljoin('http://aixinwu.sjtu.edu.cn', req.headers['Location'])
            self.s.get(redUrl3)  # 不知道为什么，要get两次。。
            self.s.get(redUrl3)  # 不知道为什么，要get两次。。
            info = self.s.get(homeUrl).text
            if self.usr in info:
                self.save_cookies(self.s.cookies)
                return 1
        except Exception as e:
            logging.error(date + " || " + str(e))
            return 0

    def captcha_rec(self, captcha):
        files = {
            'file': ('captcha.jpeg', open(captcha, 'rb'), 'image/jpeg')
        }
        req = requests.post('https://t.yctin.com/en/security/captcha-recognition/', files=files, headers=self.headers)

        return req.text.strip()  # strip之必要，mdzz

    def download(self, url):
        with open(captPath, "wb") as f:
            f.write(self.s.get(url).content)


logging.basicConfig(filename=logfilePath, level='DEBUG')
date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
logging.info("===============Log Started at " + date + "===============")

sjtuer = SJTUer()
if sjtuer.login_by_cookies() == 1:
    print("Login by cookies successfully!")
    logging.info("=============Login by cookies successfully at %s =============" % date)
elif sjtuer.login() == 1:
    print('Login successfully!')
    logging.info("=============Login successfully at %s =============" % date)
else:
    os._exit(0)
