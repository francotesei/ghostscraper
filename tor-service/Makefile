# Makefile for GhostScraper Tor Docker setup

IMAGE_NAME = ghostscraper-tor
CONTAINER_NAME = ghostscraper-tor
TOR_PORT_SOCKS = 9050
TOR_PORT_CONTROL = 9051
TOR_PASSWORD ?= your_password
TORRC_PATH ?= torrc  # Default location of your torrc file

.PHONY: build run stop restart logs clean check generate-password configure-torrc

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run the Tor container exposing SOCKS5 and ControlPort
run:
	docker run -d --name $(CONTAINER_NAME) \
		-p $(TOR_PORT_SOCKS):9050 \
		-p $(TOR_PORT_CONTROL):9051 \
		$(IMAGE_NAME)

# Stop the running container
stop:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

# Restart the container (stop + run)
restart: stop run

# Show container logs
logs:
	docker logs -f $(CONTAINER_NAME)

# Remove the Docker image and container
clean: stop
	docker rmi $(IMAGE_NAME) || true

# Check if Tor SOCKS5 proxy is working (basic check via curl)
check:
	@echo "Checking if Tor SOCKS5 proxy is up on 127.0.0.1:$(TOR_PORT_SOCKS)..."
	@curl --socks5-hostname 127.0.0.1:$(TOR_PORT_SOCKS) -s https://check.torproject.org/ | grep -q "Congratulations" && \
	echo "[✔] Tor is running and proxy is working!" || \
	(echo "[✘] Tor is NOT working properly!" && exit 1)

# Generate the HashedControlPassword using Docker (no local Tor installation required)
generate-password:
	@echo "Generating HashedControlPassword for: '$(TOR_PASSWORD)' using Docker..."
	@docker run --rm alpine:3.18 sh -c "apk add --no-cache tor > /dev/null && tor --hash-password '$(TOR_PASSWORD)'"

# Generate the hash and configure the torrc automatically
configure-torrc:
	@echo "Generating HashedControlPassword and writing to $(TORRC_PATH)..."
	@HASH=$$(docker run --rm alpine:3.18 sh -c "apk add --no-cache tor > /dev/null && tor --hash-password '$(TOR_PASSWORD)' | tail -n 1") && \
	echo "ControlPort 9051" > $(TORRC_PATH) && \
	echo "CookieAuthentication 0" >> $(TORRC_PATH) && \
	echo "HashedControlPassword $$HASH" >> $(TORRC_PATH) && \
	echo "[✔] torrc configured successfully with generated password hash!"

#make configure-torrc TOR_PASSWORD=<MYPASSWORD> TORRC_PATH=torrc
#make generate-password TOR_PASSWORD=<MYPASSWORD>
