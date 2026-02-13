"""
Executes Prometheus queries and returns structured results
"""



from datetime import datetime, timedelta
from typing import Dict, Any, List
from models.promql_model import QueryItem, ConnectionConfig
from models.processor_model import ProcessorResult, ProcessorResultData
from connector.client import PrometheusClient

class QueryExecutor:
  def __init__(self, client: PrometheusClient, connection_config: ConnectionConfig, query_items: List[QueryItem]):
    self.connection_config = connection_config
    self.query_items = query_items
    self.client = client
    self.results = []

  def _parse_time(self, time_str: str) -> float:
    if time_str == "now":
      return datetime.now().timestamp()
    
    try:
      return float(time_str)
    except ValueError:
      pass

    try:
      dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
      return dt.timestamp()
    except ValueError:
      pass

    if time_str.endswith('d'):
      days = int(time_str[:-1])
      return (datetime.now() - timedelta(days=days)).timestamp()
    elif time_str.endswith('h'):
      hours = int(time_str[:-1])
      return (datetime.now() - timedelta(hours=hours)).timestamp()
    elif time_str.endswith('m'):
      minutes = int(time_str[:-1])
      return (datetime.now() - timedelta(minutes=minutes)).timestamp()
  
    raise ValueError(f"Invalid time format: {time_str}")

  def _set_query_params(self, query_item: QueryItem) -> Dict[str, Any]:
    
    if query_item.type == "query":
      params = {
        "query": query_item.promql
      }
    elif query_item.type == "query_range":
      if not all([query_item.start, query_item.end, query_item.step]):
        print(f"❌ Query '{query_item.name}': query_range requires start, end, and step")
        return None

      try:
        start_ts = self._parse_time(query_item.start)
        end_ts = self._parse_time(query_item.end)
      except ValueError as e:
        print(f"❌ Query '{query_item.name}': {e}")
        return None
      
      params = {
        "query": query_item.promql,
        "start": start_ts,
        "end": end_ts,
        "step": query_item.step
      }
    else:
      print(f"❌ Query type of {query_item.name} must be 'query' or 'query_range")
      return None


    return params

  def execute(self) -> List[ProcessorResult]:
    """Execute queries and return results"""
    endpoint = f"{self.connection_config.url}/{self.connection_config.api_query_path}"

    for query in self.query_items:
      params = self._set_query_params(query)
      query_results = []

      if params is None:
        print(f"⚠️ Skipping query '{query.name}'")
        continue

      try:
        response = self.client.session.get(
          f"{endpoint}/{query.type}",
          params=params,
          timeout=self.connection_config.timeout
        )

        response.raise_for_status()
        data = response.json()
        data_results = data['data']['result']
        
        for data_result in data_results:
          metric = data_result.get("metric", {})
          values = data_result.get("values") or ([data_result['value']] if "value" in data_result else [])
          
          export_metric = {}

          if query.export_config:
            if query.export_config.export_all_metric:
              export_metric = metric
            elif query.export_config.export_metric_key:
              export_metric = {
                k: v for k, v in metric.items()
                if k in query.export_config.export_metric_key
              }

          query_results.append(ProcessorResultData(
            metric=export_metric,
            values=values
          ))

        self.results.append(ProcessorResult(
          query_name=query.name,
          query_type=query.type,
          promql=query.promql,
          datas=query_results,
        ))

      except Exception as e:
        print(f"❌ Query '{query.name}' failed: {e}")
        continue

    return self.results