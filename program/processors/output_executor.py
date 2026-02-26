from typing import List

from models.processor_model import ProcessorResult
from models.promql_model import OutputConfig, OutputFormatType
from .exporters.csv_exporter import write_csv
from .exporters.json_exporter import write_json

class OutputExecutor:
  def __init__(self, processor_results: List[ProcessorResult], output_config: OutputConfig):
    self.processor_results = processor_results
    self.output_config = output_config

    self.exporter_selector = {
      OutputFormatType.CSV : write_csv,
      OutputFormatType.JSON: write_json,
    }

  def _process_output(self):
    if self.output_config is None:
      return

    if self.output_config.print_output:
      print(self.processor_results)

    if self.output_config.write_options:
      for write_option in self.output_config.write_options:
        if write_option.format in self.exporter_selector:
          write_function = self.exporter_selector.get(write_option.format)

          for result in self.processor_results:
            write_function(result, write_option)
        else:
          print(f"❌ Unsupported format: {write_option.format}")

  def execute(self):
    self._process_output()