from fastapi import FastAPI

app = FastAPI(
    title="OpsMind Monitored App",
    description="Target service monitored by OpsMind agent",
    version="0.1.0"
)

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