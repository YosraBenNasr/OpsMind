from app.agent.tools import get_pod_logs, describe_pod, query_prometheus_metric

def test_k8s_tools_execution():
    # Test d'invocation directe des outils LangChain sur un pod inexistant pour vérifier le comportement d'erreur propre
    describe_res = describe_pod.invoke({"pod_name": "non-existent-pod", "namespace": "opsmind"})
    assert "Erreur" in describe_res or "NotFound" in describe_res

    logs_res = get_pod_logs.invoke({"pod_name": "non-existent-pod", "namespace": "opsmind"})
    assert "Erreur" in logs_res or "NotFound" in logs_res

def test_prometheus_tool_structure():
    # Test avec une requête simple
    prom_res = query_prometheus_metric.invoke({"query": "up"})
    assert isinstance(prom_res, str)