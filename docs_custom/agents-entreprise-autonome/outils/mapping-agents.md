# Mapping outils-agents pour les agents spécialisés

## Sélection des agents

### Agents spécialisés (10 prioritaires)
1. Fullstack Developer
2. Microservices Architect
3. Cloud Architect
4. Data Engineer
5. Security Auditor
6. Quality Assurance Engineer
7. Product Manager
8. Research Analyst
9. API Designer
10. DevOps Engineer

### Agent hybride de coordination
11. Chief of Staff

## Outils existants et leur pertinence par agent

### 1. Fullstack Developer
- **CodeEditTool** : essentiel pour éditer du code frontend/backend.
- **CodeExecution** : exécuter des scripts, tests, serveurs.
- **BrowserAgent** : tester l'interface utilisateur, interagir avec le frontend.
- **DocumentQueryTool** : lire la documentation technique.
- **SearchEngine** : rechercher des solutions, bibliothèques.
- **MemorySave/Load** : retenir des patterns, snippets.
- **CallSubordinate** : déléguer des sous‑tâches (ex. frontend/backend séparés).
- **A2AChatTool** : collaborer avec d'autres agents spécialisés.
- **SchedulerTool** : planifier des builds, des déploiements.
- **WaitTool** : attendre des processus (compilation, déploiement).

### 2. Microservices Architect
- **CodeEditTool** : modifier des configurations, définitions d'API.
- **DocumentQueryTool** : analyser des documents d'architecture.
- **SearchEngine** : rechercher des bonnes pratiques, outils.
- **MemorySave/Load** : stocker des décisions d'architecture.
- **CallSubordinate** : déléguer la conception de services individuels.
- **A2AChatTool** : discuter avec des agents de développement.
- **SchedulerTool** : planifier des revues d'architecture.
- **SequentialThinking** : raisonner sur des choix complexes.

### 3. Cloud Architect
- **CodeEditTool** : éditer des templates IaC (Terraform, CloudFormation).
- **CodeExecution** : exécuter des commandes CLI cloud (aws, gcloud).
- **DocumentQueryTool** : consulter la documentation cloud.
- **SearchEngine** : rechercher des services, limitations.
- **MemorySave/Load** : mémoriser des configurations, coûts.
- **CallSubordinate** : déléguer des tâches de déploiement.
- **SchedulerTool** : planifier des backups, des scaling.
- **WaitTool** : attendre des opérations cloud (provisioning).

### 4. Data Engineer
- **CodeEditTool** : écrire/modifier des scripts ETL, pipelines.
- **CodeExecution** : exécuter des jobs Spark, SQL, Python.
- **DocumentQueryTool** : interroger des schémas de base de données.
- **SearchEngine** : rechercher des optimisations, outils.
- **MemorySave/Load** : stocker des métadonnées, des requêtes.
- **CallSubordinate** : déléguer des tâches de nettoyage.
- **SchedulerTool** : planifier des pipelines de données.
- **WaitTool** : attendre des jobs longs.

### 5. Security Auditor
- **CodeEditTool** : examiner du code pour vulnérabilités.
- **CodeExecution** : exécuter des scans, outils de sécurité.
- **BrowserAgent** : tester des vulnérabilités web.
- **DocumentQueryTool** : analyser des rapports, politiques.
- **SearchEngine** : rechercher des CVE, advisories.
- **MemorySave/Load** : enregistrer des findings, patterns.
- **CallSubordinate** : déléguer des scans spécifiques.
- **SequentialThinking** : raisonner sur des attaques potentielles.

### 6. Quality Assurance Engineer
- **CodeEditTool** : modifier des tests, scripts d'automatisation.
- **CodeExecution** : exécuter des suites de tests.
- **BrowserAgent** : automatiser des tests end‑to‑end.
- **DocumentQueryTool** : lire des spécifications, plans de test.
- **SearchEngine** : rechercher des bugs connus, workarounds.
- **MemorySave/Load** : stocker des résultats de tests, bugs.
- **CallSubordinate** : déléguer des tests à d'autres agents.
- **SchedulerTool** : planifier des runs de tests réguliers.
- **WaitTool** : attendre des tests longs.

### 7. Product Manager
- **DocumentQueryTool** : analyser des user stories, feedback.
- **SearchEngine** : rechercher des tendances marché, concurrents.
- **MemorySave/Load** : mémoriser des décisions produit, roadmap.
- **CallSubordinate** : déléguer des analyses techniques.
- **A2AChatTool** : discuter avec des équipes techniques.
- **SchedulerTool** : planifier des revues, des livraisons.
- **SequentialThinking** : prioriser des fonctionnalités.
- **NotifyUserTool** : notifier des stakeholders.

### 8. Research Analyst
- **DocumentQueryTool** : extraire des informations de documents.
- **SearchEngine** : rechercher des articles, données.
- **BrowserAgent** : collecter des données web.
- **MemorySave/Load** : stocker des insights, références.
- **CallSubordinate** : déléguer des analyses spécifiques.
- **SequentialThinking** : synthétiser des informations complexes.
- **VisionLoad** : analyser des images, graphiques.

### 9. API Designer
- **CodeEditTool** : éditer des spécifications OpenAPI, code.
- **DocumentQueryTool** : lire des docs API existantes.
- **SearchEngine** : rechercher des standards, bonnes pratiques.
- **MemorySave/Load** : mémoriser des designs, patterns.
- **CallSubordinate** : déléguer l'implémentation.
- **A2AChatTool** : collaborer avec des développeurs.
- **SchedulerTool** : planifier des revues d'API.

### 10. DevOps Engineer
- **CodeEditTool** : éditer des scripts CI/CD, configurations.
- **CodeExecution** : exécuter des commandes d'infrastructure.
- **DocumentQueryTool** : consulter des logs, documentation.
- **SearchEngine** : rechercher des solutions d'incident.
- **MemorySave/Load** : stocker des procédures, commandes.
- **CallSubordinate** : déléguer des tâches de monitoring.
- **SchedulerTool** : planifier des maintenances, backups.
- **WaitTool** : attendre des déploiements, restaurations.
- **NotifyUserTool** : alerter en cas d'incident.

### 11. Chief of Staff
- **Delegation** : outil principal pour déléguer des tâches aux agents experts.
- **CodeEditTool** : ajustements mineurs sur les livrables intégrés.
- **CodeExecution** : exécuter des tests d'intégration, scripts de coordination.
- **BrowserAgent** : collecter des informations externes, tester des applications.
- **DocumentQueryTool** : analyser des briefs projets, documentation existante.
- **MemorySave/Load** : conserver le contexte du projet, performances des agents.
- **SearchEngine** : rechercher des bonnes pratiques, vérifier des hypothèses.
- **NotifyUser** : envoyer des mises à jour de progression, demander des clarifications.
- **SequentialThinking** : structurer des raisonnements complexes avant de répondre.
- **A2AChatTool** : communiquer avec d'autres agents de coordination.

## Outils peu pertinents ou neutres
- **Unknown** : générique, utile pour tous mais pas spécifique.
- **ResponseTool** : générique (fin de conversation).
- **Input** : générique (interaction terminal).
- **BehaviourAdjustment** : utile pour tous si besoin d'ajuster le comportement.
- **VisionLoad** : pertinent seulement si l'agent traite des images.

## Synthèse par catégorie d'outil

| Catégorie d'outil | Agents les plus concernés |
|-------------------|---------------------------|
| Édition de code | Fullstack, Microservices, Cloud, Data, Security, QA, API, DevOps |
| Exécution de code | Fullstack, Cloud, Data, Security, QA, DevOps |
| Navigation web | Fullstack, Security, QA, Research |
| Gestion de mémoire | Tous (pour la persistance des connaissances) |
| Recherche d'info | Tous (à des degrés divers) |
| Communication inter‑agents | Fullstack, Microservices, Product, API, Research, Chief of Staff |
| Planification | Cloud, Data, QA, Product, DevOps, Chief of Staff |
| Interface utilisateur | Product, DevOps, Chief of Staff (notifications) |
| Réflexion | Microservices, Security, Product, Research, Chief of Staff |
| Vision | Research (analyse d'images) |

## Notes

Ce mapping est basé sur les capacités déclarées de chaque agent et les outils disponibles dans Agent Zero. Il peut évoluer avec l'ajout de nouveaux outils ou la modification des prompts.

---

*Dernière mise à jour : 2025‑12‑12 – Inclut le Chief of Staff*