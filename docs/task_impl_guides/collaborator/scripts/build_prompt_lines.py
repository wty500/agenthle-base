#!/usr/bin/env python
"""Generate a Codex prompt list from reviewed submissions.

The script reads submission/review/task metadata from Neon DB and writes one
prompt line per qualified submission to `prompt.txt`.
"""

from __future__ import annotations

import argparse
import asyncio
import os
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.utils.database_url import to_asyncpg_url


VERDICT_ORDER = {
    "major revision": 0,
    "minor revision": 1,
    "borderline accept": 2,
    "accept": 3,
    "strong accept": 4,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build prompt.txt lines for Codex: one line per reviewed submission "
            "whose verdict is above a threshold."
        )
    )
    parser.add_argument(
        "--database-url",
        dest="database_url",
        help=(
            "Explicit Postgres URL. If omitted, reads from --db-url-env (default DATABASE_URL_MAIN). "
            "Use DATABASE_URL for preview environment."
        ),
    )
    parser.add_argument(
        "--db-url-env",
        default="DATABASE_URL_MAIN",
        help="Environment variable name for DB URL lookup when --database-url is not set.",
    )
    parser.add_argument(
        "--review-type",
        default="submission_ai",
        help="Review type to read; admin-reviews use `submission_ai` by default.",
    )
    parser.add_argument(
        "--min-verdict",
        default="Minor Revision",
        help="Verdict threshold. Default keeps items strictly greater than this value.",
    )
    parser.add_argument(
        "--comparison",
        default="gt",
        choices=("gt", "gte"),
        help="gt means strictly greater than min_verdict; gte includes equal.",
    )
    parser.add_argument(
        "--out",
        default="prompt.txt",
        help="Output prompt file path. One line per selected submission.",
    )
    parser.add_argument(
        "--docs-root",
        default="agenthle-base/docs/task_impl_guides/collaborator",
        help="Reference docs path inserted into each prompt line.",
    )
    return parser.parse_args()


def strip_quotes(raw: str | None) -> str | None:
    if not raw:
        return None
    value = raw.strip()
    if len(value) >= 2:
        first = value[0]
        last = value[-1]
        if (first == "\"" and last == "\"") or (first == "'" and last == "'"):
            return value[1:-1]
    return value


def load_env_value(name: str) -> str | None:
    env_value = os.environ.get(name)
    if env_value:
        return strip_quotes(env_value)

    repo_env = Path(__file__).resolve().parents[4] / ".env"
    if not repo_env.exists():
        return None

    for line in repo_env.read_text(encoding="utf-8").splitlines():
        if not line or line.lstrip().startswith("#") or "=" not in line:
            continue
        key, raw = line.split("=", 1)
        if key != name:
            continue
        return strip_quotes(raw)

    return None


def normalize_verdict(value: str | None) -> str | None:
    if not value:
        return None
    return " ".join(value.strip().lower().split())


def verdict_rank(value: str | None) -> int | None:
    normalized = normalize_verdict(value)
    if normalized is None:
        return None
    return VERDICT_ORDER.get(normalized)


def build_query() -> str:
    return """
    select
      s.id as submission_id,
      s.task_short_name,
      s.task_short_name_normalized,
      s.task_description,
      s.industry_domain,
      s.software_and_version,
      s.operating_system,
      s.software_licensing,
      s.specific_requirements,
      s.verification_method,
      s.evaluation_criteria,
      s.status as submission_status,
      s.gcs_prefix,
      s.created_at,
      s.submitted_at,
      r.id as review_id,
      r.overall_verdict,
      r.updated_at as review_updated_at,
      u.id as user_id,
      u.email,
      u.first_name,
      u.last_name
    from submissions s
    join users u on u.id = s.user_id
    join reviews r on r.submission_id = s.id
      and r.submission_revision_id = s.latest_submitted_revision_id
      and r.review_type = :review_type
    where s.deleted = false
      and r.overall_verdict is not null
    order by coalesce(s.submitted_at, s.created_at) desc nulls last, s.created_at desc
    """


def format_prompt_line(row: dict[str, Any], docs_root: str, min_verdict: str, comparison: str) -> str:
    names = []
    if row["first_name"]:
        names.append((row["first_name"]).strip())
    if row["last_name"]:
        names.append((row["last_name"]).strip())

    author = " ".join(names) or row["email"]
    task_name = row["task_short_name"] or row["task_short_name_normalized"] or "(unknown task)"
    verdict = row["overall_verdict"] or "(missing verdict)"

    return (
        f"请严格按照 {docs_root} 文档树来实施该任务："
        f"提交人 {author}（{row['email']}），任务 short_name={task_name}，"
        f"提交ID={row['submission_id']}，评分={verdict}（阈值{min_verdict}，"
        f"比较方式={comparison}）。请先读取该提交通道与相关 GCS 路径（gcs_prefix={row['gcs_prefix'] or 'unknown'}）后实现对应任务。"
    )


def should_include(overall_verdict: str | None, min_verdict: str, comparison: str) -> bool:
    rank_value = verdict_rank(overall_verdict)
    threshold = verdict_rank(min_verdict)
    if rank_value is None or threshold is None:
        return False
    if comparison == "gte":
        return rank_value >= threshold
    return rank_value > threshold


def select_records(records: list[dict[str, Any]], min_verdict: str, comparison: str) -> Iterator[dict[str, Any]]:
    for row in records:
        if should_include(row["overall_verdict"], min_verdict, comparison):
            yield row


async def main() -> None:
    args = parse_args()
    database_url = args.database_url or load_env_value(args.db_url_env)
    if not database_url:
        raise SystemExit(f"database url not found in environment variable {args.db_url_env}")

    engine = create_async_engine(to_asyncpg_url(database_url))
    session_factory = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

    async with session_factory() as session:
        result = await session.execute(text(build_query()), {"review_type": args.review_type})
        rows = result.fetchall()

    await engine.dispose()

    records = [dict(row._mapping) for row in rows]
    selected = list(select_records(records, args.min_verdict, args.comparison))

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        format_prompt_line(row, args.docs_root, args.min_verdict, args.comparison) for row in selected
    ]
    out_path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")

    print(f"selected_records={len(selected)}")
    print(f"prompt_file={out_path}")


if __name__ == "__main__":
    asyncio.run(main())
