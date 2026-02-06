import sys, os

from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from connector.client import PrometheusClient
from processors.output_executor import OutputExecutor
from processors.query_executor import QueryExecutor
from models.promql_model import ConnectionConfig, QueryItem, OutputConfig, QueryExportConfig

def main():
  url = os.getenv("URL")
  api_query_path = os.getenv("API_PATH")

  connection_config = ConnectionConfig(
    url=url,
    api_query_path=api_query_path,
    timeout=30,
  )

  test_query_prometheus_cpu = QueryItem(
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

  test_query_prometheus_memory = QueryItem(
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

  output_csv_config = OutputConfig(
    base_directory="./result",
    format="csv",
    print_output=False,
    write_output=True,
    timestamp_subdirectory=False,
  )

  client = PrometheusClient(connection_config=connection_config)

  query_range_results = QueryExecutor(
    client=client,
    connection_config=connection_config,
    query_items=[
      test_query_prometheus_cpu,
      test_query_prometheus_memory,
    ],
  ).execute()

  output_executor = OutputExecutor(
    processor_results=query_range_results,
    output_config=output_csv_config,
  )

  output_executor.execute()

if __name__ == "__main__":
  main()