import subprocess
import re


def ping_host(host, count=4):

    try:

        result = subprocess.run(
            [
                "ping",
                "-n",
                str(count),
                host
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            timeout=30
        )

        output = result.stdout

        packet_loss = None
        average_latency = None

        # Windows:
        # Packets: Sent = 4, Received = 4, Lost = 0 (0% loss)

        loss_match = re.search(
            r"\((\d+)%\s*loss\)",
            output,
            re.IGNORECASE
        )

        if loss_match:
            packet_loss = int(loss_match.group(1))

        # Approximate average:
        # Average = 12ms
        latency_match = re.search(
            r"Average\s*=\s*(\d+)ms",
            output,
            re.IGNORECASE
        )

        if latency_match:
            average_latency = int(
                latency_match.group(1)
            )

        return {
            "success": result.returncode == 0,
            "host": host,
            "packet_loss": packet_loss,
            "average_latency": average_latency
        }

    except subprocess.TimeoutExpired:

        return {
            "success": False,
            "host": host,
            "packet_loss": 100,
            "average_latency": None
        }