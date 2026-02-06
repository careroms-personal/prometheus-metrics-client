import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import List

from models.processor_model import ProcessorResult
from models.promql_model import OutputConfig, OutputFormatType
from .exporters.csv_exporter import write_csv

class OutputExecutor:
  def __init__(self, processor_results: List[ProcessorResult], output_config: OutputConfig):
    self.processor_results = processor_results
    self.output_config = output_config

    self.exporter_selector = {
      OutputFormatType.CSV : write_csv
    }

  def _process_output(self):
    if self.output_config.print_output == True:
      print(self.processor_results)

    if self.output_config.write_output == True:
      if self.output_config.format in self.exporter_selector:
        write_function = self.exporter_selector.get(self.output_config.format)

        # Processor result is list of all queries result from queries config, this is write result one by one
        for result in self.processor_results:
          write_function(result, self.output_config)  
          
      else:
        print(f"❌ Unsupported format: {self.output_config.format}")

  def execute(self):
    self._process_output()