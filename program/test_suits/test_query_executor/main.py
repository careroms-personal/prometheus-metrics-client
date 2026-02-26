from connector.client import PrometheusClient
from test_suit.global_test_config import *
from processors.query_executor import QueryExecutor

def main():
  client = PrometheusClient(connection_config=CONNECTION_CONFIG)

  query_results = QueryExecutor(
    client=client, 
    query_items=[TEST_SIMPLE_QUERY],
  ).execute()

  query_range_results = QueryExecutor(
    client=client,
    query_items=[TEST_SIMPLE_QUERY_RANGE],
  ).execute()

  print(f"✅ Query complete:")
  print(query_results)
  

  print(f"✅ Query range complete:")
  print(query_range_results)


if __name__ == "__main__":
  main()