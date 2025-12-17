# Guide de création d'un nouvel outil pour Agent Zero

*Ce guide est situé dans `agent-zero/git/agent-zero/guide_creation_outil.md` et sert de documentation interne pour les développeurs.*

Ce guide explique comment créer un nouvel outil (tool) pour Agent Zero, en suivant les conventions du projet et en s'appuyant sur l'exemple de l'outil `sequential_thinking`.

## 1. Structure générale

### Nommage de l'outil
- Le nom de l'outil doit être en **snake_case** (ex: `sequential_thinking`, `search_engine`, `memory`).
- Il doit être descriptif et refléter l'action principale.
- Évitez les noms trop génériques comme `tool` ou `action`.

### Emplacement des fichiers
Un outil se compose de deux fichiers principaux :

1. **Fichier Python** : `python/tools/<nom_outil>.py`
   - Contient la classe de l'outil qui hérite de `Tool`.
   - Implémente la logique d'exécution.

2. **Fichier de prompt** : `prompts/agent.system.tool.<nom_outil>.md`
   - Décrit l'outil pour l'agent : quand l'utiliser, paramètres, exemples.
   - Format markdown avec une structure spécifique.

### Exemple de structure
```
agent-zero/
├── python/tools/
│   └── sequential_thinking.py
└── prompts/
    └── agent.system.tool.sequential_thinking.md
```

## 2. Classe Python

### Héritage de `Tool`
Tout outil doit hériter de la classe abstraite `Tool` (définie dans `python/helpers/tool.py`).

```python
from python.helpers.tool import Tool, Response

class MonOutil(Tool):
    STATE_KEY = "_mon_outil_state"  # optionnel, pour gérer un état persistant

    async def execute(self, **kwargs) -> Response:
        # Logique de l'outil
        pass
```

### Méthode `execute`
C'est le cœur de l'outil. Elle est appelée lorsque l'agent utilise l'outil.

- **Paramètres** : Les arguments passés par l'agent sont disponibles dans `self.args` (dict).
- **Retour** : Doit retourner un objet `Response` avec :
  - `message` : chaîne de caractères à afficher à l'utilisateur (peut être du JSON formaté).
  - `break_loop` : booléen indiquant si l'outil doit interrompre la boucle de l'agent (généralement `False`).
  - `additional` : dictionnaire optionnel avec des données supplémentaires pour l'historique.

Exemple minimal :

```python
async def execute(self, **kwargs) -> Response:
    # Récupérer les arguments
    arg1 = self.args.get("arg1", "default")
    # Traitement
    result = f"Résultat avec {arg1}"
    # Retourner une réponse
    return Response(
        message=result,
        break_loop=False,
        additional={"processed": True}
    )
```

### Méthodes de cycle de vie
- `before_execution(self, **kwargs)` : exécutée avant `execute`. Par défaut, elle logue l'utilisation de l'outil. Vous pouvez la surcharger pour ajouter des logs personnalisés.
- `after_execution(self, response: Response, **kwargs)` : exécutée après `execute`. Par défaut, elle enregistre le résultat dans l'historique. Surchargez-la pour des traitements post‑exécution.

### Gestion d'état
Si votre outil a besoin de conserver un état entre plusieurs appels (comme une liste de pensées), utilisez les données de l'agent :

```python
STATE_KEY = "_mon_outil_state"

def _get_state(self):
    state = self.agent.get_data(self.STATE_KEY)
    if not state:
        state = {"default": []}  # état initial
    return state

def _save_state(self, state):
    self.agent.set_data(self.STATE_KEY, state)
```

Accédez à l'état dans `execute` pour le lire et le mettre à jour.

### Logging
Utilisez `PrintStyle` pour des messages colorés dans la console :

```python
from python.helpers.print_style import PrintStyle

PrintStyle(font_color="#1B4F72", bold=True).print("Message important")
```

## 3. Fonctionnement de l'outil dans l'agent

### Chargement
Les outils sont chargés dynamiquement par l'agent au démarrage. Le nom de l'outil (snake_case) doit correspondre au nom du fichier Python (sans extension) et au nom utilisé dans les prompts.

### Exécution
L'agent décide d'utiliser un outil en fonction du contexte et du prompt. Il appelle `execute` avec les arguments extraits de sa réflexion.

### Interaction avec l'agent
- L'outil a accès à `self.agent` (instance de `Agent`), ce qui permet d'interagir avec l'environnement, l'historique, les données, etc.
- Utilisez `self.agent.hist_add_tool_result()` pour ajouter un résultat à l'historique (déjà fait dans `after_execution` par défaut).

## 4. Prompts associés

### Emplacement et nommage
Le fichier de prompt doit se trouver dans `prompts/` et s'appeler `agent.system.tool.<nom_outil>.md`.

### Structure du fichier .md
Le fichier doit suivre ce modèle :

```
### <nom_outil>:
Une brève description de l'outil.

**When to use this tool**:
- Situation 1
- Situation 2

**Key features**:
- Fonctionnalité 1
- Fonctionnalité 2

**Parameters explained**:
- `param1`: description
- `param2`: description

**You should**:
1. Instruction 1
2. Instruction 2

**Example usage**:
~~~json
{
    "thoughts": ["..."],
    "headline": "...",
    "tool_name": "<nom_outil>",
    "tool_args": {
        "param1": "value1",
        "param2": "value2"
    }
}
~~~

**Response format**:
Le tool retourne un JSON avec les champs...
```

**Important** : Le prompt est utilisé par l'agent pour comprendre quand et comment utiliser l'outil. Il doit être clair, concis et inclure des exemples pertinents.

### Mécanisme de chargement
L'agent charge automatiquement tous les fichiers `agent.system.tool.*.md` du répertoire `prompts/` au démarrage. Chaque fichier est associé à un outil Python du même nom.

- Le nom de l'outil est extrait du nom de fichier : `agent.system.tool.sequential_thinking.md` → `sequential_thinking`.
- L'agent recherche ensuite une classe Python dans `python/tools/sequential_thinking.py` dont le nom est `SequentialThinking` (CamelCase dérivé du snake_case).
- Si la classe existe et hérite de `Tool`, elle est enregistrée comme outil disponible.

Ainsi, la création des deux fichiers avec les noms corrects suffit à intégrer l'outil dans l'agent.

### Utilisation par l'agent
Le prompt est injecté dans le contexte système de l'agent, lui permettant de savoir quand et comment utiliser l'outil. L'agent utilise le contenu du fichier .md pour :

1. Décider si l'outil est pertinent pour la tâche en cours.
2. Extraire les paramètres attendus et les formater correctement.
3. Comprendre le format de réponse et interpréter le résultat.

### Exemple basé sur `sequential_thinking`
Consultez `prompts/agent.system.tool.sequential_thinking.md` pour un exemple complet.

## 5. Exemple concret : création pas à pas

Prenons l'exemple de l'outil `sequential_thinking` que nous venons d'analyser.

### Étape 1 – Créer le fichier Python
`python/tools/sequential_thinking.py` contient :

- Une classe `ThoughtData` pour structurer les données.
- Une classe `SequentialThinking` qui hérite de `Tool`.
- Implémentation de `execute` qui valide les arguments, met à jour l'état, logue et retourne une réponse.
- Surcharge de `before_execution` et `after_execution` pour un logging personnalisé.

Voici un extrait commenté de la méthode `execute` :

```python
async def execute(self, **kwargs) -> Response:
    # Extraction des arguments
    thought = self.args.get("thought", "")
    next_thought_needed = self.args.get("nextThoughtNeeded", True)
    thought_number = self.args.get("thoughtNumber", 1)
    total_thoughts = self.args.get("totalThoughts", 1)

    # Validation
    if not thought:
        return Response(
            message="Error: 'thought' is required.",
            break_loop=False,
            additional={"error": True}
        )

    # Ajustement du total si nécessaire
    if thought_number > total_thoughts:
        total_thoughts = thought_number

    # Création de l'objet ThoughtData
    thought_data = ThoughtData(
        thought=thought,
        thought_number=thought_number,
        total_thoughts=total_thoughts,
        next_thought_needed=next_thought_needed,
        is_revision=self.args.get("isRevision"),
        revises_thought=self.args.get("revisesThought"),
        branch_from_thought=self.args.get("branchFromThought"),
        branch_id=self.args.get("branchId"),
        needs_more_thoughts=self.args.get("needsMoreThoughts"),
    )

    # Mise à jour de l'état
    state = self._get_state()
    state["thought_history"].append(thought_data.to_dict())

    # Gestion des branches
    if branch_from_thought and branch_id:
        if branch_id not in state["branches"]:
            state["branches"][branch_id] = []
        state["branches"][branch_id].append(thought_data.to_dict())

    self._save_state(state)

    # Logging formaté
    self._log_thought(thought_data)

    # Préparation de la réponse
    response_data = {
        "thoughtNumber": thought_number,
        "totalThoughts": total_thoughts,
        "nextThoughtNeeded": next_thought_needed,
        "branches": list(state["branches"].keys()),
        "thoughtHistoryLength": len(state["thought_history"]),
    }

    return Response(
        message=json.dumps(response_data, indent=2),
        break_loop=False,
        additional=response_data
    )
```

### Étape 2 – Créer le fichier de prompt
`prompts/agent.system.tool.sequential_thinking.md` décrit :

- Quand utiliser l'outil (problèmes complexes, besoin de révisions, etc.).
- Les paramètres (`thought`, `nextThoughtNeeded`, etc.).
- Des instructions détaillées pour l'agent.
- Un exemple d'utilisation en JSON.

Extrait du prompt :

```
### sequential_thinking:
A detailed tool for dynamic and reflective problem-solving through thoughts.
This tool helps analyze problems through a flexible thinking process that can adapt and evolve.
Each thought can build on, question, or revise previous insights as understanding deepens.

**When to use this tool**:
- Breaking down complex problems into steps
- Planning and design with room for revision
- Analysis that might need course correction
...
```

### Étape 3 – Tester l'outil
Vous pouvez tester l'outil en lançant Agent Zero et en lui demandant d'utiliser le nouvel outil, ou en écrivant un script de test (comme `test_sequential.py`).

Voici un exemple de test simple :

```python
# test_sequential.py
import asyncio
from python.tools.sequential_thinking import SequentialThinking
from python.helpers.tool import Response

# Simuler un agent (mock)
class MockAgent:
    def __init__(self):
        self.data = {}
    def get_data(self, key):
        return self.data.get(key)
    def set_data(self, key, value):
        self.data[key] = value

async def test():
    agent = MockAgent()
    tool = SequentialThinking(
        agent=agent,
        name="sequential_thinking",
        method=None,
        args={
            "thought": "Première pensée de test",
            "nextThoughtNeeded": True,
            "thoughtNumber": 1,
            "totalThoughts": 3,
        },
        message="",
        loop_data=None,
    )
    response = await tool.execute()
    print("Réponse:", response.message)

if __name__ == "__main__":
    asyncio.run(test())
```

## 6. Bonnes pratiques

### Conventions de nommage
- **Python** : classes en `CamelCase`, variables et fonctions en `snake_case`.
- **Fichiers** : `snake_case.py` pour les outils.
- **Clés d'état** : préfixez avec un underscore (`_mon_outil_state`) pour éviter les collisions.

### Gestion d'état
- Gardez l'état minimal et sérialisable (dict, list, str, int, bool).
- Pensez à réinitialiser l'état quand nécessaire (par exemple à la fin d'une tâche).

### Logging
- Utilisez `PrintStyle` pour une sortie colorée et lisible.
- Loguez les étapes importantes (début, fin, erreurs) mais évitez le bruit excessif.

### Gestion des erreurs
- Validez les arguments dans `execute` et retournez une réponse d'erreur avec `break_loop=False` pour ne pas interrompre l'agent.
- Utilisez des exceptions uniquement pour les erreurs critiques (elles remonteront à l'agent).

### Documentation
- Commentez le code, surtout la logique complexe.
- Maintenez le prompt à jour si les paramètres changent.

### Tests
- Écrivez un script de test pour vérifier le comportement de l'outil en isolation.
- Vérifiez l'intégration avec l'agent en simulant une conversation.
- Utilisez des mocks pour `self.agent` et `self.args` afin de tester différents scénarios.

### Gestion des dépendances
- Si votre outil nécessite des bibliothèques externes, ajoutez-les à `requirements.txt` ou `requirements.dev.txt` selon le cas.
- Évitez d'importer des modules lourds au niveau du module ; préférez les importer à l'intérieur de `execute` si la dépendance est optionnelle.
- Documentez toute dépendance supplémentaire dans un commentaire en tête du fichier.

### Compatibilité asynchrone
- La méthode `execute` est asynchrone (`async def`). Utilisez `await` pour les opérations I/O.
- Si votre outil effectue des calculs intensifs CPU, envisagez d'utiliser `asyncio.to_thread` ou un exécuteur pour ne pas bloquer la boucle d'événements.
- Respectez les autres outils : ne monopolisez pas le thread principal.

### Sécurité
- Ne faites pas confiance aux arguments `self.args` ; validez et assainissez les entrées.
- Évitez d'exécuter du code arbitraire ou des commandes shell sans validation stricte.
- Si l'outil interagit avec le système de fichiers, utilisez des chemins relatifs et vérifiez les permissions.
- Ne stockez pas de données sensibles (mots de passe, clés) dans l'état de l'agent sans chiffrement.

### Performance
- Gardez `execute` rapide ; pour les opérations longues, utilisez `break_loop=False` et renvoyez un message de progression.
- Si l'outil est fréquemment utilisé, envisagez un cache en mémoire (dans l'état de l'agent) pour éviter des calculs redondants.

### Maintenance
- Suivez les évolutions de l'API `Tool` ; vérifiez la compatibilité après les mises à jour du projet.
- Utilisez des logs structurés pour faciliter le débogage.
- Ajoutez des commentaires sur les décisions de conception non triviales.

## 7. Résumé des étapes

1. **Choisir un nom** en snake_case.
2. **Créer le fichier Python** dans `python/tools/`.
   - Hériter de `Tool`.
   - Implémenter `execute`.
   - Ajouter la gestion d'état si nécessaire.
   - Surcharger `before_execution`/`after_execution` si besoin.
3. **Créer le fichier de prompt** dans `prompts/agent.system.tool.<nom>.md`.
   - Suivre la structure décrite.
   - Inclure des exemples concrets.
4. **Tester** l'outil avec un script ou via l'agent.
5. **Documenter** toute particularité dans ce guide ou dans les commentaires.

## 8. Ressources

- `python/helpers/tool.py` : définition de la classe de base `Tool`.
- `python/tools/sequential_thinking.py` : exemple complet d'outil.
- `prompts/agent.system.tool.sequential_thinking.md` : exemple de prompt.
- `test_sequential.py` : exemple de test.

---

*Ce guide a été créé le 11 décembre 2025. Pour toute question, consultez la documentation du projet ou contactez les mainteneurs.*