import os

from models.promql_model import QueryItem, QueryExportConfig
from models.promql_model import ConnectionConfig

CONNECTION_CONFIG = ConnectionConfig(
  url=os.getenv("URL"),
  api_query_path=os.getenv("API_PATH"),
  timeout=30,
)

TEST_QUERY_PROMETHEUS_CPU = QueryItem(
  name="test_query_prometheus_cpu",
  type="query_range",
  promql='rate(container_cpu_usage_seconds_total{pod="prometheus-prometheus-kube-prometheus-prometheus-0"}[5m])',
  start="1h",
  end="now",
  step="10m",
  export_config=QueryExportConfig(
    export_metric_key=['node','namespace','pod']
  )
)

TEST_QUERY_PROMETHEUS_MEMORY = QueryItem(
  name="test_query_prometheus_memory",
  type="query_range",
  promql='rate(container_memory_usage_bytes{pod="prometheus-prometheus-kube-prometheus-prometheus-0"}[5m])',
  start="1h",
  end="now",
  step="10m",
  export_config=QueryExportConfig(
    export_metric_key=['node','namespace','pod']
  )
)

TEST_SIMPLE_QUERY = QueryItem(
  name="test_query",
  type="query",
  promql='up{pod="prometheus-prometheus-kube-prometheus-prometheus-0"}',
)

TEST_SIMPLE_QUERY_RANGE = QueryItem(
    name="test_query_range",
    type="query_range",
    promql='rate(container_cpu_usage_seconds_total{pod="prometheus-prometheus-kube-prometheus-prometheus-0"}[5m])',
    start="1h",
    end="now",
    step="10m",
    export_config=QueryExportConfig(
      export_all_metric=True
    )
  )