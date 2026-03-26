'''
Just a (difficult) crackme.
Credit to: SECCON2023_final_CTF
'''
import hashlib
import json
import logging
import os
import re
from dataclasses import dataclass
from typing import Any, Dict

import cua_bench as cb
from tasks.common_config import GeneralTaskConfig

logger = logging.getLogger(__name__)

EXPECTED_FLAG_SHA256 = "346dcad8c48087e885eb1cc0782d0bf1f5a7742b09cc479984a2fc06c47de446"
MAX_OUTPUT_CHARS = 2048


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def extract_flag_candidates(text: str) -> list[str]:
    return re.findall(r"SECCON\{[^}\r\n]{1,160}\}", text or "")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@dataclass
class TaskConfig(GeneralTaskConfig):
    TASK_TAG: str = "nothing_spetial_crackme"
    TASK_CATEGORY: str = "cybersecurity"
    OUTPUT_FILENAME: str = "answer.txt"

    @property
    def exe_path(self) -> str:
        return fr"{self.task_dir}\input\crackme.exe"

    @property
    def output_path(self) -> str:
        return fr"{self.remote_output_dir}\{self.OUTPUT_FILENAME}"

    @property
    def task_description(self) -> str:
        return f"""
Goal:
Recover the real flag from the bundled Windows crackme by reverse engineering it.

Input:
- Target executable: {self.exe_path}

Output:
- Save your final answer to: {self.output_path}
- The file must be plain text
- A single line containing the recovered flag is enough

Verification:
- Score is 1.0 only if the output contains the real flag.
"""

    def to_metadata(self) -> dict:
        metadata = super().to_metadata()
        metadata.update(
            {
                "exe_path": self.exe_path,
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

    logger.info("[nothing_spetial_crackme] start() begin")
    logger.info("[nothing_spetial_crackme] exe_path=%s", exe_path)
    logger.info("[nothing_spetial_crackme] out_dir=%s", out_dir)

    try:
        await session.remove_file(out_dir)
        logger.info("[nothing_spetial_crackme] removed existing output dir")
    except Exception:
        logger.info("[nothing_spetial_crackme] output dir did not need removal")

    try:
        await session.makedirs(out_dir)
        logger.info("[nothing_spetial_crackme] created output dir")
    except Exception as e:
        logger.warning("[nothing_spetial_crackme] failed to create output dir: %s", e)

    try:
        exe_exists = await session.exists(exe_path)
        logger.info("[nothing_spetial_crackme] exe exists=%s", exe_exists)
        await session.write_file(
            os.path.join(out_dir, "setup_status.json"),
            json.dumps({"exe_path": exe_path, "exists": exe_exists}, ensure_ascii=False, indent=2),
        )
    except Exception as e:
        logger.warning("[nothing_spetial_crackme] failed to verify exe existence: %s", e)


@cb.evaluate_task(split="train")
async def evaluate(task_cfg, session: cb.DesktopSession) -> list[float]:
    output_path = task_cfg.metadata["output_path"]
    out_dir = task_cfg.metadata["remote_output_dir"]

    logger.info("[nothing_spetial_crackme] evaluate() begin")
    logger.info("[nothing_spetial_crackme] output_path=%s", output_path)

    try:
        content = await session.read_file(output_path)
        logger.info("[nothing_spetial_crackme] read output chars=%s", len(content))
    except Exception as e:
        logger.warning("[nothing_spetial_crackme] failed to read output: %s", e)
        return [0.0]

    normalized = normalize_text(content)
    candidates = extract_flag_candidates(normalized)
    matched = any(sha256_text(candidate) == EXPECTED_FLAG_SHA256 for candidate in candidates)
    passed = len(content) <= MAX_OUTPUT_CHARS and matched

    report: Dict[str, Any] = {
        "output_path": output_path,
        "output_length": len(content),
        "candidate_count": len(candidates),
        "passed": passed,
    }
    if candidates:
        report["candidates_preview"] = candidates[:5]

    try:
        await session.write_file(
            os.path.join(out_dir, "autograde_report.json"),
            json.dumps(report, ensure_ascii=False, indent=2),
        )
    except Exception:
        pass

    logger.info("[nothing_spetial_crackme] candidates=%s passed=%s", candidates[:5], passed)
    return [1.0 if passed else 0.0]
