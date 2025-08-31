#!/usr/bin/env python3
"""host — upload files to Catbox.moe and return direct link."""

import argparse
from pathlib import Path
import sys

try:
    import requests
except ImportError:
    print("Please install requests: pip install requests")
    raise

__version__ = "0.1.0"

def upload_to_catbox(file_path: Path):
    api_url = "https://catbox.moe/user/api.php"
    with file_path.open("rb") as fp:
        files = {"fileToUpload": (file_path.name, fp)}
        data = {"reqtype": "fileupload"}
        resp = requests.post(api_url, data=data, files=files)
    if resp.status_code == 200 and resp.text.startswith("https://"):
        return resp.text.strip()
    else:
        raise RuntimeError(f"Upload failed: {resp.text.strip()}")

def main():
    parser = argparse.ArgumentParser(description="Upload files to Catbox.moe")
    parser.add_argument("file", help="File path to upload")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.is_file():
        print(f"File not found: {path}")
        sys.exit(1)

    try:
        link = upload_to_catbox(path)
        print(link)
    except Exception as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
