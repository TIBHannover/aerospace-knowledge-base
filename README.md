# Aerospace Knowledge Base

The Aerospace Knowledge Base represents Kratos Multiphysics CoSimulation configurations as OWL/RDF and stores them in GraphDB. It provides a FastAPI service and a Next.js web explorer for importing, inspecting, editing, searching, and exporting coupled-system models.

## Quick start with Docker

Install Docker Engine with the Compose plugin, or Docker Desktop. From the repository root, start GraphDB, the backend API, and the web explorer:

```bash
docker compose up --build
```

The services are available at:

- Web explorer: `http://localhost:3000`
- API health: `http://localhost:5000/api/v1.0/health/`
- Interactive API documentation: `http://localhost:5000/api/v1.0/docs`
- GraphDB Workbench: `http://localhost:7200`

On first start, the backend creates the configured GraphDB repository and seeds its empty application graph from `backend/onto.owl`. GraphDB data persists in the `graphdb-data` Docker volume.

Stop the stack without deleting its data:

```bash
docker compose down
```

`docker compose down -v` also deletes the persistent GraphDB volume. Use it only when an intentional data reset is required.

## Development

For component-by-component setup, configuration, testing, fixture loading, and API-contract workflows, see [docs/development.md](docs/development.md).

The manual development workflow requires Python 3.10, Node.js 20 or later, and GraphDB 10.8.4. Backend Python dependencies and frontend Node dependencies are managed independently.

## Architecture

- `backend/` — FastAPI HTTP API and the Owlready2/GraphDB integration.
- `frontend/` — Next.js web explorer.
- `openapi.yaml` — generated OpenAPI 3.1 contract.
- `examples/synthetic/` — minimal synthetic input used for integration verification.
- `tests/` — backend unit, contract, and GraphDB integration tests.

The backend uses direct SPARQL for reads and simple mutations. Structurally complex import, export, copy, and inference operations use Owlready2 and synchronize with GraphDB.

## API contract

The backend generates [openapi.yaml](openapi.yaml) from its FastAPI routes and schemas. The running API also serves the contract as YAML and JSON. Contract-freshness tests detect differences between the implementation and the committed specification.

## Data notice

The included example is synthetic and is not research, benchmark, or evaluation data. See [examples/README.md](examples/README.md).

## License

This repository is licensed under the [MIT License](LICENSE).
