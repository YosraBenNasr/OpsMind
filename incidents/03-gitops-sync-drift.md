# Incident #03 : Échec de synchronisation GitOps & Dérive (Sync Drift / Sync Failed)

## 1. Description & Symptômes
- **Symptôme :** L'application Argo CD passe au statut `Sync Failed` / `OutOfSync`. Le moteur GitOps est bloqué et ne peut plus appliquer les mises à jour.
- **Impact :** Blocage de la chaîne de déploiement continu (CD). Les modifications ultérieures poussées dans Git ne sont plus répercutées sur le cluster.

## 2. Investigation (Commandes & Constats)
- `argocd app get opsmind-app` : Affiche l'état `Sync Status: Sync Failed`.
- **Dashboard Argo CD :** La bannière d'erreur indique : `json: cannot unmarshal string into Go struct field DeploymentSpec.spec.replicas of type int32`.
- `kubectl get pods -n opsmind` : Le cluster continue d'exécuter l'ancienne version valide, mais la réconciliation automatique est interrompue.

## 3. Root Cause Analysis (RCA)
Présence d'une erreur de type/schema YAML dans le manifeste `k8s/deployment.yaml` commité sur la branche principale (`replicas: "invalid_number"` au lieu d'un entier). L'API Server Kubernetes rejette le manifeste lors de la tentative d'application par Argo CD.

## 4. Correctif
Corriger la valeur du champ `spec.replicas` dans `k8s/deployment.yaml` en remettant un entier valide (`1`), commiter et pusher la modification sur la branche `main` pour permettre à Argo CD de finaliser la synchronisation.