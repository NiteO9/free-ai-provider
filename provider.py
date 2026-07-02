# provider.py
import requests
import json
import time
import random
import base64
import hashlib
import hmac
import yaml
from typing import Dict, Optional, List, Any
from datetime import datetime
import threading
# my telegram channel: https://t.me/tele_t
class RateLimiter:
    def __init__(self, rpm: int, rps: int):
        self.rpm = rpm
        self.rps = rps
        self.minute_window = 60.0
        self.second_window = 1.0
        self.minute_requests = []
        self.second_requests = []
        self.lock = threading.Lock()
# github: https://github.com/NiteO9
    def wait_if_needed(self):
        with self.lock:
            now = time.time()
            
            self.minute_requests = [t for t in self.minute_requests if now - t < self.minute_window]
            self.second_requests = [t for t in self.second_requests if now - t < self.second_window]
            
            if len(self.minute_requests) >= self.rpm:
                wait_time = self.minute_window - (now - self.minute_requests[0]) + 0.1
                time.sleep(wait_time)
                self.minute_requests = []
                self.second_requests = []
            
            if len(self.second_requests) >= self.rps:
                wait_time = self.second_window - (now - self.second_requests[0]) + 0.1
                time.sleep(wait_time)
                self.second_requests = []
            
            self.minute_requests.append(now)
            self.second_requests.append(now)


class ChatSmithProvider:
    def __init__(self, config_path: str = "config.json", provider_path: str = "provider.yaml"):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        with open(provider_path, 'r') as f:
            self.provider = yaml.safe_load(f)['provider']
        
        self.device_id = self.config['android']['device_id']
        self.access_token = None
        self.x_auth_token = None
        self.request_id = None
        
        self.rate_limiter = RateLimiter(
            rpm=self.provider['rpm'],
            rps=self.provider['rps']
        )
        # my telegram channel: https://t.me/tele_t
        self.challenge_url = self.provider['endpoints']['challenge'].format(
            project=self.config['firebase']['project'],
            app_id=self.config['firebase']['app_id']
        )
        self.token_url = self.provider['endpoints']['token']
        self.chat_url = self.provider['endpoints']['chat']

    def _generate_request_id(self) -> str:
        return f"{random.randint(1000000000000, 9999999999999)}{int(time.time() * 1000)}"

    def _get_challenge(self) -> Optional[str]:
        params = {'key': self.config['firebase']['api_key']}
        headers = {
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 15; RMX3834 Build/AP3A.240905.015.A2)',
            'Content-Type': 'application/json',
            'X-Firebase-Client': 'H4sIAAAAAAAA_6tWykhNLCpJSk0sKVayio7VUSpLLSrOzM9TslIyUqoFAFyivEQfAAAA',
            'X-Android-Package': self.config['android']['package'],
            'X-Android-Cert': self.config['android']['cert']
        }
        try:
            response = requests.post(self.challenge_url, params=params, json={}, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.json().get("challenge")
            return None
        except Exception:
            return None

    def _generate_x_auth_token(self, challenge: str) -> str:
        try:
            timestamp = int(time.time())
            data_to_sign = f"{challenge}|{self.device_id}|{timestamp}"
            signature = hmac.new(
                self.config['security']['secret_key'].encode('utf-8'),
                data_to_sign.encode('utf-8'),
                hashlib.sha256
            ).digest()
            combined = data_to_sign.encode('utf-8') + signature
            token = base64.b64encode(combined).decode('utf-8')
            return token.replace('+', '-').replace('/', '_').rstrip('=')
        except Exception:
            return self.config['security']['fallback_token']

    def authenticate(self) -> bool:
        challenge = self._get_challenge()
        self.x_auth_token = self._generate_x_auth_token(challenge) if challenge else self.config['security']['fallback_token']
        
        self.request_id = self._generate_request_id()
        payload = {
            "device_id": self.device_id,
            "order_id": "",
            "product_id": "",
            "purchase_token": "",
            "subscription_id": ""
        }
        headers = {
            'host': 'api.vulcanlabs.co',
            'x-vulcan-application-id': self.config['android']['package'],
            'x-vulcan-request-id': self.request_id,
            'x-auth-token': self.x_auth_token,
            'user-agent': 'Chat Smith Android, Version 8.251222.2(1211)',
            'Content-Type': 'application/json'
        }
        try:
            response = requests.post(self.token_url, json=payload, headers=headers, timeout=15)
            if response.status_code == 200:
                self.access_token = response.json().get("AccessToken")
                return True
            return False
        except Exception:
            return False

    def send_message(self, messages: List[Dict[str, str]], timeout: Optional[int] = None) -> Dict[str, Any]:
        self.rate_limiter.wait_if_needed()
        
        if not self.access_token:
            if not self.authenticate():
                return {"success": False, "error": "Authentication failed"}
        
        timeout = timeout or self.provider['timeout']
        self.request_id = self._generate_request_id()
        
        payload = {
            "usage_model": {
                "provider": self.provider['name'],
                "model": self.provider['model']
            },
            "user": self.device_id,
            "messages": messages,
            "nsfw_check": True
        }
        
        headers = {
            'User-Agent': 'Chat Smith Android, Version 8.251222.2(1211)',
            'x-auth-token': self.x_auth_token,
            'authorization': f"Bearer {self.access_token}",
            'x-firebase-appcheck-error': '-9: Integrity API error (-9)',
            'x-vulcan-application-id': self.config['android']['package'],
            'x-vulcan-request-id': self.request_id,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        try:
            response = requests.post(self.chat_url, json=payload, headers=headers, timeout=timeout)
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "status": response.status_code, "response": response.text[:500]}
        except requests.exceptions.Timeout:
            return {"success": False, "error": "Request timeout"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def chat(self, user_message: str, system_prompt: Optional[str] = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_message})
        
        response = self.send_message(messages)
        
        if not response.get("success"):
            return f"Error: {response.get('error', response.get('response', 'Unknown error'))}"
        
        try:
            return response["data"]["choices"][0]["Message"]["content"]
        except (KeyError, IndexError):
            try:
                return response["data"]["choices"][0]["message"]["content"]
            except (KeyError, IndexError):
                return "Error: Invalid response structure"