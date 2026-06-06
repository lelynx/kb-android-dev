# Web Service Knowledge Base — API Reference

> Document de référence pour l'implémentation d'un client Kotlin/Android.

---

## Sommaire

1. [Configuration](#1-configuration)
2. [Modèles de données](#2-modèles-de-données)
3. [Endpoints — Thèmes](#3-endpoints--thèmes)
4. [Endpoints — Types](#4-endpoints--types)
5. [Endpoints — Tags](#5-endpoints--tags)
6. [Endpoints — Fiches de connaissance](#6-endpoints--fiches-de-connaissance)
7. [Codes HTTP de retour](#7-codes-http-de-retour)
8. [Comportement get_or_create](#8-comportement-get_or_create)
9. [Formatage du contenu](#9-formatage-du-contenu)

---

## 1. Configuration

| Paramètre    | Valeur                        |
|--------------|-------------------------------|
| Host         | `localhost` (ou `127.0.0.1`)  |
| Port         | `8002`                        |
| Base URL     | `http://localhost:8002`       |
| Content-Type | `application/json`            |
| Encoding     | UTF-8                         |

Tous les échanges (requêtes et réponses) utilisent le format **JSON**.  
Tous les endpoints sont préfixés par `/api/knowledge`.

---

## 2. Modèles de données

### 2.1 ThemeResponse

Retourné par `GET /themes` et `POST /themes`.

```json
{
  "id":           1,
  "name":         "Kotlin",
  "icon":         "🔧",
  "date_created": "2026-06-05T13:37:34"
}
```

| Champ          | Type   | Description                  |
|----------------|--------|------------------------------|
| `id`           | Int    | Identifiant unique           |
| `name`         | String | Nom du thème                 |
| `icon`         | String | Emoji représentant le thème  |
| `date_created` | String | Date ISO 8601 de création    |

---

### 2.2 TypeResponse

Retourné par `GET /types` et `POST /types`.

```json
{
  "id":           2,
  "name":         "Snippet",
  "icon":         "💻",
  "date_created": "2026-06-05T13:37:34"
}
```

| Champ          | Type   | Description                 |
|----------------|--------|-----------------------------|
| `id`           | Int    | Identifiant unique          |
| `name`         | String | Nom du type                 |
| `icon`         | String | Emoji représentant le type  |
| `date_created` | String | Date ISO 8601 de création   |

---

### 2.3 KnowledgeItemResponse

Retourné par `GET /`, `POST /`, `GET /{id}`, `PUT /{id}`.

```json
{
  "id":                2,
  "theme_id":          5,
  "type_id":           2,
  "titre":             "StateFlow vs SharedFlow",
  "description":       "Différences clés entre StateFlow et SharedFlow",
  "code":              "```kotlin\nval state = MutableStateFlow(0)\n```",
  "solution":          "Utiliser StateFlow pour un état UI, SharedFlow pour les événements.",
  "tags":              "kotlin, flow, coroutines",
  "date_creation":     "2026-06-05T14:00:00",
  "date_modification": "2026-06-05T14:05:00",
  "theme_name":        "Kotlin",
  "theme_icon":        "🔧",
  "type_name":         "Concept",
  "type_icon":         "📘"
}
```

| Champ               | Type        | Nullable | Description                              |
|---------------------|-------------|----------|------------------------------------------|
| `id`                | Int         | Non      | Identifiant unique                       |
| `theme_id`          | Int         | Oui      | FK vers la table themes                  |
| `type_id`           | Int         | Oui      | FK vers la table types                   |
| `titre`             | String      | Non      | Titre de la fiche                        |
| `description`       | String      | Oui      | Contexte / problème                      |
| `code`              | String      | Oui      | Code source (supporte Markdown + blocs)  |
| `solution`          | String      | Oui      | Explication ou solution                  |
| `tags`              | String      | Oui      | Tags séparés par des virgules            |
| `date_creation`     | String      | Non      | Date ISO 8601 de création                |
| `date_modification` | String      | Non      | Date ISO 8601 de dernière modification   |
| `theme_name`        | String      | Oui      | Nom du thème (jointure)                  |
| `theme_icon`        | String      | Oui      | Icône du thème (jointure)                |
| `type_name`         | String      | Oui      | Nom du type (jointure)                   |
| `type_icon`         | String      | Oui      | Icône du type (jointure)                 |

---

### 2.4 KnowledgeItemCreate (corps de la requête POST)

```json
{
  "titre":       "Titre de la fiche",
  "theme_name":  "Kotlin",
  "type_name":   "Snippet",
  "description": "Description optionnelle",
  "code":        "```kotlin\nfun hello() = println(\"Hello!\")\n```",
  "solution":    "Solution optionnelle",
  "tags":        "kotlin, android"
}
```

| Champ         | Type   | Obligatoire | Description                                      |
|---------------|--------|-------------|--------------------------------------------------|
| `titre`       | String | **Oui**     | Titre court et descriptif                        |
| `theme_name`  | String | **Oui**     | Nom du thème (créé automatiquement si inexistant)|
| `type_name`   | String | **Oui**     | Nom du type (créé automatiquement si inexistant) |
| `description` | String | Non         | Contexte ou description du problème              |
| `code`        | String | Non         | Code source (format Markdown recommandé)         |
| `solution`    | String | Non         | Solution ou explication détaillée                |
| `tags`        | String | Non         | Mots-clés séparés par des virgules               |

---

### 2.5 KnowledgeItemUpdate (corps de la requête PUT)

Identique à `KnowledgeItemCreate` mais **tous les champs sont optionnels**.  
Seuls les champs présents dans le corps JSON sont mis à jour.

```json
{
  "solution": "Nouvelle solution",
  "tags":     "kotlin, flow, mise-a-jour"
}
```

---

## 3. Endpoints — Thèmes

### `GET /api/knowledge/themes`

Retourne la liste de tous les thèmes.

**Réponse** `200 OK` :

```json
[
  { "id": 3,  "name": "Android",        "icon": "🤖", "date_created": "..." },
  { "id": 2,  "name": "FastAPI",        "icon": "⚡", "date_created": "..." },
  { "id": 4,  "name": "Jetpack Compose","icon": "🎨", "date_created": "..." },
  { "id": 5,  "name": "Kotlin",         "icon": "🔧", "date_created": "..." }
]
```

---

### `POST /api/knowledge/themes`

Crée un nouveau thème.

**Corps de la requête** :

```json
{
  "name": "Nouveau Thème",
  "icon": "🆕"
}
```

| Champ  | Type   | Obligatoire | Défaut |
|--------|--------|-------------|--------|
| `name` | String | **Oui**     | —      |
| `icon` | String | Non         | `"📌"` |

**Réponse** `201 Created` : objet `ThemeResponse`.

**Erreur** `400 Bad Request` si le thème existe déjà :

```json
{ "detail": "Ce thème existe déjà" }
```

---

## 4. Endpoints — Types

### `GET /api/knowledge/types`

Retourne la liste de tous les types.

**Réponse** `200 OK` :

```json
[
  { "id": 1, "name": "Concept",        "icon": "📘", "date_created": "..." },
  { "id": 2, "name": "Snippet",        "icon": "💻", "date_created": "..." },
  { "id": 3, "name": "Erreur résolue", "icon": "🐛", "date_created": "..." },
  { "id": 4, "name": "Astuce",         "icon": "💡", "date_created": "..." },
  { "id": 5, "name": "Question ouverte","icon": "❓", "date_created": "..." },
  { "id": 6, "name": "Objectif",       "icon": "🎯", "date_created": "..." },
  { "id": 7, "name": "Ressource",      "icon": "✳️", "date_created": "..." },
  { "id": 8, "name": "Piège",          "icon": "⚠️", "date_created": "..." },
  { "id": 9, "name": "Procédure",      "icon": "📋", "date_created": "..." }
]
```

---

### `POST /api/knowledge/types`

Crée un nouveau type.

**Corps de la requête** :

```json
{
  "name": "Nouveau Type",
  "icon": "🆕"
}
```

| Champ  | Type   | Obligatoire | Défaut |
|--------|--------|-------------|--------|
| `name` | String | **Oui**     | —      |
| `icon` | String | Non         | `"📄"` |

**Réponse** `201 Created` : objet `TypeResponse`.

**Erreur** `400 Bad Request` si le type existe déjà :

```json
{ "detail": "Ce type existe déjà" }
```

---

## 5. Endpoints — Tags

### `GET /api/knowledge/tags`

Retourne la liste triée de tous les tags distincts, extraits de l'ensemble des fiches.

**Réponse** `200 OK` :

```json
["android", "compose", "coroutines", "flow", "kotlin", "ktor"]
```

> Le serveur parse les champs `tags` stockés sous forme de chaînes CSV
> (ex. `"kotlin, flow, coroutines"`) et déduplique les valeurs.

---

## 6. Endpoints — Fiches de connaissance

### `GET /api/knowledge`

Retourne toutes les fiches, triées par date de modification décroissante (la plus récente en premier).

**Réponse** `200 OK` : tableau de `KnowledgeItemResponse`.

```json
[
  {
    "id": 5,
    "titre": "Ktor — Configurer le client HTTP",
    "theme_name": "Réseau & API",
    "type_name": "Snippet",
    ...
  }
]
```

---

### `POST /api/knowledge`

Crée une nouvelle fiche de connaissance.

**En-tête** :
```
Content-Type: application/json
```

**Corps de la requête** : objet `KnowledgeItemCreate`.

**Exemple complet** :

```json
{
  "titre":       "Kotlin — StateFlow vs SharedFlow",
  "theme_name":  "Kotlin",
  "type_name":   "Concept",
  "description": "Quand utiliser StateFlow ou SharedFlow dans une architecture MVVM ?",
  "code":        "```kotlin\n// StateFlow : état UI (valeur initiale requise)\nval uiState = MutableStateFlow(UiState.Loading)\n\n// SharedFlow : événements one-shot\nval events = MutableSharedFlow<UiEvent>()\n```",
  "solution":    "StateFlow pour l'état persistant, SharedFlow pour les événements consommés une seule fois.",
  "tags":        "kotlin, flow, coroutines, mvvm"
}
```

**Réponse** `201 Created` : objet `KnowledgeItemResponse` complet (avec `id`, `theme_id`, `type_id`, etc.).

**Validation** : si `titre`, `theme_name` ou `type_name` est absent → `422 Unprocessable Entity`.

---

### `GET /api/knowledge/{item_id}`

Retourne une fiche par son identifiant.

**Paramètre de chemin** :

| Paramètre | Type | Description         |
|-----------|------|---------------------|
| `item_id` | Int  | Identifiant de la fiche |

**Réponse** `200 OK` : objet `KnowledgeItemResponse`.

**Erreur** `404 Not Found` :

```json
{ "detail": "Fiche introuvable" }
```

---

### `PUT /api/knowledge/{item_id}`

Met à jour partiellement une fiche existante.  
Seuls les champs présents dans le corps sont modifiés ; les autres sont conservés.

**Corps de la requête** : objet `KnowledgeItemUpdate` (tous champs optionnels).

**Exemple** — mise à jour des tags et de la solution uniquement :

```json
{
  "tags":     "kotlin, flow, coroutines, android",
  "solution": "Préférer collectAsStateWithLifecycle() en Compose."
}
```

**Exemple** — changement de thème (le nouveau thème est créé s'il n'existe pas) :

```json
{
  "theme_name": "Jetpack Compose",
  "type_name":  "Astuce"
}
```

**Réponse** `200 OK` : objet `KnowledgeItemResponse` mis à jour.

**Erreur** `404 Not Found` si `item_id` est inconnu.

---

### `DELETE /api/knowledge/{item_id}`

Supprime une fiche.

**Réponse** `204 No Content` (corps vide).

**Erreur** `404 Not Found` si `item_id` est inconnu.

---

## 7. Codes HTTP de retour

| Code | Signification           | Endpoints concernés                          |
|------|-------------------------|----------------------------------------------|
| 200  | Succès (lecture/màj)    | GET, PUT                                     |
| 201  | Création réussie        | POST /themes, POST /types, POST /knowledge   |
| 204  | Suppression réussie     | DELETE /knowledge/{id}                       |
| 400  | Doublon (thème ou type) | POST /themes, POST /types                    |
| 404  | Ressource introuvable   | GET, PUT, DELETE /knowledge/{id}             |
| 422  | Corps JSON invalide     | Tous les POST/PUT (validation Pydantic)      |
| 500  | Erreur serveur          | —                                            |

---

## 8. Comportement get_or_create

Lors d'un `POST /api/knowledge` ou `PUT /api/knowledge/{id}`, le serveur résout
`theme_name` et `type_name` en IDs via la logique suivante :

```
1. Chercher le thème/type par name dans la base
2. S'il existe → utiliser son id
3. S'il n'existe pas → le créer avec l'icône par défaut, puis utiliser son id
```

Icônes par défaut créées automatiquement :

| Entité | Icône par défaut |
|--------|-----------------|
| Thème  | `📌`            |
| Type   | `📄`            |

**Conséquence côté client** : le client n'a jamais besoin de pré-créer un thème ou un
type avant d'enregistrer une fiche. Il suffit de passer les noms en clair.

---

## 9. Formatage du contenu

### Retours à la ligne

Les champs `description` et `solution` supportent le Markdown.  
Utiliser `\n` pour les sauts de ligne dans la chaîne JSON.

```json
"description": "Ligne 1\n\nLigne 2\n\n- Point A\n- Point B"
```

### Blocs de code

Le champ `code` supporte la syntaxe Markdown avec balise de langage.

**Format recommandé (avec langage explicite)** :

```json
"code": "```kotlin\nfun greet(name: String) = \"Hello, $name!\"\n```"
```

**Format hérité (sans balise — détection automatique)** :

```json
"code": "val x = listOf(1, 2, 3)"
```

Langages reconnus par Highlight.js : `kotlin`, `java`, `python`, `javascript`,
`typescript`, `xml`, `json`, `sql`, `bash`, `gradle`, `yaml`, etc.

### Exemple de corps JSON complet pour une fiche Android

```json
{
  "titre":       "Compose — collectAsStateWithLifecycle",
  "theme_name":  "Jetpack Compose",
  "type_name":   "Astuce",
  "description": "Collecter un Flow depuis un ViewModel dans un Composable en respectant le cycle de vie.",
  "code":        "```kotlin\n// Dépendance requise\n// implementation(\"androidx.lifecycle:lifecycle-runtime-compose:2.7.0\")\n\n@Composable\nfun MyScreen(viewModel: MyViewModel = hiltViewModel()) {\n    val uiState by viewModel.uiState.collectAsStateWithLifecycle()\n    // ...\n}\n```",
  "solution":    "Préférer `collectAsStateWithLifecycle()` à `collectAsState()` pour arrêter la collecte quand l'UI est en arrière-plan et économiser les ressources.",
  "tags":        "compose, flow, lifecycle, stateflow"
}
```
