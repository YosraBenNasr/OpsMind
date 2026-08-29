import requests
from langchain_core.tools import tool

PROMETHEUS_URL = "http://prometheus-kube-prometheus-prometheus.monitoring.svc.cluster.local:9090"
# Si exécuté hors cluster via port-forward, fallback sur localhost
LOCAL_PROMETHEUS_URL = "http://localhost:9090"

@tool
def query_prometheus_metric(query: str) -> str:
    """
    Exécute une requête PromQL instantanée sur le serveur Prometheus.
    Permet de vérifier la consommation CPU, RAM, le taux de requêtes HTTP ou le taux d'erreurs 5xx.
    Exemples de requêtes :
    - sum(rate(opsmind_api_requests_total[1m]))
    - container_memory_working_set_bytes{namespace='opsmind'}
    """
    # Essayer l'adresse In-Cluster d'abord, puis l'adresse locale
    urls_to_try = [PROMETHEUS_URL, LOCAL_PROMETHEUS_URL]
    
    for base_url in urls_to_try:
        try:
            response = requests.get(
                f"{base_url}/api/v1/query",
                params={"query": query},
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    result = data.get("data", {}).get("result", [])
                    if not result:
                        return f"Requête exécutée avec succès mais aucun résultat retourné pour : '{query}'"
                    return str(result)
        except requests.exceptions.RequestException:
            continue

    return f"Impossible de contacter Prometheus sur {urls_to_try}. Vérifiez l'accès au service."