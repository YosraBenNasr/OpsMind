from typing import Any, Dict
from app.agent.state import AlertPayload

def parse_alertmanager_webhook(payload: Dict[str, Any]) -> AlertPayload:
    """
    Extrait les données pertinentes d'un payload Webhook Alertmanager
    et les formate selon le schéma AlertPayload.
    """
    alerts = payload.get("alerts", [])
    if not alerts:
        # Payload de secours ou alerte brute isolée
        first_alert = payload
    else:
        first_alert = alerts[0]

    labels = first_alert.get("labels", {})
    annotations = first_alert.get("annotations", {})

    return AlertPayload(
        alert_name=labels.get("alertname", "UnknownAlert"),
        severity=labels.get("severity", "warning"),
        status=first_alert.get("status", "firing"),
        instance=labels.get("instance", "unknown"),
        namespace=labels.get("namespace", "opsmind"),
        pod_name=labels.get("pod") or labels.get("pod_name"),
        summary=annotations.get("summary", "Pas de résumé fourni."),
        description=annotations.get("description", "Pas de description fournie."),
        raw_labels=labels
    )