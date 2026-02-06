"""
Prometheus client for querying metrics.
"""
import sys

from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import requests

from global_config import *
from models.promql_model import ConnectionConfig

class PrometheusClient:
  """Basic Prometheus HTTP API client."""

  def __init__(self, connection_config: ConnectionConfig):
    """
    Initialize Prometheus client.
    
    url: Prometheus server URL with HTTP or HTTPS.
    timeout: Request timeout in seconds (default 30 sec)
    """

    self.url = connection_config.url
    self.timeout = connection_config.timeout
    self.api_query_path = connection_config.api_query_path
    self.session = requests.Session()

    self.test_connection()

  def test_connection(self):
    endpoint = f"{self.url}/{self.api_query_path}/query"
    params = {"query": TEST_CONNECTION_PROMQL}

    try:
      response = self.session.get(
        endpoint,
        params=params,
        timeout=self.timeout,
      )

      response.raise_for_status()
      data = response.json()

      print("✅ Connection successful!")
      print(f"Prometheus info: {data['data']['result']}")

      return response
      
    except Exception as e:
      print(f"❌ Connection failed: {e}")
      sys.exit(1)