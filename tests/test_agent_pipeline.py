import pytest
from app.agent.graph import opsmind_agent


async def test_full_agent_workflow():
    fake_alert = {
        "alert_name": "PodOOMKilled",
        "severity": "critical",
        "status": "firing",
        "instance": "opsmind-app",
        "namespace": "opsmind",
        "pod_name": "opsmind-app-test",
        "summary": "Pod killed due to high memory consumption",
        "description": "Container exceeded 128Mi limit with exit code 137.",
        "raw_labels": {}
    }

    initial_state = {
        "messages": [],
        "alert": fake_alert,
        "k8s_describe": None,
        "k8s_logs": None,
        "prometheus_metrics": None,
        "rag_context": None,
        "rca_report": None
    }

    result = await opsmind_agent.ainvoke(initial_state)

    assert result["rag_context"] is not None
    assert result["k8s_describe"] is not None
    assert result["rca_report"] is not None
    assert "OpsMind AI" in result["rca_report"] or "Rapport" in result["rca_report"]