from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


ACCESS_LOG_PATH = Path("/app/access.log")
REPORT_PATH = Path("/app/report.json")

EXPECTED_KEYS = {
    "total_requests",
    "unique_ips",
    "top_path",
}

REQUEST_PATTERN = re.compile(
    r'"(?:GET|POST|PUT|DELETE|HEAD|PATCH)\s+(\S+)\s+'
)


def load_report() -> dict[str, Any]:
    with REPORT_PATH.open(
        "r",
        encoding="utf-8",
    ) as report_file:
        result = json.load(report_file)

    assert isinstance(result, dict)
    return result


def independently_parse_log() -> tuple[
    int,
    int,
    str | None,
]:
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

    return total_requests, len(unique_ips), top_path


def test_success_criterion_1_report_format() -> None:
    """Success criterion 1: report is valid JSON with exactly the required keys."""
    assert REPORT_PATH.is_file(), (
        "/app/report.json was not created"
    )

    report = load_report()

    assert set(report) == EXPECTED_KEYS
    assert isinstance(
        report["total_requests"],
        int,
    )
    assert not isinstance(
        report["total_requests"],
        bool,
    )
    assert isinstance(
        report["unique_ips"],
        int,
    )
    assert not isinstance(
        report["unique_ips"],
        bool,
    )
    assert (
        report["top_path"] is None
        or isinstance(report["top_path"], str)
    )


def test_success_criterion_2_total_requests() -> None:
    """Success criterion 2: total_requests equals the number of non-empty lines."""
    expected_total, _, _ = independently_parse_log()
    report = load_report()

    assert report["total_requests"] == expected_total


def test_success_criterion_3_unique_ips() -> None:
    """Success criterion 3: unique_ips equals the number of distinct clients."""
    _, expected_unique_ips, _ = independently_parse_log()
    report = load_report()

    assert report["unique_ips"] == expected_unique_ips


def test_success_criterion_4_top_path() -> None:
    """Success criterion 4: top_path follows the documented counting and tie rules."""
    _, _, expected_top_path = independently_parse_log()
    report = load_report()

    assert report["top_path"] == expected_top_path