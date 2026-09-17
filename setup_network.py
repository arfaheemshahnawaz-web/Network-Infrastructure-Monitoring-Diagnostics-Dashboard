import ipaddress
import socket


def get_lan_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        sock.connect(("8.8.8.8", 80))
        return sock.getsockname()[0]
    finally:
        sock.close()


def get_network(lan_ip):
    # Your LAN currently uses /24.
    network = ipaddress.ip_network(
        f"{lan_ip}/24",
        strict=False,
    )

    return str(network)


def create_config():
    lan_ip = get_lan_ip()
    network = get_network(lan_ip)

    with open(".env.docker.local", "w", encoding="utf-8") as file:
        file.write(
            f"DISCOVERY_NETWORK={network}\n"
            f"DISCOVERY_AGENT_HOST={lan_ip}\n"
            f"DISCOVERY_AGENT_PORT=8765\n"
        )

    print("Network configuration created.")
    print(f"LAN IP: {lan_ip}")
    print(f"Network: {network}")


if __name__ == "__main__":
    create_config()