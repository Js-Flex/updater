import tls_client
import random
import string
import time
import re
import threading
import json
import colorama
import ctypes
from websocket import WebSocket
from modules.utils import Utils
from modules.logging import Log
from modules.captcha import Captcha
from modules.extra import UI
import requests


class Discord:
    global unlocked
    global locked
    global st
    
    def __init__(self) -> None:
        self.data = configuration
        self.proxy = random.choice(loaded_proxies)

        self.ua_version = ua_version
        self.ua = ua
        self.sec_ch_ua = sec_ch_ua

        self.session = tls_client.Session(client_identifier=f"chrome_{self.ua_version}", random_tls_extension_order=True)
        self.session.proxies = {
            'https': f"http://{self.proxy}",
            'http': f"http://{self.proxy}"
        }
        self.ws = WebSocket()

        self.bios = loaded_bios if self.data['bio'] else []
        self.cap_key = self.data['captcha_api_key']
        self.toggle_errors = self.data['show_errors']

        self.lock = threading_lock
        self.capabilities = 16381
        self.build_num = build_num
        self.x_sup = x_sup

        self.rl = "The resource is being rate limited."
        self.locked = "You need to verify your account in order to perform this action"
        self.captcha_detected = "captcha-required"

        if self.data['random_username']:
            self.username = "".join(random.choice(string.ascii_letters) for x in range(random.randint(6, 8)))
        else:
            self.username = random.choice(loaded_usernames)

        self.email = "".join(random.choice(string.ascii_letters) for x in range(random.randint(6, 8)))
        self.email += str("".join(str(random.randint(1, 9) if random.randint(1, 2) == 1 else random.choice(string.ascii_letters)) for x in range(int(random.randint(6, 8)))) )
        self.email += random.choice(["@gmail.com", "@outlook.com"])

        if self.data['password'] == "":
            self.password = "".join(random.choice(string.digits) if random.randint(1, 2) == 1 else random.choice(string.ascii_letters) for x in range(random.randint(8, 24))) + "".join("" if random.randint(1, 2) == 1 else random.choice(["@", "$", "%", "*", "&", "^"]) for x in range(1, 6))
        else:
            self.password = self.data['password']

    @staticmethod
    def display_stats():
        while True:
            if locked == 0 and unlocked == 0:
                ur = "0.00%"
            elif unlocked > 0 and locked == 0:
                ur = "100.0%"
            elif locked > 0 and unlocked == 0:
                ur = "0.00%"
            else:
                ur = f"{round(100 - round(locked/unlocked * 100, 2), 2)}%"
            ctypes.windll.kernel32.SetConsoleTitleW(f"[GITHUB] Pr0t0n's Generator | Unlocked: {unlocked} | Locked: {locked} | Unlock Rate: {ur} | Threads: {threading.active_count() - 2} | Time: {round(time.time() - st, 2)}s | github.com/pr0t0ns")
            time.sleep(0.5)

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
            # Attempt to fetch the registration page, retry if there are issues.
            retries = 3
            for _ in range(retries):
                try:
                    response = self.session.get(url)  # Removed timeout parameter here
                    if response.status_code == 200:
                        self.session.cookies = response.cookies
                        Log.good("Cookies fetched successfully.")
                        return
                    else:
                        Log.bad(f"Error Fetching Cookies: Received Status Code {response.status_code}")
                        time.sleep(2)  # Retry after a brief pause
                except Exception as e:
                    Log.bad(f"Error during cookie fetch attempt: {str(e)}")
                    time.sleep(2)  # Retry after a brief pause
            Log.bad("Failed to fetch cookies after 3 retries.")
        except Exception as e:
            Log.bad(f"Error Fetching Cookies: {str(e)}")
        return None

    def check_token(self):
        global unlocked, locked
        url = "https://discord.com/api/v9/users/@me/affinities/users"
        try:
            response = self.session.get(url)
        except:
            Log.bad("Error Sending Requests to check token")
            return Discord().begin()
        if int(response.status_code) in (400, 401, 403):
            Log.bad(f"Locked Token ({colorama.Fore.RED}{self.token[:25]}..{colorama.Fore.RESET})")
            locked += 1
            return
        else:
            Log.amazing(f"Unlocked Token ({colorama.Fore.LIGHTBLACK_EX}{self.token[:25]}..{colorama.Fore.RESET})")    
            unlocked += 1
            return True

    def ConnectWS(self):
            try:
               self.ws.connect('wss://gateway.discord.gg/?encoding=json&v=9&compress=zlib-stream')
               self.ws.send(json.dumps({
                "op": 2,
                "d": {
                    "token": self.token,
                    "capabilities": self.capabilities,
                    "properties": {
                        "os": "Windows",
                        "browser": "Chrome",
                        "device": "",
                        "system_locale": "en-US",
                        "browser_user_agent": self.ua,
                        "browser_version": f"{self.ua_version}.0.0.0",
                        "os_version": "10",
                        "referrer": "",
                        "referring_domain": "",
                        "referrer_current": "",
                        "referring_domain_current": "",
                        "release_channel": "stable",
                        "client_build_number": build_num,
                        "client_event_source": None
                    },
                        "presence": {
                        "status": random.choice(['online', 'idle', 'dnd']),
                        "since": 0,
                        "activities": [],
                        "afk": False
                    },
                    "compress": False,
                    "client_state": {
                        "guild_versions": {},
                        "highest_last_message_id": "0",
                        "read_state_version": 0,
                        "user_guild_settings_version": -1,
                        "user_settings_version": -1,
                        "private_channels_version": "0",
                        "api_code_version": 0
                    }
                }
                }))
            except:
                Log.bad("Error Onlining Token")
                return
            Log.good(f"Onlined Token --> ({colorama.Fore.LIGHTBLACK_EX}{self.token[:20]}..{colorama.Fore.RESET})", symbol="O")
            return

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
            'x-context-properties': Utils.build_x_context_properties("Register"),
            'x-debug-options': 'bugReporterEnabled',
            'x-discord-locale': 'en-US',
            'x-discord-timezone': 'America/New_York',
            'x-super-properties': self.x_sup,
        }
        try:
            r = self.session.get(url)
            return r.json()['fingerprint']
        except:
            Log.bad("Error Fetching Fingerprint")
            return Discord().begin()

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
                'x-captcha-key': str(Captcha.solve(user_agent=self.ua, api_key=self.data['captcha_api_key'], proxy=self.session.proxies['http'], service=self.data['captcha_service'])),
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
        except Exception:
            print(r.json())
            Log.bad("Error Creating Account!")
            return Discord().begin()

        self.session.headers = {
            'authority': 'discord.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': self.token,
            'content-type': 'application/json',
            'origin': 'https://discord.com',
            'referer': 'https://discord.com/channels/@me',
            'sec-ch-ua': self.sec_ch_ua,
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': self.ua,
            'x-captcha-key': str(Captcha.solve(user_agent=self.ua, api_key=self.data['captcha_api_key'], proxy=self.session.proxies['http'], service=self.data['captcha_service'])),
            'x-debug-options': 'bugReporterEnabled',
            'x-discord-locale': 'en-US',
            'x-discord-timezone': 'America/New_York',
            'x-super-properties': self.x_sup,
        }
        Log.good(f"Account Created: ({self.email})")
        self.get_cookies()
        self.check_token()
        self.ConnectWS()

    def begin(self):
        self.fp = self.get_fingerprint()
        self.get_cookies()
        self.create_acct()
