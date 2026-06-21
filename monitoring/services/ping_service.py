import subprocess
import platform
import re

class ConnectivityTester:

    def ping(self, target):

        if platform.system() == "Windows":
            cmd = ["ping", "-n", "4", target]
        else:
            cmd = ["ping", "-c", "4", target]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        output = result.stdout

        # Packet Loss
        loss = re.search(
            r'(\d+)%.*loss',
            output
        )

        packet_loss = loss.group(1) if loss else "100"

        # Latency
        if platform.system() == "Windows":

            latency = re.search(
                r'Average = (\d+)ms',
                output
            )

        else:

            latency = re.search(
                r'=\s[\d\.]+/([\d\.]+)/',
                output
            )

        avg_latency = (
            latency.group(1)
            if latency
            else "N/A"
        )

        return {
            "target": target,
            "packet_loss": packet_loss,
            "avg_latency": avg_latency,
            "status": (
                "online" 
                if packet_loss != "100" 
                else "offline"
                )
        }