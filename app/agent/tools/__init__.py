from app.agent.tools.k8s_tools import get_pod_logs, describe_pod
from app.agent.tools.prometheus_tools import query_prometheus_metric

# Liste complète des outils mis à disposition du LLM
sre_agent_tools = [
    get_pod_logs,
    describe_pod,
    query_prometheus_metric
]