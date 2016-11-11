import re
from ghost import Ghost
from ghost import Error
from warnings import filterwarnings


class Cookie:
    def __init__(self, url):
        # log.msg('init cookieutil class ,will be get %s cookie information!' %url, log.INFO)
        gh = Ghost(download_images=False, display=False)
        try:
            gh.open(url)
            gh.open(url)
            gh.save_cookies("cookie.txt")
            gh.exit()
        except Error as e:
            print(e.__doc__)

    def getCookie(self):
        cookie = ''
        with open("cookie.txt") as f:
            temp = f.readlines()
            for index in temp:
                cookie += self.parse_oneline(index).replace('\"', '')
        return cookie[:-1]

    def parse_oneline(self, src):
        oneline = ''
        if re.search("Set-Cookie", src):
            oneline = src.split(';')[0].split(':')[-1].strip() + ';'
        return oneline
