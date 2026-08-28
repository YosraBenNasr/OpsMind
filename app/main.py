from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

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