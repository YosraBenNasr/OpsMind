import subprocess
from langchain_core.tools import tool

@tool
def get_pod_logs(pod_name: str, namespace: str = "opsmind", tail_lines: int = 100) -> str:
    """
    Extrait les derniers logs d'un Pod Kubernetes spécifique.
    À utiliser pour analyser les erreurs applicatives ou les traces d'exception.
    """
    try:
        cmd = [
            "kubectl", "logs", pod_name,
            "-n", namespace,
            f"--tail={tail_lines}"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        
        if result.returncode != 0:
            return f"Erreur lors de la récupération des logs ({pod_name}): {result.stderr}"
        
        return result.stdout if result.stdout else "Aucun log généré par ce Pod."
    
    except subprocess.TimeoutExpired:
        return "Timeout lors de l'exécution de kubectl logs."
    except Exception as e:
        return f"Échec de la commande get_pod_logs: {str(e)}"

@tool
def describe_pod(pod_name: str, namespace: str = "opsmind") -> str:
    """
    Exécute 'kubectl describe pod' pour obtenir les événements, l'état du conteneur,
    les ressources allouées et les raisons de crash (ex: OOMKilled, ImagePullBackOff).
    """
    try:
        cmd = ["kubectl", "describe", "pod", pod_name, "-n", namespace]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        
        if result.returncode != 0:
            return f"Erreur lors du describe du pod ({pod_name}): {result.stderr}"
        
        return result.stdout
    
    except subprocess.TimeoutExpired:
        return "Timeout lors de l'exécution de kubectl describe."
    except Exception as e:
        return f"Échec de la commande describe_pod: {str(e)}"