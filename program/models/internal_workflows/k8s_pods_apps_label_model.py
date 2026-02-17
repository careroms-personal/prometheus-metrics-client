from pydantic import BaseModel
from typing import Optional, List

class K8SAppsList(BaseModel):
  deployments: Optional[List[str]] = None
  statefulsets: Optional[List[str]] = None
  daemonsets: Optional[List[str]] = None
  cronjobs: Optional[List[str]] = None

class K8SPodsAppsLabelerConfig(BaseModel):
  name: str
  config: Optional[K8SAppsList] = None