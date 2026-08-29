from langgraph.graph import StateGraph, END
from app.agent.state import AgentState
from app.agent.nodes.rag_node import rag_node
from app.agent.nodes.inspection_node import auto_inspection_node
from app.agent.nodes.rca_node import generate_rca_node

def build_opsmind_graph():
    """
    Construit et compile le StateGraph LangGraph d'OpsMind.
    
    Flux d'exécution :
    [START] ──► rag_search ──► auto_inspection ──► generate_rca ──► [END]
    """
    workflow = StateGraph(AgentState)

    # 1. Ajout des nœuds
    workflow.add_node("rag_search", rag_node)
    workflow.add_node("auto_inspection", auto_inspection_node)
    workflow.add_node("generate_rca", generate_rca_node)

    # 2. Configuration du flux (Arête / Edges)
    workflow.set_entry_point("rag_search")
    workflow.add_edge("rag_search", "auto_inspection")
    workflow.add_edge("auto_inspection", "generate_rca")
    workflow.add_edge("generate_rca", END)

    # 3. Compilation du graphe
    app_graph = workflow.compile()
    return app_graph

# Instance globale réutilisable du graphe d'agent OpsMind
opsmind_agent = build_opsmind_graph()