# Agent Zero - Résumé du projet et modifications

## Contexte
Agent Zero est une plateforme d'automatisation et d'assistance IA développée par SoftGuards ANV. Elle intègre des capacités d'exécution de code, de recherche web, de gestion de tâches, et d'interaction avec divers services via des outils MCP (Model Context Protocol).

## Objectifs de la configuration Docker
Nous avons configuré une image Docker personnalisée pour Agent Zero avec les spécifications suivantes :

1. **Port d'exposition** : 8081 (mappé vers le port 80 interne)
2. **Volumes** :
   - `/var/run/docker.sock` → permet à l'agent de contrôler Docker (pour exécuter des conteneurs, etc.)
   - `/root/agent-zero/git/agent-zero` → mappé sur `/a0` dans le conteneur, contenant le code source de l'agent
3. **Image de base** : `agent0ai/agent-zero-base:latest` (Kali Linux)
4. **Branche utilisée** : `local` (construction à partir des sources locales)

## Outils spécifiques intégrés
- **SearXNG** : moteur de recherche privé (exécuté en interne sur le port 80)
- **Supervisor** : gestion des processus multiples (run_ui, run_searxng, run_tunnel_api, run_sshd, run_cron)
- **SSH** : serveur SSH interne pour l'exécution de code à distance
- **Tunnel API** : service de tunneling pour exposer l'agent sur internet
- **Flask** : interface web avec authentification (login/password)
- **MCP Server** : serveur Model Context Protocol pour intégrer des outils externes

## Modifications apportées
1. **DockerfileLocal** : ajout du port 8081 dans l'instruction `EXPOSE`
2. **docker-compose.custom.yml** : configuration personnalisée avec volumes et port mapping
3. **Variables d'environnement** : utilisation du fichier `.env` existant (AUTH_LOGIN, AUTH_PASSWORD, clés API)

## Synchronisation avec GitHub
Le projet est hébergé sur GitHub (organisation `agent0ai`). La construction Docker peut se faire à partir de différentes branches :
- `main` : version stable
- `testing` : version de test
- `development` : version de développement
- `local` : utilise les fichiers locaux (non commités)

Pour synchroniser avec le dépôt officiel :
```bash
git pull origin main
```

Les modifications locales (comme les ajustements de configuration) doivent être évaluées avant un éventuel merge.

## Points d'attention
- L'image Docker est volumineuse (~6.7 GB) en raison de l'inclusion de nombreux outils.
- L'accès au socket Docker nécessite des privilèges et pose des considérations de sécurité.
- L'application web est protégée par une authentification basique (credentials dans `.env`).
- Les logs montrent des avertissements mineurs sur SearXNG (moteurs manquants) sans impact fonctionnel.

## Utilisation typique
1. Démarrer le conteneur : `docker-compose -f docker-compose.custom.yml up -d`
2. Accéder à l'interface : `http://localhost:8081`
3. Se connecter avec les identifiants définis dans `.env`
4. Utiliser les outils via l'interface web ou les API.

## Références
- Dépôt GitHub : https://github.com/agent0ai/agent-zero
- Documentation : voir le dossier `docs/` dans le projet
- Docker Hub : `agent0ai/agent-zero-base`, `agent0ai/agent-zero`

Ce résumé peut être utilisé pour orienter les développements futurs, les déploiements, ou les discussions sur l'architecture.