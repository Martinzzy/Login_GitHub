import requests
import chardet
import re
import http.cookiejar as cookielib
from requests.exceptions import ConnectionError
import http.cookiejar as cookielib


class GitHubLogin(object):

    def __init__(self):
        self.url = 'https://github.com/login'
        self.login_url = 'https://github.com/session'
        self.headers = {
            'Host':'github.com',
            'Referer':'https://github.com/',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
            }
        self.session = requests.session()
        self.session.cookies = cookielib.LWPCookieJar(filename='github_cookie')


    def load_cookie(self):
        try:
            self.session.cookies.load(ignore_discard=True)
        except:
            print('cookies加载失败')


    def isLogin(self):
        self.load_cookie()
        url = 'https://github.com/'
        response = self.session.get(url,headers=self.headers)
        if 'GitHub的昵称' in response.text:
            return True
        else:
            return False


    def login(self,username,passwd):
        try:
            try:
                from_data = {
                    'authenticity_token': '',
                    'commit': 'Sign+in',
                    'login': username,
                    'password': passwd,
                    'utf8': '✓'
                }
                res = self.session.get(self.url, headers=self.headers)
                res.encoding = chardet.detect(res.content)['encoding']
                result = res.text
                reg = r'name="authenticity_token" value="(.*?)"'
                pattern = re.compile(reg)
                token = re.findall(pattern, result)[0]
                from_data.update({'authenticity_token': token})
            except  ConnectionError:
                print('获取token失败')
                return None
            res = self.session.post(self.login_url,data=from_data,headers=self.headers)
            res.encoding = chardet.detect(res.content)['encoding']
            if 'Martinzzy' in res.text:
                print('###登陆成功！##')
            self.session.cookies.save()
        except ConnectionError:
            print('登录失败')


if __name__ == '__main__':
        github = GitHubLogin()
        if github.isLogin() == True:
            print('登陆成功')
        else:
            username = input('Please input your account:')
            passwd = input('Please input your passwd:')
            github.login(username,passwd)
