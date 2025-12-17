# Agent Zero - Mémoire de référence

*Document de référence rapide pour le projet Agent Zero - Dernière mise à jour : 11 décembre 2025*

---

## 1. Contexte du projet

**Agent Zero** est une plateforme d'automatisation et d'assistance IA développée par **SoftGuards ANV**. Elle intègre des capacités d'exécution de code, de recherche web, de gestion de tâches, et d'interaction avec divers services via des outils MCP (Model Context Protocol).

### Objectifs principaux
- Fournir un environnement unifié pour l'exécution d'agents IA
- Intégrer des outils externes via MCP
- Offrir une interface web avec authentification
- Permettre la recherche privée via SearXNG
- Faciliter le développement et le déploiement via Docker

### Écosystème
- **GitHub** : https://github.com/agent0ai/agent-zero
- **Docker Hub** : `agent0ai/agent-zero-base`, `agent0ai/agent-zero`
- **Documentation** : Dossier `docs/` dans le projet

---

## 2. Architecture technique

### Configuration Docker personnalisée
- **Image de base** : `agent0ai/agent-zero-base:latest` (Kali Linux)
- **Port exposé** : 8081 (mappé vers le port 80 interne)
- **Volumes montés** :
  - `/var/run/docker.sock` → permet à l'agent de contrôler Docker
  - `/root/agent-zero/git/agent-zero` → mappé sur `/a0` dans le conteneur (code source)
- **Branche utilisée** : `local` (construction à partir des sources locales)

### Services intégrés
| Service | Description | Port interne |
|---------|-------------|--------------|
| **SearXNG** | Moteur de recherche privé | 80 |
| **Supervisor** | Gestion des processus multiples | - |
| **SSH** | Serveur SSH pour exécution de code à distance | 22 |
| **Tunnel API** | Service de tunneling pour exposition internet | 5000 |
| **Flask** | Interface web avec authentification | 80 |
| **MCP Server** | Serveur Model Context Protocol | Variable |

### Modifications apportées
1. **DockerfileLocal** : Ajout du port 8081 dans l'instruction `EXPOSE`
2. **docker-compose.custom.yml** : Configuration personnalisée avec volumes et port mapping
3. **Variables d'environnement** : Utilisation du fichier `.env` (AUTH_LOGIN, AUTH_PASSWORD, clés API)

---

## 3. Documentation existante

### Fichiers clés dans `docs_custom/`

#### `agent-zero-project-summary.md`
- Résumé complet du projet et configuration Docker
- Objectifs de la configuration, outils intégrés, modifications apportées
- Synchronisation avec GitHub, points d'attention, utilisation typique

#### `guide_creation_outil.md`
- Guide détaillé pour créer de nouveaux outils pour Agent Zero
- Structure des fichiers (Python + prompt), conventions de nommage
- Exemple basé sur l'outil `sequential_thinking`
- Bonnes pratiques, gestion d'état, sécurité, tests

#### `volume-as-git-repo.md`
- Proposition innovante : faire du volume `/a0` un dépôt Git unique
- Avantages : synchronisation parfaite, backup automatique, rollback facile
- Architecture, mise en œuvre étape par étape, scripts d'initialisation
- Workflow quotidien, gestion des mises à jour upstream, risques et solutions

### Documentation officielle (dans `git/agent-zero/docs/`)
- `architecture.md` - Architecture du système
- `installation.md` - Guide d'installation
- `usage.md` - Guide d'utilisation
- `mcp_setup.md` - Configuration MCP
- `troubleshooting.md` - Dépannage

---

## 4. Idées innovantes

### Volume Docker comme dépôt Git unique
**Concept** : Fusionner le dépôt Git et le volume Docker en une seule entité.

**Avantages** :
1. **Synchronisation parfaite** : `git add . && git commit && git push` synchronise code + données + configuration
2. **Backup automatique** : Chaque commit sauvegarde l'état complet du système
3. **Restauration complète** : `git checkout` restaure l'état exact (code, données, configuration)
4. **Élégance et praticité** : Une seule source de vérité, simplification des workflows

**Structure proposée** :
```
/a0 (volume Docker mappé) = Dépôt Git
├── .git/                    # Historique Git
├── git/                     # Code source d'Agent Zero (sous-module ou clone)
├── usr/                     # Données utilisateur (mémoire, projets)
├── agents/                  # Agents personnalisés
└── docker-compose.yml       # Configuration
```

**Scripts disponibles** :
- `setup-volume-as-git.sh` : Transforme un volume Docker en dépôt Git complet
- `update-agent-zero.sh` : Gère les mises à jour upstream avec backup automatique
- Cron de backup automatique toutes les heures

---

## 5. Intégration d'AIDER

### Contexte
L'outil **AIDER** (https://github.com/Aider-AI/aider) est un assistant de codage qui utilise des blocs SEARCH/REPLACE pour éditer du code de manière précise. Ses fonctionnalités ont été adaptées pour Agent Zero afin de permettre des modifications chirurgicales dans les fichiers sans réécriture complète.

### Fonctionnalités intégrées
- **Édition par SEARCH/REPLACE** : L'outil `code_edit` applique des modifications en cherchant un bloc de code exact (SEARCH) et en le remplaçant par un nouveau bloc (REPLACE).
- **Matching flexible** : Tolère les différences d'indentation et d'espaces blancs, gère les lignes `...` pour omettre des sections.
- **Multi‑fichiers** : Possibilité d'appliquer plusieurs éditions en une seule invocation.
- **Création de fichiers** : Si SEARCH est vide, le REPLACE est ajouté à un nouveau fichier ou à la fin d'un fichier existant.

### Fichiers créés
- `git/agent-zero/python/tools/code_edit_tool.py` : Classe `CodeEditTool` héritant de `Tool`, implémente la logique d'édition.
- `git/agent-zero/prompts/agent.system.tool.code_edit.md` : Prompt détaillé expliquant quand et comment utiliser l'outil.

### Logique reprise d'AIDER
Les fonctions de matching (`replace_most_similar_chunk`, `perfect_or_whitespace`, `try_dotdotdots`, etc.) sont directement inspirées du code source d'AIDER (fichiers `editblock_coder.py`, `search_replace.py`). Elles ont été adaptées pour fonctionner dans l'écosystème Agent Zero.

### Utilisation
L'agent peut maintenant demander des modifications de code en fournissant des blocs SEARCH/REPLACE, ce qui permet des éditions incrémentielles et sûres. Exemple d'appel :
```json
{
    "tool_name": "code_edit",
    "tool_args": {
        "file_path": "src/utils.py",
        "search": "import os\n",
        "replace": "import os\nimport sys\n"
    }
}
```

### Tests
Les fonctions de base ont été testées avec succès (voir `test_edit_functions.py`). L'outil est prêt à être utilisé par l'agent.

## 6. État actuel du workspace

### Répertoire de travail
- **Workspace** : `/root/agent-zero`
- **Code source** : `/root/agent-zero/git/agent-zero`
- **Documentation personnalisée** : `/root/agent-zero/docs_custom/`

### Fichiers de configuration
- `docker-compose.custom.yml` : Configuration Docker Compose personnalisée
- `scripts/git-sync.sh` : Script de synchronisation Git
- `scripts/init-agent-zero.sh` : Script d'initialisation

### Structure du projet Agent Zero
```
git/agent-zero/
├── docker/                  # Configurations Docker (base, run)
├── python/                  # Code Python principal
├── prompts/                 # Prompts système et outils
├── agents/                  # Définitions d'agents (default, developer, hacker, researcher)
├── instruments/             # Instruments personnalisés
├── docs/                    # Documentation officielle
└── ...
```

### Services en cours d'exécution
- **Docker** : Conteneur Agent Zero avec port 8081 exposé
- **SearXNG** : Accessible via l'interface web
- **Supervisor** : Gère les processus (UI, SearXNG, Tunnel API, SSH, cron)

---

## 7. Références croisées

| Section | Fichiers source | Notes |
|---------|----------------|-------|
| Contexte | `agent-zero-project-summary.md` (lignes 1-60) | |
| Architecture Docker | `docker-compose.custom.yml`, `git/agent-zero/docker/run/Dockerfile` | |
| Création d'outils | `guide_creation_outil.md` (lignes 1-403) | Exemple : `sequential_thinking` |
| Volume Git | `volume-as-git-repo.md` (lignes 1-313) | Proposition architecturale |
| Intégration AIDER | `git/agent-zero/python/tools/code_edit_tool.py`, `git/agent-zero/prompts/agent.system.tool.code_edit.md` | Outil `code_edit` |
| Documentation officielle | `git/agent-zero/docs/*.md` | À consulter pour les détails techniques |

---

## 7. Points d'attention

### Sécurité
- Accès au socket Docker nécessite des privilèges (considérations de sécurité)
- Authentification web via credentials dans `.env`
- Validation des entrées dans les outils personnalisés

### Performance
- Image Docker volumineuse (~6.7 GB) due aux nombreux outils inclus
- Logs SearXNG avec avertissements mineurs (moteurs manquants) sans impact fonctionnel

### Maintenance
- Synchronisation régulière avec le dépôt upstream (`agent0ai/agent-zero`)
- Gestion des conflits lors des merges
- Backup automatique recommandé (via volume Git ou scripts)

---

## 8. Commandes utiles

### Démarrage/arrêt
```bash
# Démarrer le conteneur
docker-compose -f docker-compose.custom.yml up -d

# Arrêter le conteneur
docker-compose -f docker-compose.custom.yml down

# Voir les logs
docker-compose -f docker-compose.custom.yml logs -f
```

### Accès
```bash
# Interface web
http://localhost:8081

# Identifiants (définis dans .env)
AUTH_LOGIN=admin
AUTH_PASSWORD=*****
```

### Synchronisation Git
```bash
# Mettre à jour depuis upstream
cd /root/agent-zero/git/agent-zero
git pull origin main

# Synchroniser les modifications locales
cd /root/agent-zero
./scripts/git-sync.sh
```

---

## 9. Évolution future

### Améliorations envisagées
1. **Implémentation du volume Git** : Tester la proposition `volume-as-git-repo.md`
2. **Automatisation des backups** : Scripts cron + notifications
3. **Extension des outils MCP** : Intégration de nouveaux services
4. **Optimisation de l'image Docker** : Réduction de la taille, couches caching

### Suivi des versions
- **Branche principale** : `main` (stable)
- **Branches de développement** : `testing`, `development`, `local`
- **Tags** : Suivre les releases officielles sur GitHub

---

*Ce document est une synthèse des informations clés du projet Agent Zero. Pour les détails complets, consulter les fichiers source référencés.*