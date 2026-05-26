import argparse
import json
import re
from pathlib import Path

ASCII_PATTERN = re.compile(rb"[\x20-\x7e]{6,}")
UTF16_PATTERN = re.compile(rb"(?:[\x20-\x7e]\x00){6,}")

PATTERN_MAP = {
    "URLs": re.compile(r"https?://[\w\.-:/?=&%#+]+", re.I),
    "Hosts": re.compile(r"\b([\w.-]+\.(?:com|com\.br|net|org|br|info|tv|cc|gov|edu))\b", re.I),
    "Scripts": re.compile(r"[\w/\\.-]+\.(?:php|asp|cgi|xml)", re.I),
    "SwfFiles": re.compile(r"[\w/\\.-]+\.swf", re.I),
    "DatabaseFiles": re.compile(r"[\w/\\.-]+\.(?:fdb|gdb)", re.I),
    "OCX": re.compile(r"[\w/\\.-]+\.ocx", re.I),
    "DLL": re.compile(r"[\w/\\.-]+\.dll", re.I),
    "FirebirdConnection": re.compile(r"DRIVER=Firebird/InterBase\\(r\\) driver;uid=[^;]+;pwd=[^;]+;\\s*DBNAME=[^\\s]+", re.I),
}

HOST_TEMPLATE = [
    "127.0.0.1 pegajogo.com",
    "127.0.0.1 www.pegajogo.com",
    "127.0.0.1 desktop.meusjogosonline.com",
    "127.0.0.1 www.meusjogosonline.com",
    "127.0.0.1 ads.xpg.com.br",
    "127.0.0.1 promote.orkut.com",
    "127.0.0.1 twitter.com",
]


def unique_ordered(items):
    seen = set()
    ordered = []
    for value in items:
        if value not in seen:
            seen.add(value)
            ordered.append(value)
    return ordered


def extract_strings(data: bytes, pattern: re.Pattern) -> list[str]:
    return [match.decode("latin1", errors="ignore") for match in pattern.findall(data)]


def gather_results(data: bytes) -> dict[str, list[str]]:
    ascii_strings = extract_strings(data, ASCII_PATTERN)
    utf16_strings = extract_strings(data, UTF16_PATTERN)
    all_strings = ascii_strings + utf16_strings

    results = {}
    for name, pattern in PATTERN_MAP.items():
        matches = []
        for s in all_strings:
            matches.extend(pattern.findall(s))
        results[name] = unique_ordered(matches)

    url_hosts = set()
    for url in results.get("URLs", []):
        parsed = re.search(r"https?://([\w.-]+)", url, re.I)
        if parsed:
            url_hosts.add(parsed.group(1))
    if url_hosts:
        results["Hosts"] = unique_ordered(results.get("Hosts", []) + sorted(url_hosts))
    return results


def write_json_report(results: dict[str, list[str]], output_path: Path):
    output_path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")


def print_report(results: dict[str, list[str]]):
    print("LegacyLabs String Triage Report")
    print("================================")
    for section, values in results.items():
        print(f"\n[{section}] {len(values)} items")
        for item in values[:20]:
            print(f"  - {item}")
        if len(values) > 20:
            print(f"  ... and {len(values) - 20} more")

    print("\nRecommended hosts entries:")
    for line in HOST_TEMPLATE:
        print(f"  {line}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Triage strings from PegaJogo.exe and generate a local-run report.")
    parser.add_argument("binary", nargs="?", default="../DataOriginal/executavel/PegaJogo.exe", help="Path to the PegaJogo executable")
    parser.add_argument("--json", dest="json", help="Write JSON report to this file")
    return parser.parse_args()


def main():
    args = parse_args()
    path = Path(args.binary)
    if not path.exists():
        raise FileNotFoundError(f"Binary not found: {path}")

    data = path.read_bytes()
    results = gather_results(data)
    print_report(results)

    if args.json:
        write_json_report(results, Path(args.json))
        print(f"Saved JSON report to {args.json}")


if __name__ == '__main__':
    main()
