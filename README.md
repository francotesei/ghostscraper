# 👻 GhostScraper

**GhostScraper** is a Python wrapper for scrapers that enables anonymous and secure scraping by rotating IP addresses through the **Tor network**. It's designed for projects where you need to avoid IP blocking, fingerprinting, or tracking.

---

## 🚀 What is GhostScraper?

- 🌍 Hides your real IP using Tor.
- 🔁 Allows manual or scheduled IP rotation (Tor new circuit).
- 🕵️‍♂️ Randomizes headers (User-Agent and others) to avoid bot detection.
- 🛡️ Implements automatic retries with backoff using `tenacity`.
- 📦 Designed to easily integrate into any scraper as a session wrapper.
- 🐳 Includes Dockerized Tor + automated configuration via `make`.

---

## 🛠️ Installation

Make sure you have [uv](https://github.com/astral-sh/uv) installed:

```bash
pip install uv
```

Clone the project and sync dependencies:

```bash
git clone https://github.com/your-username/ghostscraper.git
cd ghostscraper
uv pip sync
```

---

## 🧩 Basic Usage

```python
from ghostscraper.session import GhostScraperSession
import time

TOR_PASSWORD = "your_password"

scraper = GhostScraperSession(tor_password=TOR_PASSWORD)

# Rotate IP (request a new Tor circuit)
scraper.renew_connection()
time.sleep(5)  # Give Tor time to activate the new circuit

# Get the current external IP
print(scraper.get_current_ip())

# Fetch a webpage
html = scraper.fetch("https://example.com")
print(html)
```

Or run the included example:

```bash
uv run ghostscraper-rest-example
```

---

## ⚙️ Tor Configuration (Automated with Makefile)

GhostScraper requires **Tor** running and accessible on port `9050` (SOCKS5 proxy) and `9051` (ControlPort).  
You can fully manage this with the provided **Makefile** (no need to install Tor manually).

### 🧰 Available `make` commands:

| Command                    | Description                                   |
|----------------------------|-----------------------------------------------|
| `make build`               | Build the Docker image for Tor               |
| `make run`                 | Run the Tor container (exposes 9050, 9051)   |
| `make stop`                | Stop and remove the Tor container            |
| `make restart`             | Restart the Tor container                    |
| `make logs`                | View the Tor container logs                  |
| `make check`               | Check if Tor SOCKS5 proxy is working         |
| `make generate-password TOR_PASSWORD=your_password` | Generate hashed password for Tor using Docker |
| `make configure-torrc TOR_PASSWORD=your_password TORRC_PATH=torrc` | Generate hash and write `torrc` automatically |

---

### ⚡ Example: Generate Tor password hash
```bash
make generate-password TOR_PASSWORD=<MYPASSWORD>
```

### ⚡ Example: Auto-configure your `torrc`:
```bash
make configure-torrc TOR_PASSWORD=<MYPASSWORD> TORRC_PATH=torrc
```

This creates a `torrc` file like:
```
ControlPort 9051
CookieAuthentication 0
HashedControlPassword 16:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

---

## 🐳 Running Tor with Docker

Build and run Tor via Docker:

```bash
make build
make run
```

Check if it's working:

```bash
make check
```

---

## 🧪 Testing

Place your tests inside the `tests/` folder and run them using `pytest`:

```bash
uv pip install pytest
pytest
```

---

## 🛡️ Legal Disclaimer

The use of scraping techniques may be restricted by website terms of service or local regulations. **GhostScraper is a technical tool** — misuse is the sole responsibility of the user.

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests for improvements, bug fixes, or new features.

---

## 📄 License

MIT License.

---

### 💻 Author

> Franco Tesei – [ftesei96@gmail.com](mailto:ftesei96@gmail.com)
