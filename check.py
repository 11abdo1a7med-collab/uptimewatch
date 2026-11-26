from pathlib import Path
import sys
import time

import requests

SITES_FILE = Path(__file__).with_name("sites.txt")
TIMEOUT = 5


def load_sites(file_path: Path) -> list[str]:
    """Load URLs, ignoring blank lines and comments."""
    if not file_path.exists():
        raise FileNotFoundError(f"Sites file not found: {file_path}")

    return [
        line.strip()
        for line in file_path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]


def check_site(url: str) -> dict:
    """Return the availability result and response time for one URL."""
    start = time.perf_counter()

    try:
        response = requests.get(url, timeout=TIMEOUT)
        elapsed_ms = (time.perf_counter() - start) * 1000
        is_up = response.status_code < 400

        return {
            "url": url,
            "status": "UP" if is_up else "DOWN",
            "status_code": str(response.status_code),
            "response_time_ms": f"{elapsed_ms:.2f}",
        }

    except requests.exceptions.RequestException as error:
        elapsed_ms = (time.perf_counter() - start) * 1000
        return {
            "url": url,
            "status": "DOWN",
            "status_code": "N/A",
            "response_time_ms": f"{elapsed_ms:.2f}",
            "error": str(error),
        }


def print_results(results: list[dict]) -> None:
    """Print results in a readable table."""
    headers = ("WEBSITE", "STATUS", "HTTP", "RESPONSE TIME")
    rows = [
        (
            result["url"],
            result["status"],
            result["status_code"],
            f'{result["response_time_ms"]} ms',
        )
        for result in results
    ]

    widths = [
        max(len(headers[i]), *(len(row[i]) for row in rows))
        for i in range(len(headers))
    ]

    def format_row(row: tuple[str, ...]) -> str:
        return " | ".join(value.ljust(widths[i]) for i, value in enumerate(row))

    print(format_row(headers))
    print("-+-".join("-" * width for width in widths))
    for row in rows:
        print(format_row(row))


def main() -> int:
    try:
        sites = load_sites(SITES_FILE)
    except (OSError, UnicodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    if not sites:
        print("ERROR: sites.txt does not contain any URLs.", file=sys.stderr)
        return 1

    results = [check_site(url) for url in sites]
    print_results(results)

    down_count = sum(result["status"] == "DOWN" for result in results)
    print(f"\nSummary: {len(results) - down_count} UP, {down_count} DOWN")

    return 1 if down_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
