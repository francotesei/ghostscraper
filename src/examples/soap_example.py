from ghostscraper import GhostScraperSession
import time
import os
import dotenv

dotenv.load_dotenv()

tor_password = os.getenv("TOR_PASSWORD")
def main():
    scraper = GhostScraperSession(tor_password=tor_password, mode="SOAP")
    
    # Rotate IP before making the SOAP request
    scraper.renew_connection()
    time.sleep(5)
    current_ip = scraper.get_current_ip()
    print(f"[GhostScraper] Current IP: {current_ip.strip()}")
    # Example WSDL: public calculator SOAP service
    wsdl_url = "http://www.dneonline.com/calculator.asmx?WSDL"
    operation = "Add"
    params = {"intA": 5, "intB": 10}
    result = scraper.soap_request(wsdl_url=wsdl_url, operation=operation, params=params)
    print(f"[SOAP Example] Result of Add operation: {result}")

if __name__ == "__main__":
    main()
