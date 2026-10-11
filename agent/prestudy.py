"""Run the Stage 14 model-selection pre-study: candidates x calibration cases x trials.

Configuration is fixed in code and in docs/stage_14_prestudy_config.md; nothing is tuned
per model or per case. Every attempt (including infrastructure failures) is logged.
"""

import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import urllib.request
from time import monotonic

from public_cases import CALIBRATION_CASES

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIRECTORY = PROJECT_ROOT / "results" / "prestudy"
LMS = Path.home() / ".lmstudio" / "bin" / "lms"

CANDIDATE_MODELS = (
    "qwen2.5-7b-instruct",
    "qwen/qwen3.5-9b",
    "qwen3.5-9b-claude-4.6-opus-reasoning-distilled",
)
TRIALS_PER_CASE = 3
MAX_INFRASTRUCTURE_ATTEMPTS = 3
DEVICE = "emulator-5556"
EMULATOR = Path.home() / "Library" / "Android" / "sdk" / "emulator" / "emulator"
AVD = "Medium_Phone_API_36-ext19"
ATTEMPT_TIMEOUT_SECONDS = 1500


def _load_model(model: str) -> None:
    subprocess.run([str(LMS), "unload", "--all"], capture_output=True, text=True)
    subprocess.run([str(LMS), "load", model, "-y"], check=True, capture_output=True, text=True)


def _server_up() -> bool:
    try:
        with urllib.request.urlopen("http://127.0.0.1:1234/v1/models", timeout=5) as response:
            return response.status == 200
    except Exception:
        return False


def _model_loaded(model: str) -> bool:
    listing = subprocess.run([str(LMS), "ps"], capture_output=True, text=True).stdout
    return model in listing


def _ensure_model(model: str) -> None:
    """Infrastructure upkeep: restart the LM Studio server / reload the model if needed."""
    if not _server_up():
        subprocess.run([str(LMS), "server", "start"], capture_output=True, text=True)
    if not _server_up() or not _model_loaded(model):
        _load_model(model)


def _emulator_healthy() -> bool:
    boot = subprocess.run(["adb", "-s", DEVICE, "shell", "getprop", "sys.boot_completed"], capture_output=True, text=True)
    package = subprocess.run(["adb", "-s", DEVICE, "shell", "pm", "path", "android"], capture_output=True, text=True)
    return boot.stdout.strip() == "1" and package.returncode == 0 and "package:" in package.stdout


def _restart_emulator() -> None:
    subprocess.run(["adb", "-s", DEVICE, "emu", "kill"], capture_output=True, text=True)
    time.sleep(10)
    subprocess.Popen(
        [str(EMULATOR), "-avd", AVD, "-no-window", "-no-audio", "-read-only", "-port", "5556"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True,
    )
    for _ in range(90):
        time.sleep(4)
        if _emulator_healthy():
            time.sleep(15)
            return


def _log_path(model: str, case: str, trial: int) -> Path:
    return OUTPUT_DIRECTORY / f"{model.replace('/', '_')}__{case}__t{trial}.log"


def main() -> None:
    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    ledger_path = OUTPUT_DIRECTORY / "ledger.jsonl"
    done = set()
    if ledger_path.exists():
        for line in ledger_path.read_text().splitlines():
            record = json.loads(line)
            if record["outcome"] == "completed":
                done.add((record["model"], record["case"], record["trial"]))
    for model in CANDIDATE_MODELS:
        loaded = False
        for case in CALIBRATION_CASES:
            for trial in range(1, TRIALS_PER_CASE + 1):
                if (model, case, trial) in done:
                    continue
                if not loaded:
                    _load_model(model)
                    loaded = True
                for attempt in range(1, MAX_INFRASTRUCTURE_ATTEMPTS + 1):
                    _ensure_model(model)
                    if not _emulator_healthy():
                        _restart_emulator()
                    started = monotonic()
                    try:
                        completed = subprocess.run(
                            [sys.executable, "main.py", "--case", case],
                            cwd=Path(__file__).resolve().parent,
                            env={**os.environ, "LM_STUDIO_MODEL": model, "PYDANTIC_AI_NO_BANNER": "1"},
                            capture_output=True,
                            text=True,
                            timeout=ATTEMPT_TIMEOUT_SECONDS,
                        )
                        output, code = completed.stdout + completed.stderr, completed.returncode
                    except subprocess.TimeoutExpired as error:
                        output, code = f"TIMEOUT after {ATTEMPT_TIMEOUT_SECONDS}s\n{error.stdout or ''}", -1
                    _log_path(model, case, trial).write_text(output, encoding="utf-8")
                    run_id = re.search(r"^Run ID: (\S+)", output, re.MULTILINE)
                    record = {
                        "model": model,
                        "case": case,
                        "trial": trial,
                        "attempt": attempt,
                        "outcome": "completed" if code == 0 else "infrastructure_failure",
                        "run_id": run_id.group(1) if run_id else None,
                        "wall_seconds": round(monotonic() - started, 1),
                        "failure": None if code == 0 else output.strip().splitlines()[-1][:300] if output.strip() else "no output",
                    }
                    with ledger_path.open("a") as ledger:
                        ledger.write(json.dumps(record) + "\n")
                    print(record, flush=True)
                    if code == 0:
                        break


if __name__ == "__main__":
    main()
