"""Report whether a PyPI release is missing any locally built artifacts."""

import argparse
import json
import sys
from pathlib import Path


def publish_required(dist_dir: Path, release_json: Path) -> bool:
    expected = {path.name for path in dist_dir.iterdir() if path.name.endswith((".whl", ".tar.gz"))}
    if not expected:
        raise RuntimeError("Build produced no wheel or source distribution")

    with release_json.open(encoding="utf-8") as response:
        uploaded = {file["filename"] for file in json.load(response)["urls"]}

    missing = sorted(expected - uploaded)
    if missing:
        print("Missing from PyPI: " + ", ".join(missing), file=sys.stderr)
    else:
        print("All built artifacts are already published", file=sys.stderr)
    return bool(missing)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("dist_dir", type=Path)
    parser.add_argument("release_json", type=Path)
    args = parser.parse_args()
    print(str(publish_required(args.dist_dir, args.release_json)).lower())


if __name__ == "__main__":
    main()
