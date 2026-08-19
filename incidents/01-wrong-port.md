# Incident #01 : Mismatch de port d'application (Wrong Port)

## 1. Description & Symptômes
- **Symptôme :** L'application `opsmind-app` est inaccessible via l'URL du Service Kubernetes.
- **Impact :** Échec des requêtes HTTP (Connection Refused / Timeout).

## 2. Investigation (Commandes & Constats)
- `kubectl get pods -n opsmind` : Le pod est en état `Running` (fausses indications de santé globale).
- `kubectl logs -l app=opsmind-app -n opsmind` : L'application FastAPI démarre correctement sur le port **8000**.
- `kubectl describe deployment opsmind-app -n opsmind` : Le manifeste Kubernetes définit `containerPort: 8080`.

## 3. Root Cause Analysis (RCA)
Discordance de configuration entre le port exposé par l'image Docker (8000) et la déclaration `containerPort` du Deployment Kubernetes (8080). Le trafic routé par le Service vers le port 8080 du pod ne trouve aucun processus à l'écoute.

## 4. Correctif
Remettre `containerPort: 8000` dans le fichier `k8s/deployment.yaml` et réappliquer le manifeste.