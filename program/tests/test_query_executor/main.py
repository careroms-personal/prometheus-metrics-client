import os

from connector.client import PrometheusClient
from processors.query_executor import QueryExecutor
from models.promql_model import ConnectionConfig, QueryItem, QueryExportConfig

def main():
  url = os.getenv("URL")
  api_query_path = os.getenv("API_PATH")

  connection_config = ConnectionConfig(
    url=url,
    api_query_path=api_query_path,
    timeout=30,
  )

  query_item = QueryItem(
    name="test_query",
    type="query",
    promql='up{pod="prometheus-prometheus-kube-prometheus-prometheus-0"}',
  )

  query_range_item = QueryItem(
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

  client = PrometheusClient(connection_config=connection_config)

  query_results = QueryExecutor(
    client=client, 
    connection_config=connection_config,
    query_items=[query_item],
  ).execute()

  query_range_results = QueryExecutor(
    client=client,
    connection_config=connection_config,
    query_items=[query_range_item],
  ).execute()

  print(f"✅ Query complete:")
  print(query_results)
  

  print(f"✅ Query range complete:")
  print(query_range_results)


if __name__ == "__main__":
  main()