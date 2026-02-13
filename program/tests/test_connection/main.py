import os

from connector.client import PrometheusClient
from models.promql_model import ConnectionConfig

def main():
  url = os.getenv("URL")
  api_query_path = os.getenv("API_PATH")

  connection_config = ConnectionConfig(
    url=url,
    api_query_path=api_query_path,
    timeout=30
  )

  PrometheusClient(
    connection_config=connection_config
  )

if __name__ == "__main__":
  main()