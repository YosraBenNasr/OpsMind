sequenceDiagram
    autonumber
    participant App as Application K8s
    participant Obs as Observability (Prometheus/Logs)
    participant Engine as Incident Engine
    participant Agent as Agent IA (LangGraph + Ollama)
    participant Git as GitHub (GitOps)
    participant Argo as Argo CD

    App->>Obs: Génération de logs / erreurs
    Obs->>Engine: Détection d'anomalie / Crash
    Engine->>Agent: Transmission de l'IncidentContext
    Agent->>Agent: Analyse RCA + Sélection de l'outil
    Agent->>Git: Push du correctif (YAML / Code)
    Git->>Argo: Déclenchement de la synchronisation
    Argo->>App: Déploiement de la correction sur K8s
    Agent->>App: Verification du statut (Health Check)
    alt Succès
        Agent-->>Engine: Clôture de l'incident
    else Échec
        Agent->>Git: Git Rollback
    end