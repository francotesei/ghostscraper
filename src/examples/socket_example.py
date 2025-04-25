from ghostscraper import GhostScraperSession
import asyncio
import time
import os
import dotenv

dotenv.load_dotenv()

tor_password = os.getenv("TOR_PASSWORD")
scraper = GhostScraperSession(tor_password=tor_password, mode="SOCKET")

async def run_socket_example():
    # Rotate IP before connecting to the WebSocket
    scraper.renew_connection()
    time.sleep(5)
    current_ip = scraper.get_current_ip()
    print(f"[GhostScraper] Current IP: {current_ip.strip()}")
    ws_url = "wss://echo.websocket.org"  # Example echo WebSocket server
    message = "Hello from GhostScraper WebSocket mode!"
    response = await scraper.socket_send(ws_url=ws_url, message=message)
    print(f"[SOCKET Example] Echoed response: {response}")

def main():
    asyncio.run(run_socket_example())

if __name__ == "__main__":
    main()
