from app.agent.state import AgentState
from app.agent.rag import retrieve_incident_context

def rag_node(state: AgentState) -> dict:
    """
    Nœud LangGraph qui extrait les informations de l'alerte
    et interroge la base FAISS pour alimenter state['rag_context'].
    """
    alert = state.get("alert", {})
    alert_name = alert.get("alert_name", "")
    description = alert.get("description", "")
    summary = alert.get("summary", "")

    # Construction d'une requête globale enrichie
    search_query = f"{alert_name} {summary} {description}"
    
    print(f"🔍 [Nœud RAG] Recherche d'incidents similaires pour : '{alert_name}'")
    retrieved_docs = retrieve_incident_context(search_query, top_k=2)

    return {
        "rag_context": retrieved_docs
    }