
# API Reference

Base URL (local): `http://127.0.0.1:8000`

All requests and responses use JSON. For `POST` requests, send the header `Content-Type: application/json`.

URLs have **no trailing slash**: use `/nodes`, not `/nodes/`.

## Quick Reference

| Method | Endpoint             | Success | Errors           |
| ------ | -------------------- | ------- | ---------------- |
| POST   | `/nodes`           | `201` | `400`          |
| POST   | `/edges`           | `201` | `400`          |
| POST   | `/routes/shortest` | `200` | `400`, `404` |
| GET    | `/routes/history`  | `200` | `400`          |

---

## 1. Add Node

**POST** `/nodes`

Adds a server. Names must be unique.

### Request body

| Field    | Type   | Required | Notes                  |
| -------- | ------ | -------- | ---------------------- |
| `name` | string | yes      | Must not already exist |

```json
{
  "name": "ServerA"
}
```

### Success: `201 Created`

```json
{
  "id": 1,
  "name": "ServerA"
}
```

### Errors: `400 Bad Request`

Name missing:

```json
{
  "name": ["This field is required."]
}
```

Name already exists:

```json
{
  "name": ["node with this name already exists."]
}
```

### Example (PowerShell)

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/nodes -ContentType "application/json" -Body '{"name": "ServerA"}'
```

### Example (curl)

```bash
curl -X POST http://127.0.0.1:8000/nodes \
  -H "Content-Type: application/json" \
  -d '{"name": "ServerA"}'
```

---

## 2. Add Edge

**POST** `/edges`

Connects two existing servers with a latency. Connections are treated as two-way.

### Request body

| Field           | Type   | Required | Notes                                                 |
| --------------- | ------ | -------- | ----------------------------------------------------- |
| `source`      | string | yes      | Name of an existing server                            |
| `destination` | string | yes      | Name of an existing server, different from `source` |
| `latency`     | number | yes      | Must be greater than 0                                |

```json
{
  "source": "ServerA",
  "destination": "ServerB",
  "latency": 12.5
}
```

### Success: `201 Created`

```json
{
  "id": 1,
  "source": "ServerA",
  "destination": "ServerB",
  "latency": 12.5
}
```

### Errors: `400 Bad Request`

Source or destination missing:

```json
{
  "destination": ["This field is required."]
}
```

Server does not exist:

```json
{
  "destination": ["Object with name=Nope does not exist."]
}
```

Latency zero or negative:

```json
{
  "latency": ["Latency must be greater than 0."]
}
```

Source and destination are the same server:

```json
{
  "non_field_errors": ["Source and destination must be different."]
}
```

Edge already exists (in either direction):

```json
{
  "non_field_errors": ["This edge already exists."]
}
```

### Example (PowerShell)

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/edges -ContentType "application/json" -Body '{"source": "ServerA", "destination": "ServerB", "latency": 12.5}'
```

### Example (curl)

```bash
curl -X POST http://127.0.0.1:8000/edges \
  -H "Content-Type: application/json" \
  -d '{"source": "ServerA", "destination": "ServerB", "latency": 12.5}'
```

---

## 3. Get Shortest Route

**POST** `/routes/shortest`

Finds the route with the lowest total latency between two servers. A successful search is saved to the history.

### Request body

| Field           | Type   | Required | Notes                      |
| --------------- | ------ | -------- | -------------------------- |
| `source`      | string | yes      | Name of an existing server |
| `destination` | string | yes      | Name of an existing server |

```json
{
  "source": "ServerA",
  "destination": "ServerD"
}
```

### Success: `200 OK` (path exists)

```json
{
  "total_latency": 23.4,
  "path": ["ServerA", "ServerB", "ServerD"]
}
```

### Not found: `404 Not Found` (no path)

Both servers exist, but no chain of connections links them.

```json
{
  "error": "No path exists between ServerA and ServerD"
}
```

### Errors: `400 Bad Request`

A server does not exist, or a field is missing:

```json
{
  "destination": ["Object with name=Nope does not exist."]
}
```

### Example (PowerShell)

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/routes/shortest -ContentType "application/json" -Body '{"source": "ServerA", "destination": "ServerD"}'
```

### Example (curl)

```bash
curl -X POST http://127.0.0.1:8000/routes/shortest \
  -H "Content-Type: application/json" \
  -d '{"source": "ServerA", "destination": "ServerD"}'
```

---

## 4. Get Route Query History

**GET** `/routes/history`

Returns saved route searches, newest first. All query parameters are optional and can be combined.

### Query parameters

| Parameter       | Type                | Description                                  |
| --------------- | ------------------- | -------------------------------------------- |
| `source`      | string              | Only searches that started at this server    |
| `destination` | string              | Only searches that ended at this server      |
| `limit`       | integer (1 or more) | Maximum number of records to return          |
| `date_from`   | date or datetime    | Only searches created on or after this time  |
| `date_to`     | date or datetime    | Only searches created on or before this time |

Dates accept `2026-10-24` or a full timestamp such as `2026-10-24T14:30:00Z`.

### Success: `200 OK`

```json
[
  {
    "id": 2,
    "source": "ServerB",
    "destination": "ServerC",
    "total_latency": 10.1,
    "path": ["ServerB", "ServerC"],
    "created_at": "2026-10-24T15:10:00Z"
  },
  {
    "id": 1,
    "source": "ServerA",
    "destination": "ServerD",
    "total_latency": 23.4,
    "path": ["ServerA", "ServerB", "ServerD"],
    "created_at": "2026-10-24T14:32:00Z"
  }
]
```

If nothing matches, the response is an empty list: `[]`.

### Errors: `400 Bad Request`

Invalid `limit`:

```json
{
  "limit": ["A valid integer is required."]
}
```

Invalid date:

```json
{
  "date_from": [
    "Datetime has wrong format. Use one of these formats instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z]."
  ]
}
```

### Examples (PowerShell)

Quote any URL that contains `?`.

```powershell
# everything
Invoke-RestMethod -Uri http://127.0.0.1:8000/routes/history

# only searches that started at ServerA
Invoke-RestMethod -Uri "http://127.0.0.1:8000/routes/history?source=ServerA"

# the 5 most recent searches ending at ServerD
Invoke-RestMethod -Uri "http://127.0.0.1:8000/routes/history?destination=ServerD&limit=5"

# searches from a given date onwards
Invoke-RestMethod -Uri "http://127.0.0.1:8000/routes/history?date_from=2026-10-24"
```

### Examples (curl)

```bash
curl "http://127.0.0.1:8000/routes/history"
curl "http://127.0.0.1:8000/routes/history?source=ServerA&limit=5"
curl "http://127.0.0.1:8000/routes/history?date_from=2026-10-01&date_to=2026-10-31"
```

---

## Try the Whole Flow

Run these in order from a fresh database:

```powershell
# 1. add servers
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/nodes -ContentType "application/json" -Body '{"name": "ServerA"}'
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/nodes -ContentType "application/json" -Body '{"name": "ServerB"}'
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/nodes -ContentType "application/json" -Body '{"name": "ServerD"}'

# 2. connect them
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/edges -ContentType "application/json" -Body '{"source": "ServerA", "destination": "ServerB", "latency": 12.5}'
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/edges -ContentType "application/json" -Body '{"source": "ServerB", "destination": "ServerD", "latency": 10.9}'

# 3. find the shortest route (total_latency 23.4, path A -> B -> D)
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/routes/shortest -ContentType "application/json" -Body '{"source": "ServerA", "destination": "ServerD"}'

# 4. see it in the history
Invoke-RestMethod -Uri http://127.0.0.1:8000/routes/history
```

## Status Code Summary

| Code    | Meaning in this API                                                                       |
| ------- | ----------------------------------------------------------------------------------------- |
| `200` | Route found, or history returned                                                          |
| `201` | Node or edge created                                                                      |
| `400` | Invalid input: missing field, duplicate, unknown server, bad latency, bad query parameter |
| `404` | Both servers exist but no path connects them                                              |
