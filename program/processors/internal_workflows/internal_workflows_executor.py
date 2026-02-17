from models.processor_model import ProcessorResult
from .k8s_pod_apps_label import k8s_pod_apps_label

class InternalWorkflowsExecutor:
  def __init__(self, processor_outputs: list[ProcessorResult]):
    self.internal_workflow_selector = {

    }