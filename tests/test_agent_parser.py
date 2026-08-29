from app.agent.parser import parse_alertmanager_webhook

def test_parse_alertmanager_webhook():
    sample_payload = {
        "status": "firing",
        "alerts": [
            {
                "status": "firing",
                "labels": {
                    "alertname": "PodCrashLoopBackOff",
                    "severity": "critical",
                    "namespace": "opsmind",
                    "pod": "opsmind-app-7d9b8c6f-x4z1"
                },
                "annotations": {
                    "summary": "Pod is crashing continuously",
                    "description": "Pod opsmind-app in namespace opsmind is in CrashLoopBackOff."
                }
            }
        ]
    }
    
    parsed = parse_alertmanager_webhook(sample_payload)
    
    assert parsed["alert_name"] == "PodCrashLoopBackOff"
    assert parsed["severity"] == "critical"
    assert parsed["namespace"] == "opsmind"
    assert parsed["pod_name"] == "opsmind-app-7d9b8c6f-x4z1"