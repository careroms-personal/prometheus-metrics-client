import sys
from pathlib import Path

import csv
from datetime import datetime

from models.processor_model import ProcessorResult
from models.promql_model import OutputConfig

def write_csv(processor_result: ProcessorResult, output_config: OutputConfig):
  csv_file = Path(output_config.base_directory) / f"{processor_result.query_name}.csv"
  csv_file.parent.mkdir(parents=True, exist_ok=True) 

  all_metric_keys = set()
  for data in processor_result.datas:
    all_metric_keys.update(data.metric.keys())

  metric_column_name = sorted(list(all_metric_keys)) 
  csv_rows = [[*metric_column_name, "datetime", "timestamp", "value"]]

  for data in processor_result.datas:
    metric_column_data = [data.metric.get(key, '') for key in metric_column_name]

    for pr_value in data.values:
      timestamp, value = pr_value[0], pr_value[1]
      dt = datetime.fromtimestamp(float(timestamp))
      dt_str = dt.strftime('%Y-%m-%d %H:%M:%S')

      row = [ *metric_column_data, dt_str, timestamp, value]

      csv_rows.append(row)

  with open(csv_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(csv_rows)
    
  print(f"   💾 Saved to: {csv_file}")
    

  # metric_column_name = [k for k,v in processor_result.data.metric.items()]
  # metric_column_data = [v for k,v in processor_result.data.metric.items()]

  # csv_rows = [[*metric_column_name, "datetime", "timestamp", "value"]]

  # for pr_value in processor_result.data.values:
  #   timestamp, value = pr_value[0], pr_value[1]

  #   dt = datetime.fromtimestamp(float(timestamp))
  #   dt_str = dt.strftime('%Y-%m-%d %H:%M:%S')

  #   row = [*metric_column_data,dt_str,timestamp,value]

  #   csv_rows.append(row)
  
  # with open(csv_file, 'w', newline='') as f:
  #   writer = csv.writer(f)
  #   writer.writerows(csv_rows)

  # print(f"   💾 Saved to: {csv_file}")