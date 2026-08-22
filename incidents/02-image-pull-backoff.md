# Incident #02 : Erreur de récupération d'image conteneur (ImagePullBackOff)

## 1. Description & Symptômes
- **Symptôme :** Le Pod ne parvient pas à démarrer et reste bloqué en statut `ImagePullBackOff` / `ErrImagePull`.
- **Impact :** Indisponibilité totale du déploiement (`0/1` réplicas prêts). Le trafic HTTP renvoie une erreur `503 Service Unavailable`.

## 2. Investigation (Commandes & Constats)
- `kubectl get pods -n opsmind` : Le Pod affiche le statut `ImagePullBackOff`.
- `kubectl describe pod -l app=opsmind-app -n opsmind` : La section `Events` montre l'erreur `rpc error: code = NotFound desc = failed to pull and unpack image`.
- `kubectl logs -l app=opsmind-app -n opsmind` : Aucun log applicatif disponible car le conteneur n'a jamais pu être instancié sur le nœud.

## 3. Root Cause Analysis (RCA)
La clé `image` spécifiée dans le manifest `k8s/deployment.yaml` pointe vers une référence (tag/SHA) inexistante ou inaccessible sur le registre distants (GHCR). Kubernetes applique un délai exponentiel (Back-off) avant chaque nouvelle tentative de téléchargement.

## 4. Correctif
Remplacer le tag d'image invalide dans `k8s/deployment.yaml` par une référence valide disponible sur le registre (ex: le SHA du dernier commit valide ou `latest`), puis re-déployer.