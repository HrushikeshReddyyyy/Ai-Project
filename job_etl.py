"""Simple ETL tool for collecting job listings from multiple portals.

This script focuses on public endpoints (JSON/RSS) and provides a consistent
schema for downstream use. Scraping should follow each site's ToS.
"""

from __future__ import annotations

import argparse
import csv
import json
import sqlite3
import sys
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable
from urllib.request import Request, urlopen
from xml.etree import ElementTree


@dataclass(frozen=True)
class JobRecord:
    source: str
    source_id: str
    title: str
    company: str
    location: str
    url: str
    tags: str
    date_posted: str
    salary: str
    description: str


class JobPortal:
    name: str

    def extract(self) -> list[JobRecord]:
        raise NotImplementedError


class RemotivePortal(JobPortal):
    name = "remotive"
    endpoint = "https://remotive.com/api/remote-jobs"

    def extract(self) -> list[JobRecord]:
        payload = fetch_json(self.endpoint)
        records: list[JobRecord] = []
        for job in payload.get("jobs", []):
            records.append(
                JobRecord(
                    source=self.name,
                    source_id=str(job.get("id", "")),
                    title=job.get("title", ""),
                    company=job.get("company_name", ""),
                    location=job.get("candidate_required_location", ""),
                    url=job.get("url", ""),
                    tags=", ".join(job.get("tags", [])),
                    date_posted=job.get("publication_date", ""),
                    salary=job.get("salary", ""),
                    description=job.get("description", ""),
                )
            )
        return records


class RemoteOkPortal(JobPortal):
    name = "remoteok"
    endpoint = "https://remoteok.com/api"

    def extract(self) -> list[JobRecord]:
        payload = fetch_json(self.endpoint)
        records: list[JobRecord] = []
        for job in payload:
            if not isinstance(job, dict) or "id" not in job:
                continue
            records.append(
                JobRecord(
                    source=self.name,
                    source_id=str(job.get("id", "")),
                    title=job.get("position", ""),
                    company=job.get("company", ""),
                    location=job.get("location", ""),
                    url=job.get("url", ""),
                    tags=", ".join(job.get("tags", [])),
                    date_posted=str(job.get("date_epoch", job.get("date", ""))),
                    salary=str(job.get("salary", "")) if job.get("salary") else "",
                    description=job.get("description", ""),
                )
            )
        return records


class WeWorkRemotelyPortal(JobPortal):
    name = "weworkremotely"
    endpoint = "https://weworkremotely.com/remote-jobs.rss"

    def extract(self) -> list[JobRecord]:
        xml_text = fetch_text(self.endpoint)
        root = ElementTree.fromstring(xml_text)
        records: list[JobRecord] = []
        for item in root.findall("./channel/item"):
            title = text_of(item, "title")
            link = text_of(item, "link")
            pub_date = text_of(item, "pubDate")
            company = text_of(item, "company")
            location = text_of(item, "region")
            tags = text_of(item, "category")
            description = text_of(item, "description")
            source_id = link.rsplit("/", 1)[-1]
            records.append(
                JobRecord(
                    source=self.name,
                    source_id=source_id,
                    title=title,
                    company=company,
                    location=location,
                    url=link,
                    tags=tags,
                    date_posted=pub_date,
                    salary="",
                    description=description,
                )
            )
        return records


def fetch_json(url: str) -> dict | list:
    request = Request(url, headers={"User-Agent": "job-etl-bot/1.0"})
    with urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_text(url: str) -> str:
    request = Request(url, headers={"User-Agent": "job-etl-bot/1.0"})
    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def text_of(parent: ElementTree.Element, tag: str) -> str:
    element = parent.find(tag)
    return element.text.strip() if element is not None and element.text else ""


def transform(records: Iterable[JobRecord]) -> list[JobRecord]:
    cleaned: list[JobRecord] = []
    for record in records:
        cleaned.append(
            JobRecord(
                source=record.source,
                source_id=record.source_id,
                title=record.title.strip(),
                company=record.company.strip(),
                location=record.location.strip(),
                url=record.url.strip(),
                tags=record.tags.strip(),
                date_posted=normalize_date(record.date_posted),
                salary=record.salary.strip(),
                description=record.description.strip(),
            )
        )
    return cleaned


def normalize_date(value: str) -> str:
    parsed = parse_datetime(value)
    if parsed is None:
        return ""
    if value.isdigit() or "T" in value or ":" in value:
        return parsed.isoformat()
    return parsed.date().isoformat()


def parse_datetime(value: str) -> datetime | None:
    if not value:
        return None
    if value.isdigit():
        return datetime.utcfromtimestamp(int(value))
    for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%a, %d %b %Y %H:%M:%S %z", "%Y-%m-%d"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    return None


def load_to_csv(records: Iterable[JobRecord], path: str) -> None:
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(JobRecord.__annotations__.keys())
        for record in records:
            writer.writerow(record.__dict__.values())


def load_to_jsonl(records: Iterable[JobRecord], path: str) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record.__dict__, ensure_ascii=False) + "\n")


def load_to_sqlite(records: Iterable[JobRecord], path: str) -> None:
    with sqlite3.connect(path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS jobs (
                source TEXT,
                source_id TEXT,
                title TEXT,
                company TEXT,
                location TEXT,
                url TEXT,
                tags TEXT,
                date_posted TEXT,
                salary TEXT,
                description TEXT,
                PRIMARY KEY (source, source_id)
            )
            """
        )
        conn.executemany(
            """
            INSERT OR REPLACE INTO jobs (
                source, source_id, title, company, location, url, tags, date_posted, salary, description
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [tuple(record.__dict__.values()) for record in records],
        )
        conn.commit()


PORTALS: dict[str, JobPortal] = {
    RemotivePortal.name: RemotivePortal(),
    RemoteOkPortal.name: RemoteOkPortal(),
    WeWorkRemotelyPortal.name: WeWorkRemotelyPortal(),
}


def run_etl(selected: list[str], output: str, fmt: str, titles: list[str]) -> int:
    records: list[JobRecord] = []
    for name in selected:
        portal = PORTALS.get(name)
        if portal is None:
            raise ValueError(f"Unknown portal: {name}")
        records.extend(portal.extract())
    cleaned = transform(records)
    filtered = filter_jobs(cleaned, titles)

    if fmt == "csv":
        load_to_csv(filtered, output)
    elif fmt == "jsonl":
        load_to_jsonl(filtered, output)
    elif fmt == "sqlite":
        load_to_sqlite(filtered, output)
    else:
        raise ValueError(f"Unsupported format: {fmt}")

    print(f"Loaded {len(filtered)} jobs to {output}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="ETL tool for job portals")
    parser.add_argument(
        "--sources",
        default=",".join(PORTALS.keys()),
        help="Comma-separated list of sources (remotive, remoteok, weworkremotely)",
    )
    parser.add_argument(
        "--titles",
        default="",
        help="Comma-separated list of job titles to match (case-insensitive)",
    )
    parser.add_argument("--output", default="jobs.sqlite3", help="Output path")
    parser.add_argument(
        "--format",
        default="sqlite",
        choices=("sqlite", "csv", "jsonl"),
        help="Output format",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    sources = [name.strip() for name in args.sources.split(",") if name.strip()]
    titles = [title.strip() for title in args.titles.split(",") if title.strip()]
    if not sources:
        print("No sources provided", file=sys.stderr)
        return 1
    return run_etl(sources, args.output, args.format, titles)


def filter_jobs(records: Iterable[JobRecord], titles: list[str]) -> list[JobRecord]:
    cutoff = datetime.utcnow().timestamp() - 24 * 60 * 60
    lowered_titles = [title.lower() for title in titles]
    filtered: list[JobRecord] = []
    for record in records:
        if lowered_titles and not title_matches(record.title, lowered_titles):
            continue
        parsed = parse_datetime(record.date_posted)
        if parsed is None or parsed.timestamp() < cutoff:
            continue
        filtered.append(record)
    return filtered


def title_matches(title: str, lowered_titles: list[str]) -> bool:
    lowered_title = title.lower()
    return any(search in lowered_title for search in lowered_titles)


if __name__ == "__main__":
    raise SystemExit(main())
