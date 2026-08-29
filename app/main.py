from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from fastapi import FastAPI, Request, BackgroundTasks
from app.agent.parser import parse_alertmanager_webhook



from fastapi import FastAPI, Request, BackgroundTasks
from app.agent.parser import parse_alertmanager_webhook
from app.agent.graph import opsmind_agent



app = FastAPI(
    title="OpsMind Monitored App",
    description="Target service monitored by OpsMind agent",
    version="0.1.0"
)



# Activation du middleware et exposition automatique de l'endpoint /metrics
Instrumentator().instrument(app).expose(app, endpoint="/metrics")


@app.get("/")
def root():
    return {
        "project": "OpsMind",
        "status": "running",
        "version": "0.1.0"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }



# Liste globale pour accumuler des données en mémoire vive
memory_leak_store = []

@app.get("/stress/memory")
def simulate_memory_leak():
    # Allocation d'environ 50 Mo de données par requête
    chunk = "X" * (50 * 1024 * 1024)
    memory_leak_store.append(chunk)
    return {
        "message": "Allocated 50MB of memory",
        "total_chunks": len(memory_leak_store),
        "estimated_mb": len(memory_leak_store) * 50
    }




async def run_agent_workflow(alert_payload: dict):
    """Fonction exécutée en tâche de fond lors d'une alerte."""
    initial_state = {
        "messages": [],
        "alert": alert_payload,
        "k8s_describe": None,
        "k8s_logs": None,
        "prometheus_metrics": None,
        "rag_context": None,
        "rca_report": None
    }
    
    # Exécution du graphe LangGraph
    final_state = await opsmind_agent.ainvoke(initial_state)
    
    print("\n=================== RAPPORT RCA GÉNÉRÉ ===================")
    print(final_state.get("rca_report"))
    print("==========================================================\n")

@app.post("/api/v1/alerts")
async def handle_alertmanager_webhook(request: Request, background_tasks: BackgroundTasks):
    payload = await request.json()
    parsed_alert = parse_alertmanager_webhook(payload)
    
    print(f"🚨 [ALERTE REÇUE] {parsed_alert['alert_name']} sur {parsed_alert['pod_name']}")
    
    # Lancement du graphe LangGraph en arrière-plan
    background_tasks.add_task(run_agent_workflow, parsed_alert)
    
    return {
        "status": "processing",
        "alert": parsed_alert["alert_name"],
        "message": "OpsMind Agent SRE déclenché."
    }