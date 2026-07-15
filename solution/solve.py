from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


ACCESS_LOG_PATH = Path("/app/access.log")
REPORT_PATH = Path("/app/report.json")

REQUEST_PATTERN = re.compile(
    r'"(?:GET|POST|PUT|DELETE|HEAD|PATCH)\s+(\S+)\s+'
)


def build_report() -> dict[str, int | str | None]:
    total_requests = 0
    unique_ips: set[str] = set()
    path_counts: Counter[str] = Counter()

    with ACCESS_LOG_PATH.open(
        "r",
        encoding="utf-8",
        errors="replace",
    ) as log_file:
        for raw_line in log_file:
            line = raw_line.strip()

            if not line:
                continue

            total_requests += 1

            fields = line.split()
            if fields:
                unique_ips.add(fields[0])

            match = REQUEST_PATTERN.search(line)
            if match is not None:
                path_counts[match.group(1)] += 1

    top_path: str | None = None

    if path_counts:
        highest_count = max(path_counts.values())

        top_path = min(
            path
            for path, count in path_counts.items()
            if count == highest_count
        )

    return {
        "total_requests": total_requests,
        "unique_ips": len(unique_ips),
        "top_path": top_path,
    }


def main() -> None:
    report = build_report()

    with REPORT_PATH.open(
        "w",
        encoding="utf-8",
    ) as output_file:
        json.dump(report, output_file)
        output_file.write("\n")


if __name__ == "__main__":
    main()