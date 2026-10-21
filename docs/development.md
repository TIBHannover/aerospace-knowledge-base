# Development guide

## Requirements

The recommended full-stack workflow requires Docker Engine with the Compose plugin, or Docker Desktop.

The component-by-component workflow requires:

- Python 3.10
- Node.js 20 or later
- GraphDB 10.8.4

## Docker Compose workflow

From the repository root:

```bash
docker compose up --build
```

The frontend is available at `http://localhost:3000`, the API at `http://localhost:5000/api/v1.0/`, and GraphDB at `http://localhost:7200`.

Follow the combined service logs with:

```bash
docker compose logs -f
```

Stop the stack while retaining GraphDB data:

```bash
docker compose down
```

GraphDB data is stored in the named `graphdb-data` volume. Running `docker compose down -v` deletes that volume and its contents.

Host ports can be overridden with `GRAPHDB_PORT`, `BACKEND_PORT`, and `FRONTEND_PORT`. Rebuild the frontend after changing `BACKEND_PORT`, because `NEXT_PUBLIC_API_URL` is embedded in the browser bundle at build time.

## Manual backend setup

Create an isolated Python environment and install the backend dependencies:

```bash
python3.10 -m venv .venv
source .venv/bin/activate
python -m pip install -r backend/requirements.txt
```

Start GraphDB at `http://localhost:7200`.

The bootstrap command creates the configured repository when necessary and loads `backend/onto.owl` only when the application graph is empty:

```bash
python backend/seed_graphdb.py
```

Start the API:

```bash
python backend/api.py
```

For development with automatic reload:

```bash
cd backend
uvicorn api:app --reload --port 5000
```

## Manual frontend setup

With GraphDB and the backend running, open another terminal and run:

```bash
cd frontend
cp .env.example .env.local
npm ci
npm run dev
```

The frontend is available at `http://localhost:3000`.

## Configuration

| Variable | Default | Purpose |
| --- | --- | --- |
| `GRAPHDB_URL` | `http://localhost:7200` | GraphDB server URL |
| `GRAPHDB_REPOSITORY` | `coupled_modelling` | GraphDB repository identifier |
| `GRAPHDB_GRAPH` | `http://coupled_modelling.owl` | Application named-graph IRI |
| `GRAPHDB_USER` | unset | Optional GraphDB username |
| `GRAPHDB_PASSWORD` | unset | Optional GraphDB password |
| `CORS_ALLOWED_ORIGINS` | `http://localhost:3000` | Comma-separated browser origins |
| `NEXT_PUBLIC_API_URL` | `http://localhost:5000/api/v1.0` | Browser-visible backend API URL |
| `GRAPHDB_PORT` | `7200` | GraphDB host port used by Compose |
| `BACKEND_PORT` | `5000` | Backend host port used by Compose |
| `FRONTEND_PORT` | `3000` | Frontend host port used by Compose |

## Loading the synthetic fixture

The following command imports `examples/synthetic/coupled-system.json` and persists the updated ontology:

```bash
python backend/load_synthetic_fixture.py
```

This operation modifies the configured repository. Use a fresh or dedicated repository. Every execution creates another coupled-system instance.

## Backend tests

The mock-isolated tests do not require a live GraphDB server:

```bash
PYTHONPATH=backend:tests python -m unittest \
  test_serialization \
  test_explorer_api \
  test_web_mutations \
  test_deletion_sets \
  test_openapi_spec \
  test_api_contract \
  test_cors \
  -v
```

The complete suite includes GraphDB integration tests and modifies the configured repository. Use a fresh or dedicated repository and load the synthetic fixture once before running it:

```bash
PYTHONPATH=backend python backend/load_synthetic_fixture.py
PYTHONPATH=backend:tests python -m unittest discover -s tests -p "test_*.py" -v
```

## Frontend gates

Run from `frontend/`:

```bash
npm run lint
npm run type-check
npm run format:check
npm run test:ci
npm run build
```

## OpenAPI workflow

After changing an API route or schema, regenerate the committed contract:

```bash
python backend/export_openapi.py
```

With the backend running, regenerate the frontend API types:

```bash
cd frontend
npm run generate:api-types
```

Do not edit `frontend/src/types/openapi.ts` manually.

The running backend exposes:

- OpenAPI YAML: `http://localhost:5000/api/v1.0/openapi.yaml`
- OpenAPI JSON: `http://localhost:5000/api/v1.0/openapi.json`
- Interactive documentation: `http://localhost:5000/api/v1.0/docs`
