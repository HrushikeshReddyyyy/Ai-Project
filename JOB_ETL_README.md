# Job Portal ETL Tool

This tool collects job listings from public job portal APIs/RSS feeds, filters them by title and recency (last 24 hours), and loads the results to CSV, JSONL, or SQLite.

## Quick start

```bash
python job_etl.py --titles "data scientist,backend engineer"
```

## Common options

- `--titles`: Comma-separated list of job titles to match (case-insensitive).
- `--sources`: Comma-separated list of sources (`remotive`, `remoteok`, `weworkremotely`).
- `--format`: Output format (`sqlite`, `csv`, `jsonl`).
- `--output`: Output file path.

## Examples

```bash
# Default SQLite output with title matching
python job_etl.py --titles "product manager,ml engineer"

# CSV output from selected sources
python job_etl.py --sources remotive,remoteok --titles "data analyst" --format csv --output jobs.csv

# JSONL output from WeWorkRemotely only
python job_etl.py --sources weworkremotely --titles "frontend" --format jsonl --output jobs.jsonl
```

## Notes

- This tool uses public endpoints and is intended to follow each portal's terms of service.
- Results include links and descriptions when available in the source API/RSS feeds.
