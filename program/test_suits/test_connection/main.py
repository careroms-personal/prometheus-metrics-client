import os

from connector.client import PrometheusClient
from test_suit.global_test_config import CONNECTION_CONFIG

def main():
  PrometheusClient(
    connection_config=CONNECTION_CONFIG
  )

if __name__ == "__main__":
  main()