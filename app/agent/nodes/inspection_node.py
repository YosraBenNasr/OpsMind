from typing import Dict, Any
from app.agent.state import AgentState
from app.agent.tools import get_pod_logs, describe_pod, query_prometheus_metric

def auto_inspection_node(state: AgentState) -> Dict[str, Any]:
    """
    Nœud qui exécute automatiquement les outils SRE de diagnostic 
    en se basant sur le Pod et le Namespace identifiés dans l'alerte.
    """
    alert = state.get("alert", {})
    pod_name = alert.get("pod_name")
    namespace = alert.get("namespace", "opsmind")

    k8s_describe_res = "Pod non spécifié dans l'alerte."
    k8s_logs_res = "Pod non spécifié dans l'alerte."
    prom_res = "Aucune métrique demandée."

    if pod_name:
        print(f"🛠️ [Inspection Node] Exécution de kubectl describe & logs sur {pod_name}...")
        k8s_describe_res = describe_pod.invoke({"pod_name": pod_name, "namespace": namespace})
        k8s_logs_res = get_pod_logs.invoke({"pod_name": pod_name, "namespace": namespace, "tail_lines": 100})
    
    # Métrique générale pour vérifier l'état du Pod/Memory/CPU
    print("🛠️ [Inspection Node] Interrogation de Prometheus...")
    prom_res = query_prometheus_metric.invoke({
        "query": f'container_memory_working_set_bytes{{namespace="{namespace}"}}'
    })

    return {
        "k8s_describe": k8s_describe_res,
        "k8s_logs": k8s_logs_res,
        "prometheus_metrics": {"container_memory": prom_res}
    }