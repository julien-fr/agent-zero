# Agents d'entreprise autonome pour Agent Zero

## Vue d'ensemble

Cette documentation décrit l'ensemble des agents spécialisés créés pour simuler une entreprise autonome dans le cadre d'Agent Zero. Ces agents sont conçus pour couvrir l'ensemble du cycle de vie logiciel, du développement à la production, en passant par l'architecture, la sécurité, la qualité, le produit et la recherche.

## Liste des agents

### Agents spécialisés (10 prioritaires)

1. **Fullstack Developer** (`fullstack_developer`) – Développement full‑stack d'applications web
2. **Microservices Architect** (`microservices_architect`) – Conception d'architectures microservices
3. **Cloud Architect** (`cloud_architect`) – Infrastructure cloud et migration
4. **Data Engineer** (`data_engineer`) – Pipelines de données et entrepôts
5. **Security Auditor** (`security_auditor`) – Audit de sécurité et conformité
6. **Quality Assurance Engineer** (`quality_assurance_engineer`) – Assurance qualité et automatisation des tests
7. **Product Manager** (`product_manager`) – Stratégie produit et roadmap
8. **Research Analyst** (`research_analyst`) – Analyse de marché et recherche compétitive
9. **API Designer** (`api_designer`) – Conception d'API et documentation
10. **DevOps Engineer** (`devops_engineer`) – CI/CD, infrastructure as code, SRE

### Agent hybride de coordination

11. **Chief of Staff** (`chief_of_staff`) – Agent hybride manager/coordinateur combinant réflexion stratégique, brainstorming et orchestration d'experts.

### Agents de base (existants)

- **Developer** (`developer`) – Développement logiciel complexe
- **Researcher** (`researcher`) – Recherche approfondie et analyse
- **Hacker** (`hacker`) – Tests de pénétration et sécurité offensive
- **Agent0** (`agent0`) – Agent par défaut

## Structure des fichiers

Chaque agent suit la structure standard d'Agent Zero :

```
agents/
  {agent_name}/
    _context.md                    # Description courte du rôle
    prompts/
      agent.system.main.role.md    # Prompt principal détaillé
```

## Adaptations réalisées

### 1. Format des prompts

- **Structure uniforme** : Tous les prompts suivent le même schéma :
  - `## Your Role` : Présentation de l'agent
  - `### Core Identity` : Fonction principale, mission, architecture
  - `### Professional Capabilities` : Compétences détaillées par catégories
  - `### Operational Directives` : Règles de comportement
  - `### [Domaine] Methodology` : Processus de travail étape par étape
  - `### Tools Integration` : Comment utiliser les outils d'Agent Zero
  - `### Examples of [Agent] Tasks` : Exemples concrets de tâches avec détails d'exécution

- **Langage adapté** : Utilisation du ton professionnel et technique présent dans les prompts existants d'Agent Zero.

### 2. Intégration des outils d'Agent Zero

Chaque prompt inclut une section **Tools Integration** qui référence explicitement les outils disponibles :

- `CodeEditTool` : pour les modifications de code précises
- `CodeExecution` : pour exécuter du code, des scripts, des commandes
- `BrowserAgent` : pour l'automatisation web et les tests UI
- `DocumentQueryTool` : pour analyser des documents existants
- `MemorySave`/`MemoryLoad` : pour la persistance du contexte
- `SearchEngine` : pour la recherche d'information via SearXNG
- `Delegation` : pour déléguer à des agents subordonnés (surtout pour le Chief of Staff)

**Éviter les références à des outils inexistants** : Seuls les outils listés dans `outils_disponibles.md` ont été mentionnés.

### 3. Processus de travail adapté

Les méthodologies décrites tiennent compte des capacités réelles d'Agent Zero :
- **Exécution directe** : Les agents sont conçus comme des agents subordonnés qui exécutent directement les tâches (sauf le Chief of Staff qui délègue).
- **Collaboration inter‑agents** : La délégation via `Delegation` est encouragée pour les tâches nécessitant une expertise spécialisée.
- **Utilisation de la mémoire** : Les agents peuvent sauvegarder et charger des connaissances pour maintenir le contexte entre sessions.

### 4. Exemples de tâches réalistes

Chaque prompt inclut 5‑6 exemples de tâches typiques pour l'agent, avec pour certains un exemple détaillé incluant :
- **Instructions étape par étape**
- **Composants architecturaux**
- **Livrables attendus**
- **Intégration avec d'autres agents**

Ces exemples servent de guide pour l'utilisateur et de référence pour l'agent.

## Vérifications de cohérence

### Couverture des rôles

- Les 10 agents prioritaires couvrent l'ensemble du cycle de vie logiciel : développement, architecture, données, sécurité, qualité, produit, recherche, API, DevOps.
- Les rôles sont complémentaires et évitent les chevauchements excessifs.

### Uniformité terminologique

- Tous les prompts utilisent la même convention de dénomination : `Agent Zero '[Role Name]'`.
- Les sections principales sont identiques dans tous les fichiers.
- Les directives opérationnelles sont cohérentes avec les agents existants.

### Adéquation avec les outils

- Aucun outil externe non disponible n'est requis.
- Les outils mentionnés sont ceux effectivement présents dans `/git/agent-zero/python/tools/`.

### Structure de répertoires

- Tous les répertoires ont été créés avec succès.
- Les fichiers `_context.md` sont brefs et conformes au format existant.
- Les fichiers `agent.system.main.role.md` sont complets (entre 80 et 180 lignes).

## Agent Chief of Staff supplémentaire

Un agent **Chief of Staff** a été ajouté pour répondre au besoin d'un coordinateur hybride capable à la fois de réflexion stratégique et d'orchestration d'experts. Son rôle est d'orchestrer les autres agents experts en déléguant des tâches via l'outil `Delegation`, tout en fournissant un brainstorming créatif et une analyse critique. Il sert de point d'entrée unique pour les projets complexes nécessitant plusieurs expertises.

## Prochaines étapes

1. **Tests** : Vérifier que les agents fonctionnent correctement dans l'environnement Agent Zero.
2. **Intégration UI** : Ajouter les nouveaux agents à l'interface utilisateur si nécessaire.
3. **Affinements** : Recueillir les retours des utilisateurs pour ajuster les prompts.
4. **Documentation utilisateur** : Créer un guide dédié à l'utilisation de ces agents.

## Fichiers générés

La liste complète des fichiers créés se trouve dans `git/agent-zero/agents/`. Chaque agent possède son propre répertoire avec les deux fichiers requis.

---

*Documentation mise à jour le 2025‑12‑12 – Inclut l'agent Chief of Staff*