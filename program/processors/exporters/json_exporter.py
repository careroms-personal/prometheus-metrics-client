import json

from pathlib import Path
from datetime import datetime

from models.processor_model import ProcessorResult
from models.promql_model import OutputWriteOption

def write_json(processor_result: ProcessorResult, output_write_config: OutputWriteOption):
  json_file = Path(output_write_config.base_directory) / f"{processor_result.query_name}.json"
  json_file.parent.mkdir(parents=True, exist_ok=True)
 
  records = []

  for data in processor_result.datas:
    values = []

    for pr_value in data.values:
      timestamp, value = pr_value[0], pr_value[1]
      dt = datetime.fromtimestamp(float(timestamp))
      dt_str = dt.strftime('%Y-%m-%d %H:%M:%S')

      values.append({
        "datetime": dt_str,
        "timestamp": timestamp,
        "value": value,
      })

    records.append({
      "metric": data.metric,
      "values": values,
    })
  
  with open(json_file, 'w') as f:
    json.dump(records, f, indent=2)

  print(f"   💾 Saved to: {json_file}")