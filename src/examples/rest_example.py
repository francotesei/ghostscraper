from ghostscraper import GhostScraperSession
import time
import os
import dotenv

dotenv.load_dotenv()

tor_password = os.getenv("TOR_PASSWORD")
def main():
    scraper = GhostScraperSession(tor_password=tor_password, mode="REST")
    scraper.renew_connection()
    time.sleep(5)
    print(scraper.get_current_ip())
    html = scraper.fetch_text("https://example.com")
    print("Fetched page successfully.")

if __name__ == "__main__":
    main()
