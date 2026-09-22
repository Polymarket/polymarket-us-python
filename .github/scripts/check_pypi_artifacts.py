"""Report whether a PyPI release is missing any locally built artifacts."""

import argparse
import hashlib
import hmac
import json
import re
import shutil
import sys
from pathlib import Path

SHA256_PATTERN = re.compile(r"[0-9a-fA-F]{64}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as artifact:
        for chunk in iter(lambda: artifact.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def uploaded_artifacts(release_json: Path) -> dict[str, dict[str, object]]:
    with release_json.open(encoding="utf-8") as response:
        release = json.load(response)

    files = release.get("urls")
    if not isinstance(files, list):
        raise RuntimeError("PyPI release metadata has no urls list")

    uploaded: dict[str, dict[str, object]] = {}
    for file in files:
        if not isinstance(file, dict):
            raise RuntimeError("PyPI release metadata contains an invalid file entry")
        filename = file.get("filename")
        if not isinstance(filename, str) or not filename:
            raise RuntimeError("PyPI release metadata contains an invalid filename")
        if filename in uploaded:
            raise RuntimeError(f"PyPI release metadata contains duplicate filename: {filename}")
        uploaded[filename] = file
    return uploaded


def validate_uploaded_artifact(path: Path, metadata: dict[str, object]) -> None:
    digests = metadata.get("digests")
    remote_sha256 = digests.get("sha256") if isinstance(digests, dict) else None
    if not isinstance(remote_sha256, str) or SHA256_PATTERN.fullmatch(remote_sha256) is None:
        raise RuntimeError(f"PyPI release metadata has no valid SHA256 for: {path.name}")
    if not hmac.compare_digest(sha256(path), remote_sha256.lower()):
        raise RuntimeError(f"SHA256 mismatch for already-published artifact: {path.name}")


def prepare_artifacts(
    dist_dir: Path,
    publish_dir: Path,
    release_json: Path | None,
) -> bool:
    expected = {path.name for path in dist_dir.iterdir() if path.name.endswith((".whl", ".tar.gz"))}
    if not expected:
        raise RuntimeError("Build produced no wheel or source distribution")

    uploaded: dict[str, dict[str, object]] = {}
    if release_json is not None:
        uploaded = uploaded_artifacts(release_json)

    missing = sorted(expected - uploaded.keys())
    if not missing:
        print("All built artifacts are already published", file=sys.stderr)
        return False

    for filename in sorted(expected & uploaded.keys()):
        validate_uploaded_artifact(dist_dir / filename, uploaded[filename])

    print("Missing from PyPI: " + ", ".join(missing), file=sys.stderr)
    publish_dir.mkdir(parents=True, exist_ok=True)
    if any(publish_dir.iterdir()):
        raise RuntimeError(f"Publish directory is not empty: {publish_dir}")
    for filename in missing:
        shutil.copy2(dist_dir / filename, publish_dir / filename)
    return True


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
