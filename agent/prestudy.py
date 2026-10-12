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
REVISION_3_CONTEXT_LENGTH = 16384  # revision 3 = revision 2 settings with a 16k context window


def _load_model(model: str) -> None:
    subprocess.run([str(LMS), "unload", "--all"], capture_output=True, text=True)
    command = [str(LMS), "load", model, "-y"]
    if os.environ.get("STUDY_REVISION") == "3":
        command += ["--context-length", str(REVISION_3_CONTEXT_LENGTH)]
    subprocess.run(command, check=True, capture_output=True, text=True)


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
    return OUTPUT_DIRECTORY / f"{model.replace('/', '_')}__{case}__t{trial}{'' if os.environ.get('STUDY_REVISION', '1') == '1' else '__r' + os.environ['STUDY_REVISION']}.log"


def main() -> None:
    """Usage: prestudy.py [--revision 2|3|4 MODEL...]; revision 1 is the original thinking-default run."""
    arguments = sys.argv[1:]
    revision = "1"
    models = CANDIDATE_MODELS
    if arguments[:2] in (["--revision", "2"], ["--revision", "3"], ["--revision", "4"]):
        revision, models = arguments[1], tuple(arguments[2:])
    os.environ["STUDY_REVISION"] = revision
    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    ledger_path = OUTPUT_DIRECTORY / {"1": "ledger.jsonl", "2": "ledger_r2.jsonl", "3": "ledger_r3.jsonl", "4": "ledger_r4.jsonl"}[revision]
    done = set()
    if ledger_path.exists():
        for line in ledger_path.read_text().splitlines():
            record = json.loads(line)
            if record["outcome"] == "completed":
                done.add((record["model"], record["case"], record["trial"]))
    for model in models:
        loaded = False
        for case in CALIBRATION_CASES:
            for trial in range(1, TRIALS_PER_CASE + 1):
                if (model, case, trial) in done:
                    continue
                if not loaded and revision != "4":
                    _load_model(model)
                    loaded = True
                for attempt in range(1, MAX_INFRASTRUCTURE_ATTEMPTS + 1):
                    if revision != "4":
                        _ensure_model(model)
                    if not _emulator_healthy():
                        _restart_emulator()
                    started = monotonic()
                    try:
                        completed = subprocess.run(
                            [sys.executable, "main.py", "--case", case],
                            cwd=Path(__file__).resolve().parent,
                            env={**os.environ, "LM_STUDIO_MODEL": model, "PYDANTIC_AI_NO_BANNER": "1", "STUDY_REVISION": revision,
                                 **({"STUDY_PROVIDER": "anthropic", "ANTHROPIC_MODEL": model} if revision == "4" else {})},
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
                        "revision": revision,
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
