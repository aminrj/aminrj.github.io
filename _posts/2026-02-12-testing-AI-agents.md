---
title: From MVP to Production (wip)
date: 2026-01-31
uuid: 202512180000
status: published
content-type: # article/video/thread/course
target-audience: # beginner/intermediate/advanced
categories: [LLM]
image:
  path: /assets/media/n8n/n8n_automation_patterns.png
---

# LLM Engineering Part 3: From Working LLM App to Production SaaS MVP

This article is a practical walkthrough of what it takes to move a working LLM application into a production-ready SaaS MVP, using the `procurement-ai` project as the reference implementation.

The first two articles covered:

- Building the first working Procurement Analyst AI.
- Building production-ready LLM agents.

This part is about the layer above agents: storage, APIs, UI, tenancy, deployment, and operational safeguards.

## 1. Production-Readiness Snapshot (Current State)

Recent hardening work in this codebase focused on:

- Stable API/storage contracts.
- Multi-tenant auth via organization API keys.
- Safer persistence via upsert semantics.
- Status normalization across orchestration, API, and DB.
- Updated scripts/docs and broad test coverage.

Evidence:

- `docs/CHANGES.md` (February 5, 2026) documents the stabilization scope.
- Current test run in the project venv: `81 passed, 3 skipped, 4 deselected`.

At this stage, this is a strong SaaS MVP baseline, not yet a fully hardened production platform. That distinction matters.

## 2. Step One: Persist the Right Things (and Persist Them Safely)

Most LLM demos fail in production because they treat the model response as the product. In practice, your product is the persisted system of record around LLM outputs.

In this project, storage moved to a multi-tenant SQLAlchemy model with explicit processing states.

```python
# src/procurement_ai/storage/models.py
class Organization(Base):
    __tablename__ = "organizations"
    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    api_key = Column(String(128), unique=True, nullable=False, index=True)
    monthly_analysis_limit = Column(Integer, nullable=False, default=100)
    monthly_analysis_count = Column(Integer, nullable=False, default=0)

class TenderDB(Base):
    __tablename__ = "tenders"
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False, index=True)
    external_id = Column(String(255), nullable=True, index=True)
    status = Column(Enum(TenderStatus), nullable=False, default=TenderStatus.PENDING, index=True)
    processing_time = Column(Float, nullable=True)
    error_message = Column(Text, nullable=True)

    __table_args__ = (
        UniqueConstraint("organization_id", "external_id", name="uq_org_external_id"),
        Index("idx_org_status_created", "organization_id", "status", "created_at"),
    )
```

Two key production moves here:

- Tenant isolation through `organization_id`.
- Idempotency and dedupe via `(organization_id, external_id)` uniqueness.

### Use migrations as product evolution history

Instead of manual table edits, schema evolves via Alembic. A recent migration added `api_key` to organizations:

```python
# alembic/versions/20260205_0900_add_organization_api_key.py
def upgrade() -> None:
    op.add_column("organizations", sa.Column("api_key", sa.String(length=128), nullable=True))
    op.execute("UPDATE organizations SET api_key = slug WHERE api_key IS NULL")
    op.alter_column("organizations", "api_key", nullable=False)
    op.create_index(op.f("ix_organizations_api_key"), "organizations", ["api_key"], unique=True)
```

This is exactly the kind of compatibility-preserving change you need in a live SaaS system.

### Prefer upsert for LLM outputs

Re-analysis should not break on uniqueness constraints. Repositories now use upsert patterns:

```python
# src/procurement_ai/storage/repositories.py
def upsert(self, tender_id: int, is_relevant: bool, confidence: float, **kwargs: Any) -> AnalysisResult:
    analysis = self.get_by_tender_id(tender_id)
    if analysis:
        analysis.is_relevant = is_relevant
        analysis.confidence = confidence
        for key, value in kwargs.items():
            if hasattr(analysis, key):
                setattr(analysis, key, value)
        analysis.updated_at = datetime.now()
        self.session.flush()
        return analysis
    return self.create(tender_id=tender_id, is_relevant=is_relevant, confidence=confidence, **kwargs)
```

Without this, retries and reprocessing become a source of outages.

## 3. Step Two: Treat Orchestration as a Stateful Workflow

A demo chain can just call model A -> model B -> model C. Production needs:

- Early-stop logic.
- Explicit terminal statuses.
- Processing metrics.
- Error capture.

```python
# src/procurement_ai/orchestration/simple_chain.py
async def process_tender(self, tender: Tender) -> ProcessedTender:
    start_time = datetime.now()
    result = ProcessedTender(tender=tender)
    try:
        result.filter_result = await self.filter_agent.filter(tender)
        if (not result.filter_result.is_relevant
            or result.filter_result.confidence < self.config.MIN_CONFIDENCE):
            result.status = "filtered_out"
            return result

        result.rating_result = await self.rating_agent.rate(tender, categories)
        if result.rating_result.overall_score < self.config.MIN_SCORE_FOR_DOCUMENT:
            result.status = "rated_low"
            return result

        result.bid_document = await self.doc_generator.generate(...)
        result.status = "complete"
    except Exception as e:
        result.status = "error"
        result.error = str(e)
    finally:
        result.processing_time = (datetime.now() - start_time).total_seconds()
    return result
```

This is the first point where your LLM app starts behaving like a backend service instead of a notebook.

## 4. Step Three: Productize the API Contract

For client-facing behavior, this project uses a simple but correct pattern:

- `POST /api/v1/analyze` returns `202 Accepted`.
- Processing runs in background tasks.
- Clients poll `GET /api/v1/tenders/{id}` for completion.

```python
# src/procurement_ai/api/routes/tenders.py
@router.post("/analyze", response_model=AnalysisResponse, status_code=status.HTTP_202_ACCEPTED)
async def analyze_tender(...):
    if not organization.can_analyze():
        raise HTTPException(status_code=429, detail="Monthly analysis limit reached")

    tender_db = tender_repo.create(...)
    org_repo.update_usage(organization.id)
    tender_repo.update_status(tender_db.id, TenderStatus.PROCESSING)

    background_tasks.add_task(process_tender_background, tender_db.id, tender_data, db, config, llm_service)
    return AnalysisResponse(tender=TenderResponse.model_validate(tender_db), status="processing")
```

### Add minimal SaaS auth and usage limits early

```python
# src/procurement_ai/api/dependencies.py
def get_current_organization(x_api_key: str = Header(...), session: Session = Depends(get_db_session)):
    org_repo = OrganizationRepository(session)
    org = org_repo.get_by_api_key(x_api_key) or org_repo.get_by_slug(x_api_key)
    if not org:
        raise HTTPException(status_code=401, detail="Invalid API key")
    if not org.is_active:
        raise HTTPException(status_code=403, detail="Organization is inactive")
    return org
```

This is enough for MVP tenancy and billing guardrails while you postpone full user auth/JWT.

## 5. Step Four: Build an Operator UI, Not Just API Docs

A production MVP needs internal and customer-facing operability. The HTMX server-rendered UI here gives:

- Real dashboard stats.
- Filtering/search.
- Tender detail modal.
- One-click analysis.

```html
<!-- src/procurement_ai/api/templates/dashboard.html -->
<form
  hx-get="/web/tenders"
  hx-target="#tender-list"
  hx-trigger="change, submit"
>
  <select name="status">
    <option value="">All</option>
    <option value="pending">Pending</option>
    <option value="processing">Processing</option>
    <option value="complete">Complete</option>
  </select>
  <input type="text" name="search" placeholder="Search tenders..." />
</form>
```

This is a practical MVP choice: low frontend complexity, high operational value.

## 6. Step Five: Add Ingestion Pipelines with Deduplication

An LLM workflow only becomes a product when fed by repeatable data ingestion.

This project’s TED ingestion script:

- Fetches source notices.
- Enriches details.
- Checks dedupe keys.
- Stores records under organization scope.

```python
# scripts/fetch_and_store.py
existing = tender_repo.get_by_external_id(external_id, org_id)
if existing:
    skipped_count += 1
    continue

tender_repo.create(
    organization_id=org_id,
    title=tender_data["title"],
    description=tender_data.get("description", tender_data["title"]),
    organization_name=tender_data.get("buyer_name", "Unknown"),
    external_id=external_id,
    source="ted_europa",
)
```

Combined with unique constraints, this avoids duplicate growth and protects downstream analytics.

## 7. Step Six: Use Layered Testing as a Deployment Gate

A production-ready LLM MVP should test at three levels:

- Unit tests for deterministic logic and adapters.
- Integration tests for API and storage behavior.
- Optional E2E tests for real running services.

This repo does exactly that:

- `tests/unit/`
- `tests/integration/`
- `tests/e2e/`

Integration API tests use dependency overrides to keep LLM behavior deterministic:

```python
# tests/integration/test_api.py
app.dependency_overrides[get_db] = lambda: db
app.dependency_overrides[get_llm_service] = lambda: DummyLLMService()
```

Current local result:

- `81 passed`
- `3 skipped` (environment-dependent PostgreSQL workflows)
- `4 deselected` (default markers exclude e2e/wip)

This gives a reliable quality baseline for iterative delivery.

## 8. Step Seven: Make It Deployable by Default

A SaaS MVP should run in one command locally and in CI/staging with minimal differences.

This project includes:

- `docker-compose.yml` for Postgres/Redis/API.
- `deployment/Dockerfile.api` for containerized API.
- Operational scripts for setup and smoke testing.

```yaml
# docker-compose.yml
services:
  postgres:
    image: postgres:15-alpine
  redis:
    image: redis:7-alpine
  api:
    build:
      context: .
      dockerfile: deployment/Dockerfile.api
    command: uvicorn procurement_ai.api.main:app --host 0.0.0.0 --port 8000 --reload
```

This is a strong MVP packaging baseline for demos, pilots, and early customer validation.

## 9. What Still Needs Work Before "Production at Scale"

This is the critical part. A good production-readiness article should not pretend the MVP is complete.

Priority backlog from current architecture:

1. Replace FastAPI in-process background tasks with a real queue-worker model (Celery/RQ/Arq) for reliability under restarts.
2. Add observability: structured logs, request IDs, model latency/cost metrics, tracing.
3. Harden security: API key rotation, secret manager integration, stricter CORS, rate limiting by key/IP.
4. Add retries and dead-letter handling around external dependencies (LLM API, TED ingestion).
5. Separate sync UI-triggered analysis from async API-triggered analysis with one shared job orchestration path.
6. Add monthly usage reset automation and billing/audit events.
7. Add CI pipeline gates for migrations, tests, and lint before deployment.
8. Improve health checks to include downstream dependency readiness (LLM endpoint reachability, queue health).

If you do these 8 items, you move from "production-ready MVP" to "operationally durable production system."

## 10. Practical Blueprint You Can Reuse

If you already have a working LLM app, this transition sequence is practical:

1. Stabilize output contracts with Pydantic schemas and strict parsing.
2. Add workflow statuses and persist every state transition.
3. Introduce multi-tenant storage model and migration discipline.
4. Productize API semantics (`202 + polling`) and tenant auth.
5. Build a lightweight operations UI.
6. Add ingestion with dedupe keys.
7. Add layered tests and smoke scripts.
8. Package runtime with Docker and environment-driven config.
9. Close reliability/security/observability gaps incrementally.

That sequence is exactly what this Procurement AI project now demonstrates.

## Final Takeaway

The jump from "LLM app works" to "SaaS MVP is production-ready" is not a prompt-engineering problem. It is a software engineering problem:

- State management.
- Contracts.
- Tenancy.
- Persistence.
- Operability.
- Reliability under failure.

The strongest signal of maturity in this project is not just that it generates analyses; it is that the system now has explicit contracts for how analyses are created, stored, retrieved, secured, and tested.

Like what you read ?

Want to discuss more around AI and how to code with LLM strategies?

Connect with me on [LinkedIn] or follow my journey on [Medium] where I share real-world insights from my experiments and research.

Also, make sure to start ⭐️ the Git repo for this article 😉.

Thanks for reading.
