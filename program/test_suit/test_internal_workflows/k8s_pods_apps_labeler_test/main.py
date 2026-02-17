from models.internal_workflows.k8s_pods_apps_label_model import K8SAppsList, K8SPodsAppsLabelerConfig
from processors.internal_workflows.k8s_pods_apps_labeler import K8SPodsAppsLabelerWorkflow

def main():
  k8s_app_list = K8SAppsList(
    deployments=[
      "api-order",
      "api-gateway",
      "api-product"
    ],
    statefulsets=[
      "postgres",
    ],
    daemonsets=[
      "fluentd"
    ],
    cronjobs=[],
  )

  k8s_pods_apps_labeler_config = K8SPodsAppsLabelerConfig(
    name="k8s_pods_apps_labeler",
    config=k8s_app_list
  )

  workflow = K8SPodsAppsLabelerWorkflow(
    workflow_config=k8s_pods_apps_labeler_config
  )

  workflow.execute()

if __name__ == "__main__":
  main()