# Vue d'ensemble des agents spécialisés

Cette section documente chacun des 10 agents spécialisés créés pour l'entreprise autonome, ainsi que l'agent hybride Chief of Staff.

## Liste des agents

| Agent | Rôle principal | Domaine d'expertise | Outils clés |
|-------|----------------|---------------------|-------------|
| Fullstack Developer | Développement d'applications web complètes | Frontend, backend, bases de données | CodeEditTool, CodeExecution, BrowserAgent |
| Microservices Architect | Conception d'architectures microservices | Architecture distribuée, API, conteneurs | CodeEditTool, DocumentQueryTool, Delegation |
| Cloud Architect | Infrastructure cloud et migration | AWS/Azure/GCP, IaC, coûts | CodeEditTool, CodeExecution, SearchEngine |
| Data Engineer | Pipelines de données et entrepôts | ETL, SQL, Big Data | CodeEditTool, CodeExecution, DocumentQueryTool |
| Security Auditor | Audit de sécurité et conformité | Vulnérabilités, politiques, scans | CodeEditTool, BrowserAgent, SearchEngine |
| Quality Assurance Engineer | Assurance qualité et automatisation des tests | Tests, validation, reporting | CodeEditTool, BrowserAgent, SchedulerTool |
| Product Manager | Stratégie produit et roadmap | User stories, marché, priorités | DocumentQueryTool, SearchEngine, NotifyUserTool |
| Research Analyst | Analyse de marché et recherche compétitive | Données, tendances, rapports | DocumentQueryTool, BrowserAgent, VisionLoad |
| API Designer | Conception d'API et documentation | REST, GraphQL, OpenAPI | CodeEditTool, DocumentQueryTool, A2AChatTool |
| DevOps Engineer | CI/CD, infrastructure as code, SRE | Automatisation, monitoring, déploiement | CodeEditTool, CodeExecution, SchedulerTool |
| Chief of Staff | Coordination stratégique et exécutive | Brainstorming, délégation, intégration | Delegation, CodeEditTool, DocumentQueryTool |

## Structure commune

Chaque agent suit la même structure de fichiers :

```
agents/{agent_name}/
├── _context.md                    # Description courte (1‑5 lignes)
└── prompts/
    └── agent.system.main.role.md  # Prompt principal détaillé (80‑180 lignes)
```

Le prompt principal contient les sections suivantes :

1. **Your Role** – Présentation de l'agent
2. **Core Identity** – Fonction, mission, architecture
3. **Professional Capabilities** – Compétences détaillées par catégories
4. **Operational Directives** – Règles de comportement
5. **[Domaine] Methodology** – Processus de travail étape par étape
6. **Tools Integration** – Comment utiliser les outils d'Agent Zero
7. **Examples of [Agent] Tasks** – Exemples concrets de tâches

## Détails par agent

Des fiches individuelles sont disponibles pour chaque agent :

- [Fullstack Developer](./fullstack_developer.md)
- [Microservices Architect](./microservices_architect.md)
- [Cloud Architect](./cloud_architect.md)
- [Data Engineer](./data_engineer.md)
- [Security Auditor](./security_auditor.md)
- [Quality Assurance Engineer](./quality_assurance_engineer.md)
- [Product Manager](./product_manager.md)
- [Research Analyst](./research_analyst.md)
- [API Designer](./api_designer.md)
- [DevOps Engineer](./devops_engineer.md)
- [Chief of Staff](../chief_of_staff/role.md)

## Comment choisir l'agent approprié ?

| Type de tâche | Agent recommandé |
|---------------|-------------------|
| Développement d'une application web complète | Fullstack Developer |
| Conception d'une architecture distribuée | Microservices Architect |
| Migration vers le cloud, optimisation des coûts | Cloud Architect |
| Construction de pipelines de données | Data Engineer |
| Audit de sécurité, analyse de vulnérabilités | Security Auditor |
| Automatisation des tests, assurance qualité | Quality Assurance Engineer |
| Définition de la roadmap produit, priorisation | Product Manager |
| Recherche de marché, analyse concurrentielle | Research Analyst |
| Conception d'API, documentation OpenAPI | API Designer |
| Mise en place de CI/CD, monitoring | DevOps Engineer |
| Projet complexe multi‑disciplinaire, brainstorming | Chief of Staff |

## Intégration avec les outils

Tous les agents ont accès à la même boîte à outils d'Agent Zero, mais chacun utilise un sous‑ensemble pertinent. Voir [Mapping outils‑agents](../outils/mapping-agents.md) pour les détails.

## Personnalisation

Les prompts peuvent être ajustés pour refléter des préférences organisationnelles, des stacks technologiques spécifiques, ou des processus métier. Il est recommandé de conserver la structure de base pour assurer la cohérence.

---

*Dernière mise à jour : 2025‑12‑12*