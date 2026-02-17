from pydantic import BaseModel
from typing import List, Literal, Optional
from enum import StrEnum

class Workflows(BaseModel):
  internal: List[str]

class OutputFormatType(StrEnum):
  CSV = "csv"
  JSON = "json"

class ConnectionConfig(BaseModel):
  url: str
  api_query_path: str
  timeout: int

class QueryExportConfig(BaseModel):
  export_all_metric: Optional[bool] = False
  export_metric_key: Optional[List[str]] = None

class QueryItem(BaseModel):
  name: str
  type: Literal["query", "query_range"] = "query"
  promql: str

  #Range Query
  start: Optional[str] = None
  end: Optional[str] = None
  step: Optional[str] = None

  #Export option
  export_config: Optional[QueryExportConfig] = None

  #Workflow option
  workflows: Optional[Workflows] = None

class OutputWriteOption(BaseModel):
  base_directory: str
  format: OutputFormatType

class OutputConfig(BaseModel):
  print_output: bool = False
  write_options: List[OutputWriteOption]

class QueryConfig(BaseModel):
  name: str
  connection: ConnectionConfig
  queries: List[QueryItem]
  internal_workflows: Optional[List[dict]] = None
  output: Optional[OutputConfig] = None