"""
Extract Prometheus data from query result
"""

import yaml, sys

from pathlib import Path
from pydantic import ValidationError
from connector.client import PrometheusClient
from models.promql_model import *
from .query_executor import QueryExecutor
from .output_executor import OutputExecutor

class Processor:
  def __init__(self, config_path: str):
    self._load_and_validate_config(config_path=config_path)
    self.client = PrometheusClient(self.query_config.connection)

  def _load_and_validate_config(self, config_path: str):
    if not Path(config_path).exists():
      print(f"❌ Config file not found: {config_path}")
      sys.exit(1)

    try:
      with open(config_path, 'r') as f:
        yaml_data = yaml.safe_load(f)
        self.query_config = QueryConfig(**yaml_data)
        
    except ValidationError as e:
      print(f"❌ Invalid config file:")

      for error in e.errors():
        print(f"   - {error['loc']}: {error['msg']}")
      
      sys.exit(1)

  def execute(self):
    self.query_executor = QueryExecutor(self.client, self.query_config.queries)
    self.results = self.query_executor.execute()

    self.output_executor = OutputExecutor(self.results, self.query_config.output)
    self.output_executor.execute()