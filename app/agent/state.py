from typing import Annotated, Any, Dict, List, Optional
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AlertPayload(TypedDict):
    """Structure normalisée d'une alerte reçue depuis Alertmanager."""
    alert_name: str
    severity: str
    status: str  # firing / resolved
    instance: str
    namespace: str
    pod_name: Optional[str]
    summary: str
    description: str
    raw_labels: Dict[str, str]

class AgentState(TypedDict):
    """État global du graphe LangGraph OpsMind."""
    # Historique de conversation et d'appels d'outils (utilisant le réducteur add_messages)
    messages: Annotated[List[BaseMessage], add_messages]
    
    # Données structurées de l'alerte déclencheuse
    alert: AlertPayload
    
    # Données d'inspection collectées par les outils (K8s describe, logs, métriques)
    k8s_describe: Optional[str]
    k8s_logs: Optional[str]
    prometheus_metrics: Optional[Dict[str, Any]]
    
    # Contexte extrait de la base vectorielle d'incidents (RAG)
    rag_context: Optional[List[str]]
    
    # Rapport final d'Analyse des Causes Racines (RCA)
    rca_report: Optional[str]