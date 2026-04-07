# prometheus-metrics-query

A flexible, config-driven Prometheus/Mimir query executor with CSV and JSON export for data-driven SRE workflows.

## Overview

This tool executes PromQL queries against a Prometheus or Mimir server based on a YAML configuration file, and exports the results as CSV or JSON files. It is designed for batch metric extraction — useful for reporting, audits, or feeding data into downstream pipelines.

## Requirements

- Python >= 3.9
- Dependencies (install via pip):
  - `requests>=2.31.0`
  - `pydantic==2.12.5`
  - `PyYAML==6.0.3`

```bash
pip install .
```

## Usage

```bash
python program/app/main.py -c <path-to-config.yaml>
```

**Arguments:**

| Flag | Description |
|------|-------------|
| `-c`, `--config` | Path to the YAML configuration file (required) |

**Example:**

```bash
python program/app/main.py -c ./my_config.yaml
```

## Configuration

The configuration file is a YAML file. A template is provided at [program/config_templates/global_config.yaml](program/config_templates/global_config.yaml).

### Full Structure

```yaml
name: "my-metrics"                  # Identifier for this config

connection:
  url: "http://prometheus:9090"     # Prometheus/Mimir server URL
  api_query_path: "/api/v1"         # API path (use /prometheus/api/v1 for Mimir)
  timeout: 30                       # Request timeout in seconds

queries:
  - name: "cpu_usage"               # Query identifier, used as output filename
    type: "query_range"             # "query" (instant) or "query_range" (time series)
    promql: |
      rate(container_cpu_usage_seconds_total[5m])
    start: "24h"                    # Start time (required for query_range)
    end: "now"                      # End time (required for query_range)
    step: "5m"                      # Aggregation step (required for query_range)
    export_config:                  # Optional: control which metric labels to export
      export_all_metric: false
      export_metric_key:
        - pod
        - namespace

  - name: "current_status"
    type: "query"                   # Instant query — no start/end/step needed
    promql: 'up{job="prometheus"}'

output:                             # Optional
  print_output: false               # Print results to stdout
  write_options:
    - base_directory: "./results"   # Output directory
      format: csv
    - base_directory: "./results"
      format: json
```

### Configuration Fields

#### `connection`

| Field | Required | Description |
|-------|----------|-------------|
| `url` | Yes | Full base URL of the Prometheus/Mimir server |
| `api_query_path` | Yes | API path, typically `/api/v1` for Prometheus or `/prometheus/api/v1` for Mimir |
| `timeout` | No | HTTP request timeout in seconds (default: `30`) |

#### `queries[]`

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Query name; also used as the output filename |
| `type` | Yes | `"query"` for instant or `"query_range"` for time series |
| `promql` | Yes | PromQL expression to execute |
| `start` | For `query_range` | Start time of the range |
| `end` | For `query_range` | End time of the range |
| `step` | For `query_range` | Query resolution step |
| `export_config` | No | Controls which metric labels are included in output |

**Time formats for `start` / `end`:**

| Format | Example | Description |
|--------|---------|-------------|
| Relative | `"30d"`, `"2h"`, `"15m"` | Time ago from now |
| Literal | `"now"` | Current time |
| Unix timestamp | `"1700000000"` | Unix epoch (numeric string) |
| ISO 8601 | `"2025-01-01T00:00:00"` | Absolute datetime |

#### `export_config` (optional)

Controls which Prometheus metric labels appear in the output. If omitted, all labels are exported.

| Field | Description |
|-------|-------------|
| `export_all_metric` | `true` to export all labels |
| `export_metric_key` | List of specific label keys to include |

If both are set, `export_all_metric: true` takes precedence.

#### `output` (optional)

| Field | Description |
|-------|-------------|
| `print_output` | `true` to print results to stdout (default: `false`) |
| `write_options` | List of file output destinations |

#### `write_options[]`

| Field | Description |
|-------|-------------|
| `base_directory` | Directory where output files are saved |
| `format` | `"csv"` or `"json"` |

Output files are named after the query: `<base_directory>/<query_name>.csv` or `<query_name>.json`.

## Output Formats

### CSV

Columns: metric label columns (alphabetically sorted) + `datetime`, `timestamp`, `value`.

One row per data point per metric series.

```
namespace,pod,datetime,timestamp,value
monitoring,prometheus-0,2025-01-01 00:00:00,1735689600.0,0.0042
monitoring,prometheus-0,2025-01-01 00:05:00,1735689900.0,0.0038
```

### JSON

An array of objects, each with `metric` (label map) and `values` (list of data points).

```json
[
  {
    "metric": {
      "namespace": "monitoring",
      "pod": "prometheus-0"
    },
    "values": [
      {
        "datetime": "2025-01-01 00:00:00",
        "timestamp": 1735689600.0,
        "value": "0.0042"
      }
    ]
  }
]
```

## Examples

### Export 7-day CPU and memory metrics to CSV

```yaml
name: "weekly-report"

connection:
  url: "http://prometheus.internal:9090"
  api_query_path: "/api/v1"
  timeout: 30

queries:
  - name: "cpu_usage"
    type: "query_range"
    promql: |
      rate(container_cpu_usage_seconds_total{namespace="production"}[5m])
    start: "7d"
    end: "now"
    step: "1h"
    export_config:
      export_metric_key:
        - namespace
        - pod

  - name: "memory_usage"
    type: "query_range"
    promql: |
      container_memory_usage_bytes{namespace="production"}
    start: "7d"
    end: "now"
    step: "1h"
    export_config:
      export_metric_key:
        - namespace
        - pod

output:
  write_options:
    - base_directory: "./results"
      format: csv
```

```bash
python program/app/main.py -c ./weekly_report.yaml
# Output: ./results/cpu_usage.csv, ./results/memory_usage.csv
```

### Instant query with stdout print and JSON export

```yaml
name: "status-check"

connection:
  url: "http://mimir.internal/prometheus/api/v1"
  api_query_path: "/prometheus/api/v1"

queries:
  - name: "up_status"
    type: "query"
    promql: 'up{job="node-exporter"}'
    export_config:
      export_metric_key:
        - instance
        - job

output:
  print_output: true
  write_options:
    - base_directory: "./output"
      format: json
```

```bash
python program/app/main.py -c ./status_check.yaml
# Prints to stdout and writes ./output/up_status.json
```
