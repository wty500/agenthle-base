'''
2026 New Year Keygen Challenge
Credit to: 52pojie
'''
import json
import logging
import os
from dataclasses import dataclass
from typing import Any, Dict

import cua_bench as cb
from tasks.common_config import GeneralTaskConfig

logger = logging.getLogger(__name__)


@dataclass
class TaskConfig(GeneralTaskConfig):
    TASK_TAG: str = "newyear_keygen"
    TASK_CATEGORY: str = "cybersecurity"
    OUTPUT_FILENAME: str = "keys.txt"

    @property
    def exe_path(self) -> str:
        return fr"{self.task_dir}\input\crackme.exe"

    @property
    def uids_path(self) -> str:
        return fr"{self.task_dir}\input\uids.txt"

    @property
    def reference_keys_path(self) -> str:
        return fr"{self.reference_dir}\keys.txt"

    @property
    def output_path(self) -> str:
        return fr"{self.remote_output_dir}\{self.OUTPUT_FILENAME}"

    @property
    def task_description(self) -> str:
        return f"""
Goal:
Recover the keygen logic used by the bundled Windows crackme and output the correct key for every UID.

Inputs:
- Executable to analyze: {self.exe_path}
- UID list: {self.uids_path}

Output:
- Save EXACTLY one UTF-8 text file to: {self.output_path}
- One key per line
- Preserve the same order as uids.txt
- Do not add extra commentary, numbering, or blank lines

Verification:
- Score is 1.0 only if the output file matches the reference answers exactly line by line.
"""

    def to_metadata(self) -> dict:
        metadata = super().to_metadata()
        metadata.update(
            {
                "exe_path": self.exe_path,
                "uids_path": self.uids_path,
                "reference_keys_path": self.reference_keys_path,
                "output_path": self.output_path,
                "output_filename": self.OUTPUT_FILENAME,
            }
        )
        return metadata


config = TaskConfig()


@cb.tasks_config(split="train")
def load():
    return [
        cb.Task(
            description=config.task_description,
            metadata=config.to_metadata(),
            computer={"provider": "computer", "setup_config": {"os_type": config.OS_TYPE}},
        )
    ]


@cb.setup_task(split="train")
async def start(task_cfg, session: cb.DesktopSession):
    out_dir = task_cfg.metadata["remote_output_dir"]
    exe_path = task_cfg.metadata["exe_path"]
    uids_path = task_cfg.metadata["uids_path"]

    logger.info("[newyear_keygen] start() begin")
    logger.info("[newyear_keygen] exe_path=%s", exe_path)
    logger.info("[newyear_keygen] uids_path=%s", uids_path)
    logger.info("[newyear_keygen] out_dir=%s", out_dir)

    try:
        await session.remove_file(out_dir)
        logger.info("[newyear_keygen] removed existing output dir")
    except Exception:
        logger.info("[newyear_keygen] output dir did not need removal")

    try:
        await session.makedirs(out_dir)
        logger.info("[newyear_keygen] created output dir")
    except Exception as e:
        logger.warning("[newyear_keygen] failed to create output dir: %s", e)

    try:
        await session.run_command("taskkill /IM crackme.exe /F", check=False)
        logger.info("[newyear_keygen] killed leftover crackme.exe processes")
    except Exception as e:
        logger.warning("[newyear_keygen] failed to clean crackme.exe process: %s", e)

    status: Dict[str, Any] = {}
    try:
        status = {
            "exe_exists": await session.exists(exe_path),
            "uids_exists": await session.exists(uids_path),
        }
        logger.info("[newyear_keygen] setup status=%s", status)
    except Exception as e:
        status = {"error": str(e)}
        logger.warning("[newyear_keygen] failed to collect setup status: %s", e)

    try:
        await session.write_file(
            os.path.join(out_dir, "setup_status.json"),
            json.dumps(status, ensure_ascii=False, indent=2),
        )
    except Exception:
        pass


@cb.evaluate_task(split="train")
async def evaluate(task_cfg, session: cb.DesktopSession) -> list[float]:
    out_dir = task_cfg.metadata["remote_output_dir"]
    output_path = task_cfg.metadata["output_path"]
    uids_path = task_cfg.metadata["uids_path"]
    reference_keys_path = task_cfg.metadata["reference_keys_path"]

    logger.info("[newyear_keygen] evaluate() begin")
    logger.info("[newyear_keygen] output_path=%s", output_path)
    logger.info("[newyear_keygen] uids_path=%s", uids_path)
    logger.info("[newyear_keygen] reference_keys_path=%s", reference_keys_path)

    try:
        uids = await session.read_file(uids_path)
        expected = await session.read_file(reference_keys_path)
        actual = await session.read_file(output_path)
        logger.info(
            "[newyear_keygen] loaded files uids=%s expected=%s actual=%s chars",
            len(uids),
            len(expected),
            len(actual),
        )
    except Exception as e:
        logger.warning("[newyear_keygen] failed to read required files: %s", e)
        try:
            await session.write_file(
                os.path.join(out_dir, "autograde_report.json"),
                json.dumps({"passed": False, "error": str(e)}, ensure_ascii=False, indent=2),
            )
        except Exception:
            pass
        return [0.0]

    uid_lines = uids.splitlines()
    expected_lines = expected.splitlines()
    actual_lines = actual.splitlines()

    passed = actual_lines == expected_lines
    mismatch_index = None
    for idx, (exp, got) in enumerate(zip(expected_lines, actual_lines)):
        if exp != got:
            mismatch_index = idx
            break
    if mismatch_index is None and len(expected_lines) != len(actual_lines):
        mismatch_index = min(len(expected_lines), len(actual_lines))

    report: Dict[str, Any] = {
        "passed": passed,
        "uid_count": len(uid_lines),
        "expected_count": len(expected_lines),
        "actual_count": len(actual_lines),
        "first_mismatch_index": mismatch_index,
    }
    if mismatch_index is not None:
        report["uid"] = uid_lines[mismatch_index] if mismatch_index < len(uid_lines) else None
        report["expected_line"] = (
            expected_lines[mismatch_index] if mismatch_index < len(expected_lines) else None
        )
        report["actual_line"] = (
            actual_lines[mismatch_index] if mismatch_index < len(actual_lines) else None
        )

    try:
        await session.write_file(
            os.path.join(out_dir, "autograde_report.json"),
            json.dumps(report, ensure_ascii=False, indent=2),
        )
    except Exception:
        pass

    logger.info(
        "[newyear_keygen] uid_count=%s expected_count=%s actual_count=%s passed=%s",
        len(uid_lines),
        len(expected_lines),
        len(actual_lines),
        passed,
    )
    return [1.0 if passed else 0.0]
