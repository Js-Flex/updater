import tls_client
import random
import string
import json
import base64
from modules.utils import Utils
from modules.logging import Log

class Discord:
    def __init__(self) -> None:
        self.session = tls_client.Session(client_identifier="chrome_124", random_tls_extension_order=True)
        self.proxy = random.choice(loaded_proxies)  # Assuming `loaded_proxies` is a list of proxies
        self.session.proxies = {'https': f"http://{self.proxy}", 'http': f"http://{self.proxy}"}
        
        # Dynamic headers
        self.ua_version = "124"
        self.ua = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{self.ua_version}.0.0.0 Safari/537.36"
        self.sec_ch_ua = f'"Chromium";v="{self.ua_version}", "Google Chrome";v="{self.ua_version}", "Not-A.Brand";v="99"'

        # Initial placeholders
        self.x_sup = None
        self.fingerprint = None
        self.token = None

    def fetch_headers(self):
        """Automatically fetch necessary headers like x-super-properties, fingerprint, etc."""
        try:
            url = "https://discord.com/register"
            response = self.session.get(url)
            if response.status_code != 200:
                Log.bad("Failed to fetch registration page.")
                return

            # Fetch x-super-properties (Base64-encoded)
            self.x_sup = response.headers.get("x-super-properties")
            if not self.x_sup:
                Log.bad("x-super-properties not found in headers.")
                return

            # Fetch fingerprint
            self.fingerprint = self.get_fingerprint()
            if not self.fingerprint:
                Log.bad("Failed to fetch fingerprint.")
                return

            Log.good(f"Successfully fetched x-super-properties and fingerprint.")
        except Exception as e:
            Log.bad(f"Error fetching headers: {str(e)}")

    def get_fingerprint(self):
        """Get the fingerprint from Discord's API."""
        url = "https://discord.com/api/v9/experiments?with_guild_experiments=true"
        self.session.headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'referer': 'https://discord.com/register',
            'sec-ch-ua': self.sec_ch_ua,
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': self.ua,
        }
        try:
            response = self.session.get(url)
            if response.status_code == 200:
                return response.json()['fingerprint']
            else:
                Log.bad("Failed to fetch fingerprint.")
                return None
        except Exception as e:
            Log.bad(f"Error fetching fingerprint: {str(e)}")
            return None

    def create_acct(self):
        """Create a new account."""
        if not self.x_sup or not self.fingerprint:
            Log.bad("Missing required headers. Cannot create account.")
            return

        url = 'https://discord.com/api/v9/auth/register'
        display_name = "".join(random.choice(string.ascii_letters) for _ in range(random.randint(6, 8)))
        email = "".join(random.choice(string.ascii_letters) for _ in range(random.randint(6, 8)))
        email += str(random.randint(1000, 9999)) + "@gmail.com"
        password = "".join(random.choice(string.ascii_letters + string.digits + "@$%*&^") for _ in range(random.randint(8, 24)))

        payload = {
            'fingerprint': self.fingerprint,
            'email': email,
            'username': display_name,
            'password': password,
            'consent': True,
            'date_of_birth': f'{random.randint(1980, 2001)}-{random.randint(1, 10)}-{random.randint(1, 10)}',
        }
        
        self.session.headers = {
            'authority': 'discord.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://discord.com',
            'referer': 'https://discord.com/register',
            'sec-ch-ua': self.sec_ch_ua,
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': self.ua,
            'x-super-properties': self.x_sup,
            'x-fingerprint': self.fingerprint,
        }

        try:
            response = self.session.post(url, json=payload)
            if response.status_code == 200:
                self.token = response.json()['token']
                Log.good(f"Account created successfully! Token: {self.token}")
            else:
                Log.bad(f"Error creating account: {response.json()}")
        except Exception as e:
            Log.bad(f"Error creating account: {str(e)}")

    def begin(self):
        """Begin the process of fetching headers and creating accounts."""
        self.fetch_headers()
        self.create_acct()

# Run the script
if __name__ == "__main__":
    discord = Discord()
    discord.begin()
