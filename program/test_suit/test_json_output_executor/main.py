from test_suit.global_test_config import *

from connector.client import PrometheusClient
from processors.output_executor import OutputExecutor
from processors.query_executor import QueryExecutor
from models.promql_model import OutputWriteOption, OutputFormatType, OutputConfig

def main():
  output_config = OutputConfig(
    print_output=False,
    write_options=[
      OutputWriteOption(
        base_directory="./result",
        format=OutputFormatType.JSON,
      )
    ]
  )

  client = PrometheusClient(connection_config=CONNECTION_CONFIG)

  query_range_results = QueryExecutor(
    client=client,
    query_items=[
      TEST_QUERY_PROMETHEUS_CPU,
      TEST_QUERY_PROMETHEUS_MEMORY,
    ],
  ).execute()

  output_executor = OutputExecutor(
    processor_results=query_range_results,
    output_config=output_config,
  )

  output_executor.execute()

if __name__ == "__main__":
  main()