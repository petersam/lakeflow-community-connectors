# Demo Guide — Pre-Bronze Security Data Ingestion
## Snyk & Wiz via Lakeflow Community Connectors

---

| Field | Detail |
|-------|--------|
| **Presenter** | Sam Adhikari |
| **Demo Date** | [DATE] at [TIME] |
| **Duration** | 30 minutes |
| **Meeting Link** | [ZOOM / TEAMS LINK] |
| **Repo** | https://github.com/databrickslabs/lakeflow-community-connectors |
| **Branch** | master |
| **Status** | ✅ Both connectors implemented · All tests passing |

---

## Table of Contents

1. [Pre-Demo Slack Messages](#1-pre-demo-slack-messages)
2. [Meeting Agenda](#2-meeting-agenda)
3. [Demo Script — Block by Block](#3-demo-script--block-by-block)
4. [Technical Reference](#4-technical-reference)
5. [Live Commands Cheat Sheet](#5-live-commands-cheat-sheet)
6. [Expected Questions & Answers](#6-expected-questions--answers)
7. [Post-Demo Follow-Up Template](#7-post-demo-follow-up-template)

---

## 1. Pre-Demo Slack Messages

### Message A — Send 72 Hours Before

```
👋 Hey team — dropping some context ahead of our demo on [DATE] at [TIME].

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 Demo: Pre-Bronze Security Data Ingestion — Snyk & Wiz via Lakeflow Community Connectors
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🧩 What's the problem we're solving?
Our security team runs Snyk (code vulnerabilities) and Wiz (cloud risks) — but that
data doesn't live in Databricks today. We can't correlate it with our data assets,
trend it over time, or build alerts on top of it. This demo shows a path to get it
into our pre-bronze layer on a scheduled, reliable basis.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🗂 Quick background — 3 approaches we evaluated

1️⃣ Config-based Metadata-Driven Collector — custom YAML/JSON-driven ingestion.
   Flexible, but we own all the plumbing.

2️⃣ Lakebase UI — UI-driven pipeline setup. Great for standard catalog sources,
   but Snyk and Wiz don't fit that mold.

3️⃣ Lakeflow Community Connectors — open-source framework from Databricks Labs.
   You implement a 4-method Python interface; the framework handles Spark, Delta
   writes, CDC, checkpointing, and scheduling. ← this is what the demo focuses on

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Agenda (30 mins)

  1. Problem statement + why this matters         3 min
  2. 3-approach comparison + decision rationale   5 min
  3. Architecture walkthrough                     4 min
  4. Live code demo — Snyk + Wiz connectors      10 min
  5. Live test run — all tests passing            4 min
  6. What's next + open discussion               4 min

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 Key things you'll see in the demo

• Working Snyk connector — 6 tables (organizations, projects, issues,
  vulnerabilities, targets, users)
• Working Wiz connector — 6 tables (issues, cloud resources, vulnerabilities,
  projects, users, controls)
• In-memory mock API — tests run with zero real credentials, simulating full
  pagination and CDC offset logic
• 14 tests passing across both connectors in under 1 second
• The full path: Python class → Unity Catalog connection → Delta table

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 No prep needed — but if you want context ahead of time:

• What is Lakeflow Community Connectors?
  → https://github.com/databrickslabs/lakeflow-community-connectors

• What is a pre-bronze layer?
  Raw, unmodified data landed from source systems before any transformation.
  Bronze is your first clean layer; pre-bronze is the ingestion mechanism itself.

• What is CDC?
  Change Data Capture — instead of reloading a full table every run, we track
  what changed using a cursor field (e.g. updated_at) and only fetch new/modified
  records.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 Date/Time: [DATE] at [TIME]
🔗 Meeting: [ZOOM/TEAMS LINK]
⏱ Duration: 30 minutes

Happy to answer questions before the demo — drop them here and I'll address
them during the session too. 🙌
```

---

### Message B — Send Day-of (Morning)

```
🔔 Reminder — demo is today at [TIME]!

Pre-Bronze Security Data Ingestion — Snyk & Wiz via Lakeflow Community Connectors

Quick summary of what we'll cover:
→ Why Snyk + Wiz data belongs in Databricks
→ Live working connectors with full test suite
→ Comparison of 3 ingestion approaches
→ What's next

🔗 [MEETING LINK] — see you there!
```

---

## 2. Meeting Agenda

```
┌─────────────────────────────────────────────────────────────────────┐
│  PRE-BRONZE SECURITY DATA INGESTION                                 │
│  Snyk & Wiz via Lakeflow Community Connectors                       │
│  Presenter: Sam Adhikari  │  Duration: 30 minutes                  │
└─────────────────────────────────────────────────────────────────────┘

  [0:00 – 0:03]  Block 1 — Problem Statement
                 Why security data needs to be in Databricks

  [0:03 – 0:08]  Block 2 — Three-Approach Comparison
                 Config-based vs Lakebase UI vs Lakeflow Community
                 Why we're recommending Lakeflow Community Connectors

  [0:08 – 0:12]  Block 3 — Architecture Overview
                 The 4-method interface contract
                 How the framework handles Spark, Delta, CDC

  [0:12 – 0:22]  Block 4 — Live Code Demo
                 Snyk connector walkthrough (REST/JSON:API)
                 Wiz connector walkthrough (GraphQL/OAuth2)
                 Mock API strategy — zero external dependencies

  [0:22 – 0:26]  Block 5 — Live Test Run
                 pytest across both connectors
                 14 tests passing, 0 external calls

  [0:26 – 0:30]  Block 6 — What's Next + Q&A
                 Path to production
                 Open discussion
```

---

## 3. Demo Script — Block by Block

> 💡 **Presenter tip:** Read this section out loud once before the demo. Don't memorize it — just internalize the flow. The exact words don't matter; the structure does.

---

### Block 1 — Problem Statement (3 min)

**Open with this — no slides, just talk:**

> "Today I want to show you something I've been building over the past few weeks.
> Our security team uses two key tools — Snyk for scanning code vulnerabilities
> in our repositories, and Wiz for monitoring cloud infrastructure risks.
>
> Both tools have rich data. But right now that data is trapped in their UIs.
> We can't join it with our pipeline metadata, we can't track trends over time,
> and we can't build unified security dashboards in Databricks.
>
> The goal of today's demo is to show a working path to land that data in our
> pre-bronze layer — raw, auditable, refreshing on a schedule — using an
> open-source framework from Databricks Labs called Lakeflow Community Connectors."

**Pause. Let it land. Then say:**

> "Before I show you the code, let me give you 5 minutes of context on how
> we got here — because we actually evaluated three different approaches."

---

### Block 2 — Three-Approach Comparison (5 min)

**Share screen on the comparison table below (or whiteboard it):**

| | Config-based Metadata Collector | Lakebase UI | Lakeflow Community Connectors |
|---|---|---|---|
| **How it works** | YAML/JSON config drives ingestion logic | UI-driven pipeline setup | Python class implementing a 4-method interface; runs on Spark PDS |
| **Flexibility** | High — you control all logic | Low-medium — bounded by UI | High — full Python, any API shape |
| **Standardization** | Low — every connector is bespoke | Medium — UI enforces a pattern | High — every connector looks identical |
| **Testability** | Hard — tightly coupled to infra | Hard — UI state is hard to test | Easy — pytest against live or mock API |
| **Community / reuse** | Internal only | Internal only | Open source, Databricks-maintained |
| **Maintenance** | Team owns everything | Databricks owns UI layer | Team owns connector code; framework is shared |
| **Best for** | One-off custom sources | Fast onboarding of standard sources | New community sources needing full lifecycle |

**Say:**

> "The config-based approach gave us flexibility but we ended up owning too much
> plumbing — every new source was a new bespoke implementation.
>
> The Lakebase UI is great for sources that are already in the catalog, but Snyk
> and Wiz are not standard catalog sources — they need custom connector logic.
>
> Lakeflow Community Connectors hits the sweet spot. We write Python that follows
> a clear 4-method contract, and the framework handles all the Spark and pipeline
> machinery underneath."

---

### Block 3 — Architecture Overview (4 min)

**Open `REPO-OVERVIEW.md` on screen, point to Section 2.**

**Say:**

> "The core of the framework is a single abstract base class called LakeflowConnect.
> Every connector — ours and the community's — implements exactly these 4 methods."

**Read through the 4 methods:**

```
list_tables()          → what tables does this source expose?
get_table_schema()     → what does each table look like (Spark StructType)?
read_table_metadata()  → how should it be ingested — snapshot or CDC?
read_table()           → give me the records, paginated, with an offset
```

**Say:**

> "That's the whole contract. Four methods.
>
> The framework takes those four methods and wires them into Spark, writes to
> Delta, handles checkpointing so we don't re-ingest the same records, and
> manages schema evolution. We never write a line of pipeline code.
>
> For ingestion type: snapshot means full reload every run — good for reference
> tables like projects or users. CDC means incremental — we pass in a cursor value
> from the last run and only fetch records that changed since then. Snyk issues
> and Wiz issues are both CDC — we only pull what's new or updated."

---

### Block 4 — Live Code Demo (10 min)

> 💡 **Open these files in VS Code before the call starts:**
> - `sources/snyk/snyk.py`
> - `sources/snyk/snyk_schemas.py`
> - `sources/snyk/snyk_mock_api.py`
> - `sources/wiz/wiz_mock_api.py`
> - `tests/unit/sources/snyk/test_snyk_connector.py`

---

#### Step 1 — `snyk.py` (2 min)

Open `snyk.py`. Point to:

```python
def __init__(self, options: dict[str, str]) -> None:
```
> "Options come directly from the Unity Catalog connection object. No hardcoded
> credentials anywhere in the code."

Point to the dispatch table in `read_table`:
```python
dispatch = {
    "organizations": self._read_organizations,
    "projects":      self._read_projects,
    "issues":        self._read_issues,
    ...
}
```
> "One method per table. Clean, testable, easy to extend."

Point to `_paginate_rest`:
> "Snyk uses a JSON:API format with a links.next cursor for pagination. This one
> helper handles all 6 tables — no duplicated pagination logic."

Point to `_flatten_jsonapi`:
> "Snyk wraps everything in a JSON:API envelope — id, type, attributes,
> relationships. This helper flattens it into a plain dict that matches our schema."

---

#### Step 2 — `snyk_schemas.py` (1 min)

Quickly scroll through the file:
> "Schemas, metadata, and table names — three constants, one file.
> The framework uses the schema for type coercion and Delta schema evolution.
> The test harness uses it to validate every record we return."

---

#### Step 3 — `snyk_mock_api.py` (2 min)

Open `snyk_mock_api.py`. This is your strongest technical moment.

> "Here's the part I'm most proud of. We don't have live Snyk credentials in
> our dev environment, and we didn't want tests that require a VPN or real API
> keys in CI.
>
> So we built an in-memory mock API that simulates the real Snyk API exactly."

Point to `SnykMockAPI.__init__`:
> "Seeded data for all 6 tables — real-looking IDs, timestamps, field values.
> This is what the connector reads during tests."

Point to `SnykMockSession.get()`:
> "The mock session parses the URL, routes to the right handler, and returns
> paginated responses with links.next — exactly the format the real API uses.
> Page size is set to 3 intentionally, so every test exercises multi-page reads."

Point to `get_mock_api()` and `reset_mock_api()`:
> "Singleton pattern — same design as the built-in example connector.
> Tests call reset_mock_api() before setup to get a clean state."

**The punchline:**
> "To switch the connector into mock mode, you set token to the string 'mock'.
> That's it. The connector never knows it's not talking to real Snyk."

---

#### Step 4 — `wiz_mock_api.py` (2 min)

Briefly open `wiz_mock_api.py`:
> "Wiz is GraphQL, not REST — so the mock is different.
>
> The session intercepts POST requests. If the body has grant_type, it's an OAuth
> token request — the mock returns a fake bearer token. If it's anything else,
> it's a GraphQL call.
>
> For GraphQL, we extract the operation name from the query string using regex —
> GetIssues, GetCloudResources, GetVulnerabilities — and route to the right
> in-memory data store. The response format matches what the connector expects:
> data.issues.nodes[] with pageInfo.hasNextPage and endCursor."

---

#### Step 5 — `test_snyk_connector.py` (1 min)

Open the test file:

```python
class TestSnykConnector(LakeflowConnectTests):
    connector_class = SnykLakeflowConnect
    sample_records = 50

    @classmethod
    def setup_class(cls):
        cls.config = cls._load_config()
        reset_mock_api()
        super().setup_class()
```

> "Three lines of test code. The harness does everything else — schema validation,
> offset contract, metadata validation, record type-checking. Same pattern for Wiz."

---

### Block 5 — Live Test Run (4 min)

**Switch to terminal. Run:**

```bash
.venv/bin/pytest tests/unit/sources/snyk/ tests/unit/sources/wiz/ -v
```

**Narrate as tests run:**

| Test name | What to say |
|-----------|-------------|
| `test_initialization` | *"Connector boots, OAuth flow completes — mocked"* |
| `test_list_tables` | *"Returns all 6 tables for each connector"* |
| `test_invalid_table_name` | *"Raises correctly on unknown table names"* |
| `test_get_table_schema` | *"Valid Spark StructType for every table"* |
| `test_read_table_metadata` | *"CDC vs snapshot classification, primary keys, cursor fields validated"* |
| `test_read_table` | *"Actually fetches records, parses them against schema, checks non-nullables"* |
| `test_micro_batch_offset_contract` | *"Two consecutive pipeline trigger cycles — offset in, offset out, no duplicates"* |

**When you see the result:**
```
14 passed, 14 skipped in 0.20s
```

> "14 tests, zero external API calls, runs in under a second. The 14 skipped are
> write-back tests — both Snyk and Wiz are read-only APIs, which is expected and correct."

---

### Block 6 — What's Next + Q&A (4 min)

**Say:**

> "So where does this go from here?
>
> Immediate next step: swap the mock token for a real Snyk API token and a
> real org UUID. The connector code doesn't change at all — it's a config swap.
>
> After that: we write README files for each connector and submit them to the
> community repo. That means other Databricks customers can benefit from this work.
>
> The bigger picture: any new security or observability source we need —
> CrowdStrike, Tenable, Lacework — follows this exact same pattern. Four methods,
> a schemas file, a mock API, and a test file. Onboarding a new source is a day's
> work, not a sprint.
>
> Questions?"

---

## 4. Technical Reference

### The LakeflowConnect Interface Contract

```python
from abc import ABC, abstractmethod
from typing import Iterator
from pyspark.sql.types import StructType

class LakeflowConnect(ABC):

    def __init__(self, options: dict[str, str]) -> None:
        """Receives credentials and config from Unity Catalog connection."""

    @abstractmethod
    def list_tables(self) -> list[str]:
        """Returns all supported table names."""

    @abstractmethod
    def get_table_schema(self, table_name: str, table_options: dict) -> StructType:
        """Returns Spark schema for the given table."""

    @abstractmethod
    def read_table_metadata(self, table_name: str, table_options: dict) -> dict:
        """Returns ingestion_type, primary_keys, cursor_field."""

    @abstractmethod
    def read_table(
        self, table_name: str, start_offset: dict, table_options: dict
    ) -> tuple[Iterator[dict], dict]:
        """Returns (records_iterator, end_offset). Stop when offset == start_offset."""

    def read_table_deletes(self, ...):
        """Optional. Required only for cdc_with_deletes ingestion type."""
```

---

### Ingestion Types

| Type | Description | Cursor field? | Primary keys? |
|------|-------------|:---:|:---:|
| `snapshot` | Full reload every run | No | Yes |
| `cdc` | Incremental — only fetch records changed since last cursor | Yes | Yes |
| `cdc_with_deletes` | CDC + explicit delete tracking | Yes | Yes |
| `append` | Append-only (event logs, audit trails) | Optional | No |

---

### Snyk Connector — Tables at a Glance

| Table | API | Ingestion | Cursor Field | `org_id` required? |
|-------|-----|-----------|-------------|-------------------|
| `organizations` | `GET /v1/orgs` | snapshot | — | No |
| `projects` | `GET /rest/orgs/{org_id}/projects` | snapshot | — | Yes |
| `issues` | `GET /rest/orgs/{org_id}/issues` | **cdc** | `updated_at` | Yes |
| `targets` | `GET /rest/orgs/{org_id}/targets` | snapshot | — | Yes |
| `users` | `GET /rest/orgs/{org_id}/users` | snapshot | — | Yes |
| `vulnerabilities` | `GET /rest/orgs/{org_id}/vulnerabilities` | snapshot | — | Yes |

---

### Wiz Connector — Tables at a Glance

| Table | GraphQL Operation | Ingestion | Cursor Field |
|-------|-------------------|-----------|-------------|
| `issues` | `GetIssues` | **cdc** | `updatedAt` |
| `cloud_resources` | `GetCloudResources` | snapshot | — |
| `vulnerabilities` | `GetVulnerabilities` | **cdc** | `lastDetectedAt` |
| `projects` | `GetProjects` | snapshot | — |
| `users` | `GetUsers` | snapshot | — |
| `controls` | `GetControls` | snapshot | — |

---

### Mock API Design Summary

```
┌─────────────────────────────────────────────────────────────┐
│                     MOCK API PATTERN                        │
├──────────────────┬──────────────────────────────────────────┤
│ Trigger          │ token == "mock"  (Snyk)                  │
│                  │ wiz_client_id == "mock"  (Wiz)           │
├──────────────────┼──────────────────────────────────────────┤
│ What it replaces │ requests.Session  (real HTTP library)    │
├──────────────────┼──────────────────────────────────────────┤
│ Snyk mock        │ Routes URL paths to in-memory data       │
│                  │ Simulates JSON:API + links.next           │
│                  │ PAGE_SIZE=3 → exercises multi-page reads  │
├──────────────────┼──────────────────────────────────────────┤
│ Wiz mock         │ Detects auth vs GraphQL by request body  │
│                  │ Parses operation name via regex           │
│                  │ Returns pageInfo.hasNextPage/endCursor    │
├──────────────────┼──────────────────────────────────────────┤
│ Seeded records   │ Snyk: 1 org, 5 projects, 10 issues,      │
│                  │       5 targets, 5 users, 10 vulns        │
│                  │ Wiz:  8 issues, 6 cloud resources,        │
│                  │       8 vulns, 5 projects, 4 users,       │
│                  │       6 controls                          │
├──────────────────┼──────────────────────────────────────────┤
│ External deps    │ None — runs anywhere, no credentials      │
└──────────────────┴──────────────────────────────────────────┘
```

---

### File Map

```
src/databricks/labs/community_connector/sources/
├── snyk/
│   ├── __init__.py
│   ├── snyk.py                  ← connector implementation
│   ├── snyk_schemas.py          ← TABLE_SCHEMAS, TABLE_METADATA, SUPPORTED_TABLES
│   ├── snyk_mock_api.py         ← in-memory mock (REST/JSON:API)
│   └── connector_spec.yaml      ← UC connection parameter spec
└── wiz/
    ├── __init__.py
    ├── wiz.py                   ← connector implementation
    ├── wiz_schemas.py           ← TABLE_SCHEMAS, TABLE_METADATA, SUPPORTED_TABLES
    ├── wiz_mock_api.py          ← in-memory mock (GraphQL/OAuth2)
    └── connector_spec.yaml      ← UC connection parameter spec

tests/unit/sources/
├── test_suite.py                ← LakeflowConnectTests base harness
├── snyk/
│   ├── __init__.py
│   ├── test_snyk_connector.py   ← test class (3 lines of code)
│   └── configs/
│       ├── dev_config.json      ← {"token": "mock"}
│       └── dev_table_config.json
└── wiz/
    ├── __init__.py
    ├── test_wiz_connector.py    ← test class (3 lines of code)
    └── configs/
        └── dev_config.json      ← {"wiz_client_id": "mock", ...}
```

---

## 5. Live Commands Cheat Sheet

> 💡 **Keep this page open in a separate window during the demo.**

```bash
# Navigate to repo
cd /path/to/lakeflow-community-connectors

# Activate virtual environment
source .venv/bin/activate

# Run Snyk tests only
.venv/bin/pytest tests/unit/sources/snyk/ -v

# Run Wiz tests only
.venv/bin/pytest tests/unit/sources/wiz/ -v

# Run both together (what to run during demo)
.venv/bin/pytest tests/unit/sources/snyk/ tests/unit/sources/wiz/ -v

# Run a single specific test
.venv/bin/pytest tests/unit/sources/snyk/ -k "test_read_table" -v

# Run with short traceback (useful if something fails)
.venv/bin/pytest tests/unit/sources/snyk/ tests/unit/sources/wiz/ -v --tb=short
```

**Expected output:**
```
========================= 14 passed, 14 skipped in 0.20s =========================
```

---

### Config Files (what's in them)

```json
// tests/unit/sources/snyk/configs/dev_config.json
{ "token": "mock" }

// tests/unit/sources/snyk/configs/dev_table_config.json
{
  "issues":          { "org_id": "org-mock-0001" },
  "projects":        { "org_id": "org-mock-0001" },
  "targets":         { "org_id": "org-mock-0001" },
  "users":           { "org_id": "org-mock-0001" },
  "vulnerabilities": { "org_id": "org-mock-0001" }
}

// tests/unit/sources/wiz/configs/dev_config.json
{
  "wiz_client_id": "mock",
  "wiz_client_secret": "mock",
  "wiz_api_endpoint": "https://mock.wiz.io/graphql"
}
```

---

## 6. Expected Questions & Answers

**Q: How do we handle token rotation for Snyk?**
> Credentials live in the Unity Catalog connection object, not in the connector code.
> When the token is rotated in Snyk, you update it in the UC connection — one place,
> no code changes, no redeployment.

**Q: What about multi-org Snyk setups?**
> The `organizations` table gives you the full list of orgs your token has access to.
> For tables like `issues` and `projects`, `org_id` is a per-table option — you can
> configure separate pipeline tables for each org. Multi-org cross-scanning is a
> future enhancement that the `organizations` table already supports.

**Q: Can we add more tables later — e.g. Snyk license issues or Wiz findings?**
> Yes. Each new table is: one entry in `snyk_schemas.py` (schema + metadata) and
> one new `_read_*` method in `snyk.py`. Typically 30–50 lines of code.
> The test harness picks it up automatically — no test code changes.

**Q: What does "pre-bronze" mean exactly? Is this landing in a raw zone?**
> Yes. The connector delivers raw, unmodified records as Python dicts. The framework
> writes them to Delta using the schema we define. No transformations, no business
> logic. Bronze transformations happen downstream in a separate pipeline.

**Q: Why not just use Databricks Partner Connect or a third-party ETL tool?**
> Snyk and Wiz aren't in the partner catalog. Third-party tools (Fivetran, Airbyte)
> do have some coverage but they add cost, another credential surface, and we lose
> control over the ingestion logic. The community connector gives us full ownership
> at a fraction of the complexity.

**Q: How does this compare to what we built with the config-based collector?**
> The config-based approach required us to own the Spark integration, Delta write
> logic, and checkpointing. With lakeflow community connectors, the framework owns
> all of that. We only write the API interaction layer — the 4 methods. It's
> significantly less code to maintain.

**Q: What happens if the Snyk API changes — e.g. a new API version?**
> The API version is a constant in `snyk.py` (`_API_VERSION = "2024-10-15"`).
> Field schema changes would require updating `snyk_schemas.py`. The framework
> handles Delta schema evolution, so additive changes (new columns) won't break
> existing pipelines.

**Q: Why mock instead of a real test environment?**
> Two reasons: (1) we don't want real security credentials in a development or CI
> environment, and (2) tests that depend on live APIs are slow and brittle — they
> break when the API is rate-limited or the data changes. The mock is deterministic,
> instant, and runs anywhere.

**Q: When can we run this in production?**
> The connector code is production-ready. The remaining steps are:
> (1) obtain a real Snyk API token + org UUID,
> (2) create the Unity Catalog connection,
> (3) deploy the pipeline spec.
> Estimated time: half a day.

---

## 7. Post-Demo Follow-Up Template

> Send in the same Slack thread within 1 hour of the demo ending.

```
Thanks everyone for joining! 🙏

Quick recap of what we covered and next steps:

📌 What we showed
• Working Snyk connector — 6 tables, mock API, all tests passing
• Working Wiz connector — 6 tables, GraphQL mock, all tests passing
• Comparison of 3 ingestion approaches (config-based, Lakebase UI, Lakeflow)
• The path from Python connector class → Unity Catalog → Delta table

📂 Resources
• Repo: https://github.com/databrickslabs/lakeflow-community-connectors
• REPO-OVERVIEW.md — full technical reference (in repo root)
• DEMO-GUIDE.md — this summary + all commands (in repo root)

🔜 Next steps
[ ] Obtain real Snyk API token + org UUID → swap mock credentials → run live
[ ] Obtain Wiz client_id + client_secret + API endpoint → run live
[ ] Write README.md for each connector
[ ] Submit to community repo

💬 Questions from the session I'll follow up on:
[ADD ANY UNANSWERED QUESTIONS HERE]

Feel free to drop any follow-up questions here — happy to dig in!
```

---

## Appendix — Key Concepts Glossary

| Term | Definition |
|------|-----------|
| **Pre-bronze layer** | The ingestion mechanism itself — raw data from source systems landed to Delta before any transformation |
| **Bronze layer** | First transformed layer — data is cleaned, typed, and deduplicated but not yet business-logic enriched |
| **Spark PDS** | Spark Python Data Source API — the Databricks framework that powers lakeflow connectors |
| **SDP** | Spark Declarative Pipeline — the pipeline orchestration layer |
| **CDC** | Change Data Capture — incremental ingestion using a cursor field (e.g. `updated_at`) to fetch only new/changed records |
| **Unity Catalog connection** | A secure, centralized credential store in Databricks — connectors read credentials from here at runtime |
| **JSON:API** | A standardized REST response format used by Snyk — wraps records in `{id, type, attributes, relationships}` envelopes |
| **GraphQL** | Query language for APIs used by Wiz — single endpoint, operation-named queries, cursor-based pagination |
| **`links.next`** | Snyk's cursor pagination mechanism — the API embeds the next page URL directly in the response |
| **`pageInfo.endCursor`** | Wiz's cursor pagination — GraphQL convention for cursor-based paging |
| **Ingestion offset** | A dict (e.g. `{"cursor": "2024-03-20T10:00:00Z"}`) that the framework stores after each run and passes back as `start_offset` on the next run |

---

*Document prepared by Sam Adhikari · [DATE] · lakeflow-community-connectors*
