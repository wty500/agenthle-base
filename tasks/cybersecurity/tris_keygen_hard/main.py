'''
Recover the keygen logic used by the bundled program and output the correct password for every serial number. A possible solution is to reverse engineer the executable to understand the keygen algorithm, then implement that algorithm to generate the passwords for the provided serial numbers.
Credit to: Juanru Li @ SJTU
'''
import json
import logging
import os
from dataclasses import dataclass

import cua_bench as cb
from tasks.common_config import GeneralTaskConfig

logger = logging.getLogger(__name__)

REGISTRY_PATH = (
    r"Registry::HKEY_CURRENT_USER\Software\Classes\VirtualStore\MACHINE\SOFTWARE\WOW6432Node"
    r"\Stefan Pettersson\YourTris"
)
REGISTRY_PATH_REG_EXE = (
    r"HKCU\Software\Classes\VirtualStore\MACHINE\SOFTWARE\WOW6432Node"
    r"\Stefan Pettersson\YourTris"
)


def generate_password(name: str) -> str:
    tmp = "".join(str(ord(ch) * (idx + 1) + idx) for idx, ch in enumerate(name))
    n = len(name)
    start_idx = max(0, n - 7)
    end_idx = max(start_idx + 6, n - 1)
    return tmp[start_idx:end_idx]


def last_json(stdout: str) -> dict:
    for line in reversed([x.strip() for x in str(stdout).splitlines() if x.strip()]):
        try:
            return json.loads(line)
        except Exception:
            continue
    return {}


def trim_text(value, limit: int = 400) -> str:
    text = str(value or "").strip()
    if len(text) <= limit:
        return text
    return text[:limit] + "...<truncated>"


def registry_cleanup_cmd() -> str:
    return (
        "powershell -NoProfile -ExecutionPolicy Bypass -Command "
        "\"& { "
        "$psPath = '"
        + REGISTRY_PATH
        + "'; "
        "$regExePath = '"
        + REGISTRY_PATH_REG_EXE
        + "'; "
        "Stop-Process -Name tris -Force -ErrorAction SilentlyContinue; "
        "Start-Sleep -Milliseconds 300; "
        "if (Test-Path -LiteralPath $psPath) { "
        "Remove-Item -LiteralPath $psPath -Recurse -Force -ErrorAction SilentlyContinue "
        "}; "
        "if (Test-Path -LiteralPath $psPath) { "
        "& reg.exe delete $regExePath /f | Out-Null "
        "}; "
        "[pscustomobject]@{removed = -not (Test-Path -LiteralPath $psPath)} | ConvertTo-Json -Compress "
        "}\""
    )


@dataclass
class TaskConfig(GeneralTaskConfig):
    TASK_TAG: str = "tris_keygen_hard"
    TASK_CATEGORY: str = "cybersecurity"
    OUTPUT_FILENAME: str = "passwords.txt"

    @property
    def exe_path(self) -> str:
        return fr"{self.task_dir}\input\tris.exe"

    @property
    def serials_path(self) -> str:
        return fr"{self.task_dir}\input\serials.txt"

    @property
    def reference_passwords_path(self) -> str:
        return fr"{self.reference_dir}\passwords.txt"

    @property
    def output_path(self) -> str:
        return fr"{self.remote_output_dir}\{self.OUTPUT_FILENAME}"

    @property
    def task_description(self) -> str:
        return f"""
Goal:
Recover the keygen logic used by the bundled program and output the correct password for every serial number.

Inputs:
- Executable to reverse/analyze: {self.exe_path}
- Serial numbers: {self.serials_path}

Output:
- Save EXACTLY one UTF-8 text file to: {self.output_path}
- One password per line
- Preserve the same order as serials.txt
- Do not add any extra commentary, numbering, or blank lines

Verification:
- Score is 1.0 only if the output file matches the reference answers exactly line by line.
"""

    def to_metadata(self) -> dict:
        metadata = super().to_metadata()
        metadata.update(
            {
                "exe_path": self.exe_path,
                "serials_path": self.serials_path,
                "reference_passwords_path": self.reference_passwords_path,
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

    logger.info("[tris_keygen_hard] start() begin")
    logger.info("[tris_keygen_hard] exe_path=%s", exe_path)
    logger.info("[tris_keygen_hard] registry_path=%s", REGISTRY_PATH)
    logger.info("[tris_keygen_hard] out_dir=%s", out_dir)

    try:
        await session.remove_file(out_dir)
        logger.info("[tris_keygen_hard] removed existing output dir: %s", out_dir)
    except Exception:
        logger.info("[tris_keygen_hard] output dir did not need removal: %s", out_dir)

    try:
        await session.makedirs(out_dir)
        logger.info("[tris_keygen_hard] created output dir: %s", out_dir)
    except Exception as e:
        logger.warning("Failed to create output dir: %s", e)

    try:
        logger.info("[tris_keygen_hard] running registry cleanup command")
        cleanup_result = await session.run_command(registry_cleanup_cmd(), check=False)
        cleanup_status = last_json(cleanup_result.get("stdout", ""))
        logger.info(
            "[tris_keygen_hard] cleanup rc=%s stdout=%s stderr=%s parsed=%s",
            cleanup_result.get("return_code"),
            trim_text(cleanup_result.get("stdout")),
            trim_text(cleanup_result.get("stderr")),
            cleanup_status,
        )
        await session.write_file(
            os.path.join(out_dir, "registry_cleanup.json"),
            json.dumps(cleanup_status, ensure_ascii=False, indent=2),
        )
        logger.info("[tris_keygen_hard] wrote registry_cleanup.json")
    except Exception as e:
        logger.warning("Failed to clean registry/process state: %s", e)

    try:
        exe_exists = await session.exists(exe_path)
        logger.info("[tris_keygen_hard] exe exists=%s path=%s", exe_exists, exe_path)
        if not exe_exists:
            logger.warning("[tris_keygen_hard] executable not found: %s", exe_path)
    except Exception as e:
        logger.warning("Failed to verify tris.exe existence: %s", e)


@cb.evaluate_task(split="train")
async def evaluate(task_cfg, session: cb.DesktopSession) -> list[float]:
    out_dir = task_cfg.metadata["remote_output_dir"]
    output_path = task_cfg.metadata["output_path"]
    serials_path = task_cfg.metadata["serials_path"]
    reference_passwords_path = task_cfg.metadata["reference_passwords_path"]

    logger.info("[tris_keygen_hard] evaluate() begin")
    logger.info("[tris_keygen_hard] serials_path=%s", serials_path)
    logger.info("[tris_keygen_hard] output_path=%s", output_path)
    logger.info("[tris_keygen_hard] reference_passwords_path=%s", reference_passwords_path)

    try:
        serials = await session.read_file(serials_path)
        expected = await session.read_file(reference_passwords_path)
        actual = await session.read_file(output_path)
        logger.info(
            "[tris_keygen_hard] loaded files serials=%s expected=%s actual=%s chars",
            len(serials),
            len(expected),
            len(actual),
        )
    except Exception as e:
        logger.warning("Failed to read required files: %s", e)
        try:
            await session.write_file(
                os.path.join(out_dir, "autograde_report.json"),
                json.dumps({"passed": False, "error": str(e)}, ensure_ascii=False, indent=2),
            )
        except Exception:
            pass
        return [0.0]

    serial_lines = serials.splitlines()
    expected_lines = expected.splitlines()
    actual_lines = actual.splitlines()

    passed = actual_lines == expected_lines
    logger.info(
        "[tris_keygen_hard] line counts serials=%s expected=%s actual=%s passed=%s",
        len(serial_lines),
        len(expected_lines),
        len(actual_lines),
        passed,
    )

    mismatch_index = None
    for idx, (exp, got) in enumerate(zip(expected_lines, actual_lines)):
        if exp != got:
            mismatch_index = idx
            break
    if mismatch_index is None and len(expected_lines) != len(actual_lines):
        mismatch_index = min(len(expected_lines), len(actual_lines))

    report = {
        "passed": passed,
        "serial_count": len(serial_lines),
        "expected_count": len(expected_lines),
        "actual_count": len(actual_lines),
        "first_mismatch_index": mismatch_index,
    }
    if mismatch_index is not None:
        report["expected_line"] = (
            expected_lines[mismatch_index] if mismatch_index < len(expected_lines) else None
        )
        report["actual_line"] = (
            actual_lines[mismatch_index] if mismatch_index < len(actual_lines) else None
        )
        logger.info(
            "[tris_keygen_hard] first mismatch at line %s expected=%r actual=%r",
            mismatch_index,
            report["expected_line"],
            report["actual_line"],
        )
    else:
        logger.info("[tris_keygen_hard] no mismatch found")

    try:
        await session.write_file(
            os.path.join(out_dir, "autograde_report.json"),
            json.dumps(report, ensure_ascii=False, indent=2),
        )
        logger.info("[tris_keygen_hard] wrote autograde_report.json")
    except Exception:
        pass

    return [1.0 if passed else 0.0]
