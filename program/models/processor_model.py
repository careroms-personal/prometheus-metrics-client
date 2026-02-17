from pydantic import BaseModel
from typing import List, Dict, Union, Optional

class ProcessorResultData(BaseModel):
  metric: Dict[str, str]
  values: List[List[Union[float, str]]]

class ProcessorResult(BaseModel):
  query_name: str
  query_type: str
  promql: str
  internal_workflows: Optional[List[str]] = None
  datas: List[ProcessorResultData]