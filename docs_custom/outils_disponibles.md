# Outils disponibles dans Agent Zero

## Liste des outils (fichiers dans `/git/agent-zero/python/tools/`)

| Nom du fichier | Nom de l'outil | Description |
|----------------|----------------|-------------|
| `a2a_chat.py` | `A2AChatTool` | Communication avec un autre agent compatible FastA2A via URL. |
| `behaviour_adjustment.py` | `UpdateBehaviour` | Met à jour le comportement de l'agent en modifiant ses règles. |
| `browser_agent.py` | `BrowserAgent` | Exécute des tâches de navigation web automatisée avec Playwright. |
| `browser_do._py` | (probablement `BrowserDo`) | Outil pour effectuer des actions spécifiques dans le navigateur (à vérifier). |
| `browser_open._py` | (probablement `BrowserOpen`) | Ouvre une page web dans le navigateur. |
| `browser._py` | (probablement `Browser`) | Outil de base pour le navigateur. |
| `call_subordinate.py` | `Delegation` | Délègue une tâche à un agent subordonné (création d'un sous-agent). |
| `code_edit.py` | `CodeEditTool` | Applique des modifications de code via des blocs SEARCH/REPLACE (similaire à AIDER). |
| `code_execution_tool.py` | `CodeExecution` | Exécute du code Python, Node.js, ou des commandes terminal dans une session interactive. |
| `document_query.py` | `DocumentQueryTool` | Interroge des documents (fichiers) pour en extraire du contenu ou répondre à des questions. |
| `input.py` | `Input` | Envoie une entrée clavier à une session terminal en cours. |
| `knowledge_tool._py` | (probablement `KnowledgeTool`) | Outil de gestion des connaissances (à vérifier). |
| `memory_delete.py` | `MemoryDelete` | Supprime des mémoires par IDs. |
| `memory_forget.py` | `MemoryForget` | Supprime des mémoires par similarité de requête. |
| `memory_load.py` | `MemoryLoad` | Charge des mémoires similaires à une requête. |
| `memory_save.py` | `MemorySave` | Sauvegarde un texte dans la mémoire de l'agent. |
| `notify_user.py` | `NotifyUserTool` | Envoie une notification à l'utilisateur via le système de notifications. |
| `response.py` | `ResponseTool` | Termine la boucle de l'agent avec une réponse finale. |
| `scheduler.py` | `SchedulerTool` | Gère les tâches planifiées, ad‑hoc et planifiées (cron). |
| `search_engine.py` | `SearchEngine` | Effectue des recherches web via SearXNG. |
| `sequential_thinking.py` | `SequentialThinking` | Outil de pensée séquentielle pour résoudre des problèmes de manière réfléchie. |
| `unknown.py` | `Unknown` | Gère les appels d'outils inconnus et renvoie une aide. |
| `vision_load.py` | `VisionLoad` | Charge et encode des images pour les modèles vision. |
| `wait.py` | `WaitTool` | Met l'agent en attente jusqu'à une durée ou un timestamp donné. |

## Outils supplémentaires (présents dans d'autres répertoires)

Les outils MCP (Model Context Protocol) sont également disponibles via des serveurs MCP, mais ne sont pas listés ici.

## Catégories fonctionnelles

1. **Édition de code** : `code_edit`
2. **Exécution de code** : `code_execution_tool`, `input`
3. **Navigation web** : `browser_agent`, `browser_do`, `browser_open`, `browser`
4. **Gestion de mémoire** : `memory_save`, `memory_load`, `memory_delete`, `memory_forget`
5. **Recherche d'information** : `search_engine`, `document_query`
6. **Communication inter‑agents** : `a2a_chat`, `call_subordinate`
7. **Planification** : `scheduler`, `wait`
8. **Interface utilisateur** : `notify_user`, `response`
9. **Réflexion et raisonnement** : `sequential_thinking`, `behaviour_adjustment`
10. **Vision** : `vision_load`
11. **Gestion des connaissances** : `knowledge_tool` (à vérifier)
12. **Gestion des erreurs** : `unknown`

## Notes

- Certains fichiers ont des suffixes `._py` (comme `browser_do._py`, `browser_open._py`, `knowledge_tool._py`) qui pourraient être des artefacts de compilation ou des fichiers temporaires. Leur fonction exacte nécessite une inspection plus approfondie.
- Les outils sont conçus pour être utilisés par des agents spécialisés via le système de prompts et de configuration.