# Architecture V1 - OpsMind Platform

## Composants Actuels

1. **Application Cible (`app/`)** : API REST développée avec FastAPI et exposant `/` et `/health`.
2. **Conteneurisation (`Dockerfile`)** : Image `opsmind-app:v1` exécutant l'application sur Python 3.10-slim.
3. **Orchestration (`k8s/`)** : Déploiement sur cluster Minikube local sous le namespace `opsmind` via Deployment et Service (NodePort 30080).
4. **Moteur d'IA Local (`Ollama`)** : Exécution locale du modèle pour l'analyse future des logs et incidents.

## Schéma de Flux

Developer -> Git/GitHub -> Docker Build -> Minikube (Deployment/Pod/Service) -> Ollama (LLM)