# Scénario : Orchestration d'un projet multi‑agents

## Contexte

Vous avez un projet concret et bien défini (ex. « Construire une API de recommandation de films ») et vous souhaitez le réaliser rapidement en exploitant l'expertise de plusieurs agents spécialisés. Vous engagez le **Chief of Staff** en mode exécutif pour décomposer le projet, déléguer les tâches aux agents appropriés, suivre la progression et intégrer les livrables.

## Objectifs

- Délivrer un produit fonctionnel et intégré dans les délais.
- Maximiser l'utilisation des compétences spécialisées.
- Maintenir une qualité élevée et une cohérence architecturale.
- Fournir une visibilité complète sur l'avancement.

## Participants

- **Utilisateur** : Client / Product Owner.
- **Chief of Staff** : Coordinateur exécutif.
- **Agents experts** : Fullstack Developer, API Designer, Data Engineer, Cloud Architect, Quality Assurance Engineer, etc. (selon les besoins).

## Étapes détaillées

### 1. Brief initial
**Utilisateur** : « Je veux une API de recommandation de films qui suggère des films similaires à un film donné. L'API doit être scalable, documentée avec OpenAPI, et déployée sur AWS. »

**Chief of Staff** :
- Confirme la compréhension et passe en mode exécutif.
- Identifie les composants clés :
  1. **Base de données** : Stockage des métadonnées de films et des similarités.
  2. **Algorithme de recommandation** : Logique de calcul des similarités.
  3. **API REST** : Endpoints pour requêter les recommandations.
  4. **Infrastructure** : Déploiement, monitoring, scaling.
  5. **Documentation** : OpenAPI, guide d'utilisation.
  6. **Tests** : Validation fonctionnelle et de performance.

### 2. Décomposition et planification
Le Chief of Staff crée un plan de travail détaillé :

| Tâche | Agent assigné | Livrable attendu | Dépendances |
|-------|---------------|------------------|-------------|
| 1. Conception de la base de données | Data Engineer | Schéma SQL/NoSQL, script de migration | – |
| 2. Collecte et préparation des données | Data Engineer | Jeu de données nettoyé (films, genres, notes) | Tâche 1 |
| 3. Implémentation de l'algorithme | Fullstack Developer | Script Python de calcul de similarité (cosine sur genres) | Tâche 2 |
| 4. Conception de l'API | API Designer | Spécification OpenAPI 3.0, endpoints définis | – |
| 5. Développement de l'API | Fullstack Developer | Code FastAPI/Express implémentant les endpoints | Tâches 3,4 |
| 6. Configuration de l'infrastructure AWS | Cloud Architect | Terraform/IaC, configuration VPC, EC2, RDS | Tâches 1,5 |
| 7. Déploiement initial | DevOps Engineer | Pipeline CI/CD, déploiement sur staging | Tâches 5,6 |
| 8. Tests automatisés | Quality Assurance Engineer | Suite de tests (unitaires, intégration, charge) | Tâche 5 |
| 9. Documentation utilisateur | API Designer | Documentation interactive (Swagger UI), README | Tâche 4 |
| 10. Revue de sécurité | Security Auditor | Rapport de vulnérabilités, recommandations | Tâche 5 |

### 3. Délégation séquentielle et parallèle
Le Chief of Staff utilise l'outil `Delegation` pour créer et instruire chaque agent :

**Exemple d'instruction pour Data Engineer** :
« En tant que Data Engineer, votre tâche est de concevoir une base de données pour une API de recommandation de films. Les exigences :
- Stocker au moins 10 000 films avec titre, année, genres, description.
- Permettre des requêtes rapides pour récupérer les films similaires par similarité de genres.
- Choisir entre PostgreSQL (relationnel) ou MongoDB (document) ; justifiez votre choix.
- Produire un schéma SQL/DDL ou une collection MongoDB, ainsi qu'un script de peuplement avec des données d'exemple.
Livrez le schéma et le script dans un fichier `database/` du projet. »

**Exemple d'instruction pour API Designer** :
« En tant qu'API Designer, concevez une API REST pour une recommandation de films. Spécifiez :
- Endpoint `GET /recommendations/{movie_id}` retournant une liste de films similaires.
- Endpoint `GET /movies` pour la recherche.
- Modèles de requête/réponse en JSON.
- Documentation OpenAPI 3.0 dans un fichier `openapi.yaml`.
Tenez‑vous aux meilleures pratiques de design d'API (versioning, pagination, codes HTTP). »

### 4. Suivi de progression
Le Chief of Staff surveille l'état des tâches via :
- **Notifications** : Chaque agent notifie la complétion via `NotifyUserTool`.
- **Vérification des livrables** : Le Chief of Staff utilise `DocumentQueryTool` pour examiner les fichiers produits.
- **Gestion des blocages** : Si un agent signale un problème, le Chief of Staff ajuste le plan ou délègue une tâche de résolution.

**Tableau de bord mental** :
| Tâche | Statut | Agent | Blocages |
|-------|--------|-------|----------|
| 1. Conception BD | ✅ terminé | Data Engineer | – |
| 2. Préparation données | 🔄 en cours | Data Engineer | Données manquantes |
| 3. Algorithme | ⏳ en attente | Fullstack Developer | Dépend de 2 |
| ... | ... | ... | ... |

### 5. Intégration et validation
Une fois toutes les tâches individuelles terminées, le Chief of Staff :
- Rassemble les livrables dans une structure de projet cohérente.
- Exécute des tests d'intégration via `CodeExecution` pour vérifier que l'API fonctionne avec la base de données.
- Détecte et résout les conflits (ex. différences de formats de données).
- Demande une revue finale à **Quality Assurance Engineer** et **Security Auditor**.

### 6. Livraison au client
Le Chief of Staff produit un livrable intégré comprenant :
- **Code source** : Dépôt Git avec tous les fichiers.
- **Documentation** : README, guide de déploiement, spécification OpenAPI.
- **Scripts d'infrastructure** : Terraform, Docker Compose.
- **Rapport de qualité** : Couverture de tests, résultats de sécurité, métriques de performance.
- **Instructions d'utilisation** : Exemples de requêtes curl, URL de staging.

**Présentation à l'utilisateur** :
« Votre API de recommandation de films est prête. Voici ce qui a été livré :
1. **API déployée** : https://api‑films‑staging.example.com
2. **Documentation interactive** : https://api‑films‑staging.example.com/docs
3. **Code source** : https://github.com/your‑org/film‑recommendation‑api
4. **Scripts de déploiement** : Dans le dossier `infra/`.
5. **Rapport de sécurité** : Aucune vulnérabilité critique détectée.
Vous pouvez immédiatement interroger l'API avec `curl https://api‑films‑staging.example.com/recommendations/123`. »

## Exemple de dialogue

**Utilisateur** : « J'ai besoin d'une API de recommandation de films pour mon site. »

**Chief of Staff** : « Compris. Je vais orchestrer sa construction. Voici le plan :
1. Data Engineer va créer la base de données et préparer les données.
2. API Designer va concevoir l'interface OpenAPI.
3. Fullstack Developer va implémenter l'API et l'algorithme.
4. Cloud Architect va configurer AWS.
5. Quality Assurance va tester le tout.
Cela prendra environ 5 jours. Je vous tiens informé après chaque étape. »

*(Quelques heures plus tard)*

**Chief of Staff** : « Mise à jour : Data Engineer a terminé le schéma de base de données. API Designer a produit la spécification OpenAPI. Fullstack Developer commence maintenant l'implémentation. Aucun blocage pour l'instant. »

## Points clés

- **Délégation précise** : Chaque instruction doit être claire, avec des livrables attendus explicites.
- **Gestion des dépendances** : Les tâches sont séquencées pour éviter les attentes inutiles.
- **Transparence** : L'utilisateur reçoit des mises à jour régulières.
- **Qualité intégrée** : Chaque agent applique ses standards de qualité ; le Chief of Staff assure la cohérence globale.

## Avantages de cette approche

- **Efficacité** : Parallélisation des tâches spécialisées réduit le temps total.
- **Qualité** : Chaque domaine est traité par un expert.
- **Scalabilité** : Le même modèle peut gérer des projets de toute taille.
- **Réutilisabilité** : Les livrables sont modulaires et peuvent être réutilisés dans d'autres projets.

## Variantes

- **Projet urgent** : Délégation massive en parallèle avec suivi rapproché.
- **Projet itératif** : Plusieurs cycles de délégation (sprints) avec feedback utilisateur entre chaque.
- **Projet de recherche** : Orchestration d'agents de recherche (Researcher, Data Engineer, Research Analyst) pour produire un rapport.

---

*Scénario rédigé le 2025‑12‑12*