# agentic-sdlc-url-shortener
Agentic SDLC automation prototype for a production-oriented URL shortener
## Objective

Demonstrate how AI agents can transform an engineering requirement into a reviewable engineering outcome while maintaining:

- Requirement understanding

- Task decomposition

- Dependency-aware orchestration

- Sequential and parallel execution

- Human approval checkpoints

- Bounded retries

- Rollback and safe-stop controls

- Auditability and decision lineage

- Reliability metrics

- Automated testing

- Documentation and release readiness

## Architecture

The system contains two major areas:

### URL Shortener Application

- FastAPI REST API

- SQLite persistence

- SQLAlchemy

- URL creation

- Short-code redirection

- Click analytics

- Health endpoint

### Agentic Orchestration Layer

- Task lifecycle management

- Workflow state

- Dependency graph

- Approval gates

- Retry policy

- Rollback

- Safe-stop

- Audit logging

- Reliability metrics

- Workflow orchestration

See:

- `docs/architecture.md`

- `docs/orchestration.md`

## Project Structure

```text

src/

├── main.py

├── api/

│   ├── __init__.py

│   └── routes.py

├── domain/

│   └── url.py

├── infrastructure/

│   ├── database.py

│   └── models.py

└── orchestration/

    ├── task.py

    ├── state.py

    ├── graph.py

    ├── gates.py

    ├── retry.py

    ├── rollback.py

    ├── audit.py

    ├── metrics.py

    └── orchestrator.py

tests/

└── test_api.py
