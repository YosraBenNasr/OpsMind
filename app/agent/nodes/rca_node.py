from typing import Dict, Any
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from app.agent.state import AgentState

# Initialisation du modèle local Ollama
llm = ChatOllama(model="llama3.2", base_url="http://localhost:11434", temperature=0.1)

def generate_rca_node(state: AgentState) -> Dict[str, Any]:
    """
    Nœud final qui analyse l'ensemble des contextes récoltés et génère 
    un rapport d'incident complet avec recommandation d'action.
    """
    alert = state.get("alert", {})
    k8s_describe = state.get("k8s_describe", "Non disponible.")
    k8s_logs = state.get("k8s_logs", "Non disponible.")
    prometheus_metrics = state.get("prometheus_metrics", "Non disponible.")
    rag_context = state.get("rag_context", [])

    context_str = "\n---\n".join(rag_context) if rag_context else "Aucun incident similaire trouvé dans la base vectorielle."

    system_prompt = """Tu es OpsMind AI, un ingénieur SRE (Site Reliability Engineering) expert Kubernetes et observabilité.
Ton rôle est d'analyser l'alerte reçue, les données d'inspection Kubernetes, les métriques Prometheus et l'historique RAG d'incidents pour fournir une Analyse des Causes Racines (RCA) concise et actionnable.

Le rapport doit obligatoirement respecter la structure Markdown suivante :
# 🚨 Rapport d'Incident SRE - OpsMind AI

## 1. Résumé de l'Alerte
- **Nom de l'alerte :** ...
- **Sévérité :** ...
- **Cible :** ...

## 2. Analyse Diagnostique & Preuves
- Synthèse des événements Kubernetes (`describe`) et des logs applicatifs.
- Analyse des métriques observées.

## 3. Cause Racine Identifiée (RCA)
- Explication précise de l'origine du problème (ex: OOMKilled, erreur de syntaxe, panne DB, etc.).
- Lien fait avec l'historique d'incidents RAG (si applicable).

## 4. Plan de Remédiation & Recommandations
- Actions immédiates à effectuer via `kubectl` ou révision de code/manifestes.
"""

    user_content = f"""
### DONNÉES DE L'ALERTE :
- Alerte: {alert.get('alert_name')}
- Sévérité: {alert.get('severity')}
- Pod Cible: {alert.get('pod_name')}
- Namespace: {alert.get('namespace')}
- Description: {alert.get('description')}

### INSPECTION KUBERNETES (DESCRIBE) :{k8s_describe}

### LOGS RECENTES DU POD :{k8s_logs}

### MÉTRIQUES PROMETHEUS :{prometheus_metrics}

### HISTORIQUE RAG (INCIDENTS SIMILAIRES) :{context_str}
"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_content)
    ]

    response = llm.invoke(messages)
    rca_report = response.content

    print("📄 [Nœud RCA] Rapport d'incident généré avec succès par le LLM local.")
    return {"rca_report": rca_report}