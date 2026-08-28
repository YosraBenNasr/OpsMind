# Incident #04 : Épuisement mémoire et conteneur tué par l'OS (OOMKilled / CrashLoopBackOff)

## 1. Description & Symptômes
- **Symptôme :** Le Pod redémarre brutalement avec le statut `OOMKilled` (Exit Code 137) puis bascule en `CrashLoopBackOff`.
- **Impact :** Interruptions de service temporaires, perte de l'état en mémoire vive et dégradation des métriques de disponibilité (Erreurs 502/503).

## 2. Investigation (Commandes & Constats)
- `kubectl get pods -n opsmind` : Affiche `STATUS: OOMKilled` ou `CrashLoopBackOff` (Restarts > 0).
- `kubectl describe pod -l app=opsmind-app -n opsmind` : La section `Last State` indique `Terminated`, `Reason: OOMKilled`, `Exit Code: 137`.
- **Dashboard Grafana :** Le graphique `Pod Memory Usage` montre une consommation atteignant le plafond strict des `128Mi` avant une rupture nette.

## 3. Root Cause Analysis (RCA)
Une consommation excessive de mémoire (simulée via l'endpoint `/stress/memory`) a fait dépasser la limite `resources.limits.memory: 128Mi` définie dans `k8s/deployment.yaml`. Le sous-système cgroups du noyau Linux a déclenché l'OOM Killer pour stopper le conteneur.

## 4. Correctif
1. Supprimer ou corriger l'endpoint responsable de la fuite de mémoire applicative.
2. Diminuer l'accumulation en mémoire et réajuster les limites `resources.limits.memory` à une valeur réaliste pour la production (ex: `256Mi` ou `512Mi`).