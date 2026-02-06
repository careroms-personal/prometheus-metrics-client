from pydantic import BaseModel
from typing import List, Literal, Optional
from enum import StrEnum

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

class OutputConfig(BaseModel):
  base_directory: str = ""
  print_output: bool = False
  write_output: bool = False
  format: Optional[OutputFormatType] = OutputFormatType.CSV
  timestamp_subdirectory: bool = False

class QueryConfig(BaseModel):
  name: str
  version: str
  connection: ConnectionConfig
  queries: List[QueryItem]
  output: Optional[OutputConfig]