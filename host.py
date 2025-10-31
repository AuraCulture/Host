#!/usr/bin/env python3


__version__ = "0.1.2"

import argparse
import sys
from pathlib import Path

try:
    import requests
except ImportError: 
    print("\nPlease install dependencies first: pip install requests")
    raise

def upload_to_catbox(file_path: Path, userhash: str | None = None, timeout: int = 60) -> str:

    api_url = "https://catbox.moe/user/api.php"
    data = {"reqtype": "fileupload"}

    if userhash:
        data["userhash"] = userhash

    with file_path.open("rb") as fp:
        files = {"fileToUpload": (file_path.name, fp)}
        resp = requests.post(api_url, data=data, files=files, timeout=timeout)

    if resp.status_code != 200:
        raise RuntimeError(f"Upload failed: HTTP {resp.status_code}: {resp.text.strip()}")

    text = resp.text.strip()
    if text.startswith("https://"):
        return text

    raise RuntimeError(f"Upload failed: unexpected response: {text}")

def copy_to_clipboard(text: str) -> bool:
    """Try to copy text to clipboard. Returns True when successful, False otherwise."""
    try:
        import pyperclip
    except Exception:
        return False

    try:
        pyperclip.copy(text)
        return True
    except Exception:
        return False

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="host",
        description="Upload files to Catbox.moe and print direct link."
    )
    p.add_argument("file", help="Path to file to upload")
    p.add_argument(
        "-c", "--copy",
        action="store_true",
        help="Copy returned link to clipboard (requires pyperclip)"
    )
    p.add_argument("--userhash", help="Optional Catbox userhash (if you have an account)")
    p.add_argument("--timeout", type=int, default=60, help="Request timeout in seconds")
    p.add_argument("--version", action="version", version=__version__)
    return p

def main(argv=None) -> int:
    argv = argv or sys.argv[1:]
    parser = build_parser()
    args = parser.parse_args(argv)

    path = Path(args.file)
    if not path.exists() or not path.is_file():
        print(f"File not found: {path}")
        return 2

    try:
        link = upload_to_catbox(path, userhash=args.userhash, timeout=args.timeout)
    except Exception as e:
        print(f"Upload error: {e}")
        return 1

    print(link)

    if args.copy:
        ok = copy_to_clipboard(link)
        if ok:
            print("(copied to clipboard)")
        else:
            print("(could not copy — install pyperclip: pip install pyperclip)")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
