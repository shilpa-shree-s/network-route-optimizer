
# Network Route Optimizer

A REST API that stores servers (nodes) and the connections between them (edges), and finds the lowest-latency route between any two servers.

Built with Python, Django and Django REST Framework, using test-driven development.

## Features

- **Add servers** with unique names
- **Connect servers** with a latency value (validated: must be greater than 0, no duplicates, no self-links)
- **Find the shortest route** between two servers by total latency (not by number of hops)
- **Route history**: every successful search is saved and can be queried with filters
- **Clear validation errors** with the correct HTTP status codes (`201`, `200`, `400`, `404`)
- **Automated tests** for the route-finding logic and for every endpoint

## Tech Stack

| Area      | Choice                                                                      |
| --------- | --------------------------------------------------------------------------- |
| Language  | Python 3                                                                    |
| Framework | Django, Django REST Framework                                               |
| Database  | SQLite (default; can be switched to MySQL or PostgreSQL in `settings.py`) |
| Testing   | Django test runner, DRF `APITestCase`                                     |

## Setup

```bash
git clone <your-repo-url>
cd network-route-optimizer

python -m venv venv

# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The API is now available at `http://127.0.0.1:8000/`.

## Running the Tests

```bash
python manage.py test
```

Tests run against a temporary database, so your real data is never touched.

| Test file                       | What it covers                                                                  |
| ------------------------------- | ------------------------------------------------------------------------------- |
| `tests_route_finder.py`       | Shortest-route logic on plain dictionaries (no database)                        |
| `tests_nodes_api.py`          | `POST /nodes`: success, missing name, duplicate name                          |
| `tests_edges_api.py`          | `POST /edges`: success, missing fields, bad latency, unknown node, duplicates |
| `tests_shortest_route_api.py` | `POST /routes/shortest`: 200, 404, 400, history saving                        |
| `tests_history_api.py`        | `GET /routes/history`: filters, limit, ordering, bad input                    |

## API Overview

| Method | Endpoint             | Purpose                                 |
| ------ | -------------------- | --------------------------------------- |
| POST   | `/nodes`           | Add a server                            |
| POST   | `/edges`           | Connect two servers with a latency      |
| POST   | `/routes/shortest` | Find the lowest-latency route           |
| GET    | `/routes/history`  | List past route searches (with filters) |

Full request and response examples are in [API.md](API.md).

## How It Works

A request follows the same path through every endpoint:

```
URL (urls.py) -> View (views.py) -> Serializer (validation) -> Model (database)
```

For `POST /routes/shortest`:

1. The serializer checks that both server names exist (`400` if not).
2. `build_graph()` reads the `Node` and `Edge` tables and builds a dictionary: each server maps to its neighbours and the latency to reach them.
3. `find_shortest_route()` works out the lowest-latency path on that dictionary.
4. If no path exists, the API returns `404`. Otherwise the search is saved as a `RouteQuery` and returned.

The route-finding function contains no Django code, which keeps it simple to test and explain.

## Design Decisions and Assumptions

The brief leaves a few points open. These are the choices made:

- **Connections are two-way.** An edge `ServerA - ServerB` can be travelled in both directions with the same latency.
- **Duplicate edges are detected in either direction.** If `ServerA - ServerB` exists, adding `ServerB - ServerA` is rejected with `400`.
- **A server cannot connect to itself.** Source and destination must be different.
- **Latency must be greater than 0.** This is also required for the shortest-path algorithm to be correct.
- **Only successful searches are saved to history.** Searches that return `404` (no path) or `400` (invalid input) are not stored.
- **History stores server names as text, not foreign keys.** History is a log, so old records stay readable even if a server is deleted later.
- **URLs have no trailing slash** (`/nodes`, not `/nodes/`), matching the brief. `APPEND_SLASH` is set to `False` for this reason.
- **No authentication.** The brief does not ask for it.

## Shortest-Route Algorithm

The route finder uses **Dijkstra's algorithm**:

1. Every server starts at an unknown (infinite) distance, except the source, which is 0.
2. Repeatedly pick the unvisited server with the smallest known distance.
3. For each of its neighbours, check whether going through this server is shorter. If so, update the distance and remember where we came from.
4. Stop when the destination is reached, or when nothing reachable is left.
5. Walk backwards from the destination to rebuild the path.

It works because all latencies are positive. This implementation scans for the smallest distance each round, giving O(V²) time, which is fine for small and medium networks. For very large networks it can be improved to O((V + E) log V) with a priority queue (`heapq`).

## Data Model

| Model          | Fields                                                                   | Notes                                                                  |
| -------------- | ------------------------------------------------------------------------ | ---------------------------------------------------------------------- |
| `Node`       | `name`                                                                 | `name` is unique                                                     |
| `Edge`       | `source`, `destination`, `latency`                                 | Foreign keys to `Node`; unique on the `(source, destination)` pair |
| `RouteQuery` | `source`, `destination`, `total_latency`, `path`, `created_at` | Ordered newest first                                                   |

## Project Structure

```
network-route-optimizer/
├── manage.py
├── requirements.txt
├── README.md
├── API.md
├── config/
│   ├── settings.py
│   └── urls.py
└── routes/
    ├── models.py                    # Node, Edge, RouteQuery
    ├── serializers.py               # validation and JSON conversion
    ├── views.py                     # endpoints and build_graph()
    ├── urls.py                      # URL routes
    ├── route_finder.py              # shortest-route logic (no Django code)
    ├── tests_route_finder.py
    ├── tests_nodes_api.py
    ├── tests_edges_api.py
    ├── tests_shortest_route_api.py
    └── tests_history_api.py
```

## Possible Improvements

- List and delete endpoints for nodes and edges
- Pagination on the history endpoint
- Authentication (for example JWT)
- Priority-queue version of the route finder for very large networks
- Caching the graph, or frequently requested routes
- Switching to MySQL or PostgreSQL for production
