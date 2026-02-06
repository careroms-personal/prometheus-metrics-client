from pydantic import BaseModel
from typing import List, Dict, Union

class ProcessorResultData(BaseModel):
  metric: Dict[str, str]
  values: List[List[Union[float, str]]]

class ProcessorResult(BaseModel):
  query_name: str
  query_type: str
  promql: str
  datas: List[ProcessorResultData]