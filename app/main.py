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