There is an Apache-style access log at `/app/access.log`. Analyze the log and save a JSON report to `/app/report.json`.

Success criteria:

1. `/app/report.json` must contain a valid JSON object with exactly these keys: `total_requests`, `unique_ips`, and `top_path`.

2. `total_requests` must be the number of non-empty lines in `/app/access.log`.

3. `unique_ips` must be the number of distinct client addresses found in the first whitespace-separated field of each non-empty log line.

4. `top_path` must be the request path that occurs most often among valid HTTP request fields. Recognize the methods `GET`, `POST`, `PUT`, `DELETE`, `HEAD`, and `PATCH`. If multiple paths have the same highest count, return the lexicographically smallest path. If no request path is found, use JSON `null`.

Do not modify `/app/access.log`.