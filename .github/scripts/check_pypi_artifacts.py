"""Report whether a PyPI release is missing any locally built artifacts."""

import argparse
import json
import shutil
import sys
from pathlib import Path


def prepare_artifacts(
    dist_dir: Path,
    publish_dir: Path,
    release_json: Path | None,
) -> bool:
    expected = {path.name for path in dist_dir.iterdir() if path.name.endswith((".whl", ".tar.gz"))}
    if not expected:
        raise RuntimeError("Build produced no wheel or source distribution")

    uploaded: set[str] = set()
    if release_json is not None:
        with release_json.open(encoding="utf-8") as response:
            uploaded = {file["filename"] for file in json.load(response)["urls"]}

    missing = sorted(expected - uploaded)
    if missing:
        print("Missing from PyPI: " + ", ".join(missing), file=sys.stderr)
        publish_dir.mkdir(parents=True, exist_ok=True)
        if any(publish_dir.iterdir()):
            raise RuntimeError(f"Publish directory is not empty: {publish_dir}")
        for filename in missing:
            shutil.copy2(dist_dir / filename, publish_dir / filename)
    else:
        print("All built artifacts are already published", file=sys.stderr)
    return bool(missing)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("dist_dir", type=Path)
    parser.add_argument("publish_dir", type=Path)
    parser.add_argument("--release-json", type=Path)
    args = parser.parse_args()
    print(
        str(
            prepare_artifacts(
                args.dist_dir,
                args.publish_dir,
                args.release_json,
            )
        ).lower()
    )


if __name__ == "__main__":
    main()
