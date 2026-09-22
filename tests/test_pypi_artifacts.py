"""Offline tests for partial PyPI release recovery."""

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).parents[1] / ".github" / "scripts" / "check_pypi_artifacts.py"
WHEEL = "polymarket_us-1.0.0-py3-none-any.whl"
SDIST = "polymarket_us-1.0.0.tar.gz"


def build_artifacts(tmp_path: Path) -> Path:
    dist = tmp_path / "dist"
    dist.mkdir()
    (dist / WHEEL).write_bytes(b"wheel from current build")
    (dist / SDIST).write_bytes(b"sdist from current build")
    return dist


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_release(
    tmp_path: Path,
    entries: list[dict[str, object]],
) -> Path:
    release = tmp_path / "release.json"
    release.write_text(json.dumps({"urls": entries}), encoding="utf-8")
    return release


def run_guard(
    dist: Path,
    publish_dir: Path,
    release: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    command = [sys.executable, str(SCRIPT), str(dist), str(publish_dir)]
    if release is not None:
        command.extend(["--release-json", str(release)])
    return subprocess.run(command, check=False, capture_output=True, text=True)


def staged_files(publish_dir: Path) -> set[str]:
    return {path.name for path in publish_dir.iterdir()} if publish_dir.exists() else set()


def test_absent_release_stages_both_artifacts(tmp_path: Path) -> None:
    dist = build_artifacts(tmp_path)
    publish_dir = tmp_path / "publish"

    result = run_guard(dist, publish_dir)

    assert result.returncode == 0
    assert result.stdout.strip() == "true"
    assert staged_files(publish_dir) == {WHEEL, SDIST}


def test_complete_release_skips_without_digest_comparison(tmp_path: Path) -> None:
    dist = build_artifacts(tmp_path)
    release = write_release(tmp_path, [{"filename": WHEEL}, {"filename": SDIST}])
    publish_dir = tmp_path / "publish"

    result = run_guard(dist, publish_dir, release)

    assert result.returncode == 0
    assert result.stdout.strip() == "false"
    assert staged_files(publish_dir) == set()


@pytest.mark.parametrize("uploaded,missing", [(WHEEL, SDIST), (SDIST, WHEEL)])
def test_matching_partial_release_stages_only_missing_artifact(
    tmp_path: Path,
    uploaded: str,
    missing: str,
) -> None:
    dist = build_artifacts(tmp_path)
    release = write_release(
        tmp_path,
        [{"filename": uploaded, "digests": {"sha256": sha256(dist / uploaded)}}],
    )
    publish_dir = tmp_path / "publish"

    result = run_guard(dist, publish_dir, release)

    assert result.returncode == 0
    assert result.stdout.strip() == "true"
    assert staged_files(publish_dir) == {missing}


@pytest.mark.parametrize("uploaded", [WHEEL, SDIST])
def test_mismatched_partial_release_fails_without_staging(
    tmp_path: Path,
    uploaded: str,
) -> None:
    dist = build_artifacts(tmp_path)
    release = write_release(
        tmp_path,
        [{"filename": uploaded, "digests": {"sha256": "0" * 64}}],
    )
    publish_dir = tmp_path / "publish"

    result = run_guard(dist, publish_dir, release)

    assert result.returncode != 0
    assert "SHA256 mismatch" in result.stderr
    assert staged_files(publish_dir) == set()


@pytest.mark.parametrize("digests", [None, {"sha256": "not-a-digest"}])
def test_partial_release_with_missing_or_invalid_digest_fails_closed(
    tmp_path: Path,
    digests: dict[str, str] | None,
) -> None:
    dist = build_artifacts(tmp_path)
    entry: dict[str, object] = {"filename": WHEEL}
    if digests is not None:
        entry["digests"] = digests
    release = write_release(tmp_path, [entry])
    publish_dir = tmp_path / "publish"

    result = run_guard(dist, publish_dir, release)

    assert result.returncode != 0
    assert "no valid SHA256" in result.stderr
    assert staged_files(publish_dir) == set()
