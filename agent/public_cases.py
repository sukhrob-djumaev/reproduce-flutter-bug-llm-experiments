"""Prepare, launch, and reset public calibration cases in scratch Flutter workspaces.

The case source is copied byte-for-byte from the curated pool. The only harness
additions are the Android scaffold, a ``flutter_driver`` dependency, and a wrapper
entrypoint that enables the Driver extension; no case code is edited.
"""

import asyncio
from contextlib import asynccontextmanager
from pathlib import Path
import re
import shutil
import subprocess

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ACCEPTED_DIRECTORY = PROJECT_ROOT / "curation" / "accepted"
WORKSPACES_DIRECTORY = PROJECT_ROOT / "results" / "workspaces"
ISSUES_DIRECTORY = PROJECT_ROOT / "issues"

CALIBRATION_CASES = (
    "S12-001",
    "S12-003",
    "S12-004",
    "S13-002",
    "S13-005",
    "S13B-002",
    "S13B-003",
)

DRIVER_ENTRYPOINT = "lib/main_driver.dart"
DRIVER_ENTRYPOINT_SOURCE = """import 'package:flutter_driver/driver_extension.dart';

import 'main.dart' as app;

void main() {
  enableFlutterDriverExtension();
  app.main();
}
"""


def is_public_case(case: str) -> bool:
    return case in CALIBRATION_CASES


def issue_path(case: str) -> Path:
    return ISSUES_DIRECTORY / f"case_{case}.md"


def _source_directory(case: str) -> Path:
    matches = sorted(ACCEPTED_DIRECTORY.glob(f"*/{case}/source"))
    if len(matches) != 1:
        raise RuntimeError(f"Expected one curated source directory for {case}: {matches}")
    return matches[0]


def workspace_directory(case: str) -> Path:
    return WORKSPACES_DIRECTORY / case


def _run(command: list[str], cwd: Path) -> None:
    completed = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
    if completed.returncode != 0:
        raise RuntimeError(
            f"{' '.join(command)} failed in {cwd}:\n{completed.stdout[-2000:]}\n{completed.stderr[-2000:]}"
        )


def prepare_workspace(case: str) -> Path:
    """Create a fresh scratch Android project for the case; replaces any earlier one."""
    if not is_public_case(case):
        raise ValueError(f"{case} is not a Stage 14 calibration case")
    source = _source_directory(case)
    workspace = workspace_directory(case)
    if workspace.exists():
        shutil.rmtree(workspace)
    WORKSPACES_DIRECTORY.mkdir(parents=True, exist_ok=True)

    pubspec_text = (source / "pubspec.yaml").read_text(encoding="utf-8")
    name_match = re.search(r"^name:\s*(\S+)", pubspec_text, re.MULTILINE)
    if name_match is None:
        raise RuntimeError(f"No package name in {source / 'pubspec.yaml'}")
    _run(
        ["flutter", "create", "-e", "--platforms=android", "--project-name", name_match.group(1), case],
        WORKSPACES_DIRECTORY,
    )

    shutil.rmtree(workspace / "lib")
    shutil.copytree(source / "lib", workspace / "lib")
    shutil.copy2(source / "pubspec.yaml", workspace / "pubspec.yaml")
    if (source / "pubspec.lock").exists():
        shutil.copy2(source / "pubspec.lock", workspace / "pubspec.lock")
    # Harness-only: SDK packages outside the SDK workspace cannot resolve this key.
    pubspec = workspace / "pubspec.yaml"
    pubspec.write_text(
        re.sub(r"^resolution:\s*workspace\s*\n", "", pubspec.read_text(encoding="utf-8"), flags=re.MULTILINE),
        encoding="utf-8",
    )
    _run(["flutter", "pub", "add", "flutter_driver", "--sdk=flutter"], workspace)
    (workspace / DRIVER_ENTRYPOINT).write_text(DRIVER_ENTRYPOINT_SOURCE, encoding="utf-8")
    return workspace


def flutter_run_command(device: str) -> list[str]:
    """Command that launches the prepared workspace with the Driver entrypoint."""
    return ["flutter", "run", "-d", device, "--debug", "--print-dtd", "-t", DRIVER_ENTRYPOINT]


APP_START_TIMEOUT_SECONDS = 600


@asynccontextmanager
async def running_case(case: str, device: str):
    """Launch a fresh debug run of the prepared workspace and always stop it afterwards.

    A fresh process per trial is the reset procedure: no state survives between trials.
    """
    workspace = workspace_directory(case)
    if not (workspace / DRIVER_ENTRYPOINT).exists():
        prepare_workspace(case)
    process = await asyncio.create_subprocess_exec(
        *flutter_run_command(device),
        cwd=workspace,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )
    output: list[str] = []

    async def wait_until_ready() -> str:
        assert process.stdout is not None
        while True:
            line = await process.stdout.readline()
            if not line:
                raise RuntimeError("flutter run exited before the app was ready:\n" + "".join(output[-30:]))
            text = line.decode(errors="replace")
            output.append(text)
            match = re.search(r"Dart Tooling Daemon is available at: (ws://\S+)", text)
            if match:
                return match.group(1)

    async def drain() -> None:
        assert process.stdout is not None
        while await process.stdout.readline():
            pass

    try:
        dtd_uri = await asyncio.wait_for(wait_until_ready(), APP_START_TIMEOUT_SECONDS)
        drainer = asyncio.create_task(drain())
        yield workspace, dtd_uri
    finally:
        if process.returncode is None:
            try:
                assert process.stdin is not None
                process.stdin.write(b"q\n")
                await process.stdin.drain()
                await asyncio.wait_for(process.wait(), 30)
            except Exception:
                process.kill()
                await process.wait()
