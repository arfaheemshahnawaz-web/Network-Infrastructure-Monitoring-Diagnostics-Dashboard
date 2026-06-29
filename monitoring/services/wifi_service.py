import platform
import subprocess
import re


class WiFiService:

    @staticmethod
    def scan():

        system = platform.system()

        if system == "Windows":
            return WiFiService._scan_windows()

        elif system == "Linux":
            return WiFiService._scan_linux()

        return []

    @staticmethod
    def _scan_windows():

        result = subprocess.run(
            [
                "netsh",
                "wlan",
                "show",
                "networks",
                "mode=bssid"
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

        return WiFiService._parse_windows(result.stdout)

    @staticmethod
    def _scan_linux():

        result = subprocess.run(
            [
                "nmcli",
                "-f",
                "SSID,SIGNAL,CHAN,SECURITY",
                "dev",
                "wifi"
            ],
            capture_output=True,
            text=True
        )

        return WiFiService._parse_linux(result.stdout)

    @staticmethod
    def _parse_windows(output):

        networks = []
        current = None

        for raw_line in output.splitlines():

            line = raw_line.strip()

            ssid_match = re.match(
                r"^SSID\s+\d+\s*:\s*(.+)$",
                line
            )

            if ssid_match:

                if current:
                    networks.append(current)

                current = {
                    "ssid": ssid_match.group(1),
                    "signal": 0,
                    "channel": 0,
                    "security": "",
                    "band": "",
                    "bssid": "",
                }

                continue

            if current is None:
                continue

            if line.startswith("Authentication"):
                current["security"] = line.split(":", 1)[1].strip()

            elif re.match(r"^BSSID\s+\d+", line):
                current["bssid"] = line.split(":", 1)[1].strip()

            elif line.startswith("Signal"):
                match = re.search(r"(\d+)", line)
                if match:
                    current["signal"] = int(match.group(1))

            elif line.startswith("Band"):
                current["band"] = line.split(":", 1)[1].strip()

            elif line.startswith("Channel"):
                match = re.search(r"(\d+)", line)
                if match:
                    current["channel"] = int(match.group(1))

        if current:
            networks.append(current)

        networks.sort(
            key=lambda x: x["signal"],
            reverse=True
        )

        return networks

    @staticmethod
    def _parse_linux(output):

        networks = []

        lines = output.splitlines()

        for line in lines[1:]:

            parts = line.split()

            if len(parts) >= 4:

                security = " ".join(parts[3:])

                networks.append({
                    "ssid": parts[0],
                    "signal": int(parts[1]),
                    "channel": int(parts[2]),
                    "security": security,
                    "band": "",
                    "bssid": "",
                })

        networks.sort(
            key=lambda x: x["signal"],
            reverse=True
        )

        return networks