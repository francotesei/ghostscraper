import requests
import random
import time
from fake_useragent import UserAgent
from stem import Signal
from stem.control import Controller
from tenacity import retry, stop_after_attempt, wait_random
from typing import Optional, Dict, Any
from zeep import Client, Transport
import asyncio
import websockets

class GhostScraperSession:
    def __init__(
        self,
        tor_password: str,
        control_port: int = 9051,
        proxy_port: int = 9050,
        default_headers: Optional[Dict[str, str]] = None,
        use_random_user_agent: bool = True,
        mode: str = "REST",  # Now supports REST, SOCKET, SOAP
    ):
        self.tor_password = tor_password
        self.control_port = control_port
        self.proxy_port = proxy_port
        self.ua = UserAgent()
        self.default_headers = default_headers or {}
        self.use_random_user_agent = use_random_user_agent
        self.mode = mode.upper()
        if self.mode not in ["REST", "SOCKET", "SOAP"]:
            raise ValueError("Unsupported mode. Use 'REST', 'SOCKET', or 'SOAP'.")

    def renew_connection(self):
        with Controller.from_port(port=self.control_port) as controller:
            controller.authenticate(password=self.tor_password)
            controller.signal(Signal.NEWNYM)
            print("[GhostScraper] New IP requested through Tor.")

    def get_session(self) -> requests.Session:
        session = requests.Session()
        session.proxies = {
            'http': f'socks5h://127.0.0.1:{self.proxy_port}',
            'https': f'socks5h://127.0.0.1:{self.proxy_port}',
        }

        headers = self.default_headers.copy()
        if self.use_random_user_agent:
            headers["User-Agent"] = self.ua.random

        headers.setdefault("Accept-Language", "en-US,en;q=0.9")
        headers.setdefault("Accept", "application/json, text/html, */*;q=0.8")
        session.headers.update(headers)
        return session

    @retry(stop=stop_after_attempt(5), wait=wait_random(1, 5))
    def request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        timeout: int = 15,
        **kwargs
    ) -> requests.Response:
        if self.mode != "REST":
            raise NotImplementedError("This method supports only REST mode.")

        session = self.get_session()
        if headers:
            session.headers.update(headers)

        response = session.request(
            method=method.upper(),
            url=url,
            params=params,
            data=data,
            json=json,
            timeout=timeout,
            **kwargs
        )

        if response.status_code not in [200, 201, 202]:
            print(f"[GhostScraper] Status {response.status_code} on {method} {url}")
            raise Exception(f"Non-successful response: {response.status_code}")

        return response

    def fetch_text(self, url: str, **kwargs) -> str:
        response = self.request("GET", url, **kwargs)
        return response.text

    def get_current_ip(self) -> str:
        # Always use REST session for this, safe to ignore mode
        session = self.get_session()
        response = session.get("https://httpbin.org/ip", timeout=10)
        return response.text

    # ---------------- SOAP Support -----------------
    def soap_request(self, wsdl_url: str, operation: str, params: Dict[str, Any]):
        if self.mode != "SOAP":
            raise NotImplementedError("This method supports only SOAP mode.")

        session = self.get_session()
        transport = Transport(session=session)
        client = Client(wsdl=wsdl_url, transport=transport)

        service = getattr(client.service, operation)
        result = service(**params)
        print(f"[GhostScraper SOAP] Operation '{operation}' executed.")
        return result

    # ---------------- SOCKET Support -----------------
    async def socket_send(self, ws_url: str, message: str):
        if self.mode != "SOCKET":
            raise NotImplementedError("This method supports only SOCKET mode.")

        print(f"[GhostScraper SOCKET] Connecting to {ws_url}...")
        async with websockets.connect(ws_url) as websocket:
            await websocket.send(message)
            print(f"[GhostScraper SOCKET] Sent: {message}")
            response = await websocket.recv()
            print(f"[GhostScraper SOCKET] Received: {response}")
            return response
