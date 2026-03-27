# Slide Deck — Pre-Bronze Security Data Ingestion
## Snyk & Wiz via Lakeflow Community Connectors

> **Format:** 6 slides · 30-minute demo · Presenter: Sam Adhikari
> **Tip:** Keep slides on screen only during Blocks 1–3 and Block 6. Switch to live code for Blocks 4–5.

---

## SLIDE 1 — The Problem

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│   HEADLINE (large, centered)                                            │
│                                                                         │
│   Our security data lives in silos.                                     │
│   It's time to bring it into Databricks.                                │
│                                                                         │
├──────────────────────────┬──────────────────────────────────────────────┤
│                          │                                              │
│   LEFT COLUMN            │   RIGHT COLUMN                               │
│   (The Gap Today)        │   (What We Want)                             │
│                          │                                              │
│   🔴  Snyk data          │   ✅  Security data in Delta tables          │
│       lives in Snyk UI   │                                              │
│                          │   ✅  Correlate vulns with data assets       │
│   🔴  Wiz data           │                                              │
│       lives in Wiz UI    │   ✅  Trend risks over time                  │
│                          │                                              │
│   🔴  No cross-source    │   ✅  Unified dashboards & alerts            │
│       correlation        │       in Databricks                          │
│                          │                                              │
│   🔴  No historical      │   ✅  Scheduled, auditable,                  │
│       trending           │       incremental ingestion                  │
│                          │                                              │
└──────────────────────────┴──────────────────────────────────────────────┘
│  FOOTER: Snyk = code vulnerability scanning  ·  Wiz = cloud risk mgmt  │
└─────────────────────────────────────────────────────────────────────────┘
```

**Visual suggestion:** Red/green color split. Left column has light red background, right has light green. Simple icons: lock, shield, chart.

**Speaker notes:**
> "Our security team uses two tools. Snyk scans our code repositories for
> vulnerabilities. Wiz monitors our cloud infrastructure for risks and misconfigs.
> Both tools have rich, actionable data — but today it's trapped in their UIs.
>
> We can't join security findings with our data pipeline metadata. We can't see
> whether a vulnerable package is actually used in a production pipeline. We can't
> trend our risk posture over time. And we can't alert on security regressions from
> inside Databricks.
>
> This demo shows how we fix that."

**Time on slide:** 1.5 minutes

---

## SLIDE 2 — Three Approaches, One Clear Choice

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│   HEADLINE                                                              │
│   We evaluated 3 ingestion approaches.                                  │
│   Here's why Lakeflow Community Connectors wins.                        │
│                                                                         │
├───────────────────┬───────────────────────┬─────────────────────────────┤
│                   │                       │                             │
│  Config-based     │    Lakebase UI        │  Lakeflow Community  ✅     │
│  Metadata         │                       │  Connectors                 │
│  Collector        │                       │                             │
├───────────────────┼───────────────────────┼─────────────────────────────┤
│                   │                       │                             │
│  ✅ Flexible      │  ✅ Fast to set up    │  ✅ Flexible                │
│                   │                       │                             │
│  ❌ We own all    │  ❌ Bounded by        │  ✅ Standardized            │
│     the plumbing  │     what UI exposes   │                             │
│                   │                       │  ✅ Fully testable          │
│  ❌ Hard to test  │  ❌ Hard to test      │                             │
│                   │                       │  ✅ Open source /           │
│  ❌ Bespoke per   │  ❌ Snyk + Wiz don't │     Databricks-backed       │
│     source        │     fit the catalog   │                             │
│                   │                       │  ✅ Framework owns          │
│  Best for:        │  Best for:            │     Spark, Delta, CDC       │
│  One-off sources  │  Standard catalog     │                             │
│                   │  sources              │  Best for: New community    │
│                   │                       │  sources like Snyk + Wiz    │
│                   │                       │                             │
└───────────────────┴───────────────────────┴─────────────────────────────┘
```

**Visual suggestion:** Three columns. Left two columns have neutral/grey background. Right column (Lakeflow) has brand blue background with white text and a checkmark badge in the top corner.

**Speaker notes:**
> "Before building anything, I evaluated three paths.
>
> The config-based metadata collector gave us full flexibility but we ended up
> owning everything — the Spark integration, Delta writes, checkpointing. Every
> new source was its own engineering project.
>
> The Lakebase UI is great for sources already in the Databricks partner catalog,
> but Snyk and Wiz are not standard catalog sources. The UI can't express the
> custom pagination and auth logic they need.
>
> Lakeflow Community Connectors is the right fit. It's an open-source framework
> from Databricks Labs. We implement a 4-method Python interface — and the
> framework handles all the Spark, Delta, CDC, and pipeline machinery underneath.
> We own the API interaction layer. Databricks owns the rest."

**Time on slide:** 3 minutes

---

## SLIDE 3 — How Lakeflow Community Connectors Works

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│   HEADLINE                                                              │
│   You implement 4 methods.                                              │
│   The framework handles everything else.                                │
│                                                                         │
├───────────────────────────────────┬─────────────────────────────────────┤
│                                   │                                     │
│   YOUR CODE (4 methods)           │   FRAMEWORK HANDLES                 │
│                                   │                                     │
│   list_tables()                   │   ⚡  Spark Python Data Source      │
│   → what tables exist?            │                                     │
│                                   │   📦  Delta table writes            │
│   get_table_schema()              │                                     │
│   → what does each table          │   🔄  CDC checkpointing             │
│     look like?                    │       (no duplicate records)        │
│                                   │                                     │
│   read_table_metadata()           │   📐  Schema evolution              │
│   → snapshot or CDC?              │                                     │
│      primary keys?                │   🗓  Scheduled pipeline triggers   │
│      cursor field?                │                                     │
│                                   │   🔐  Unity Catalog credentials     │
│   read_table()                    │                                     │
│   → give me records,              │                                     │
│     paginated, with               │                                     │
│     an offset                     │                                     │
│                                   │                                     │
├───────────────────────────────────┴─────────────────────────────────────┤
│                                                                         │
│   snapshot = full reload every run                                      │
│   cdc      = only fetch records changed since last cursor               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Visual suggestion:** Two-panel layout. Left panel is white with clean code-style bullets. Right panel is dark (dark blue/slate) with white icons and text — the "framework magic" side. A vertical dividing line with a small lightning bolt icon at the midpoint.

**Speaker notes:**
> "Here's the contract we implement. Four methods — that's it.
>
> list_tables tells the framework what tables this source has.
> get_table_schema returns a Spark StructType for each table — this is what
> gets used when writing to Delta.
> read_table_metadata tells the framework whether to do a full reload or an
> incremental CDC read, and which field to use as the cursor.
> read_table is the actual data fetch — paginated, returning records and an
> offset dict so the framework knows where to resume next time.
>
> On the right is everything we don't write. Spark wiring, Delta upserts,
> checkpointing so we never re-ingest the same record, schema evolution when
> fields change, and scheduled pipeline triggers. The framework owns all of that.
>
> The bottom two terms are key: snapshot means reload the whole table every run —
> good for things like users or projects that don't change often. CDC means we
> track a cursor — like updated_at — and only pull what's new or changed since
> the last run."

**Time on slide:** 4 minutes

---

## SLIDE 4 — What We Built

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│   HEADLINE                                                              │
│   Two connectors. 12 tables. Zero external dependencies for testing.   │
│                                                                         │
├──────────────────────────────┬──────────────────────────────────────────┤
│                              │                                          │
│   🐍 SNYK CONNECTOR          │   ☁️  WIZ CONNECTOR                     │
│   REST / JSON:API            │   GraphQL / OAuth2                       │
│                              │                                          │
├──────────────────────────────┼──────────────────────────────────────────┤
│                              │                                          │
│  Table            Type       │  Table              Type                 │
│  ─────────────────────────   │  ──────────────────────────────          │
│  organizations    snapshot   │  issues             CDC ↺                │
│  projects         snapshot   │  cloud_resources    snapshot             │
│  issues           CDC ↺      │  vulnerabilities    CDC ↺                │
│  vulnerabilities  snapshot   │  projects           snapshot             │
│  targets          snapshot   │  users              snapshot             │
│  users            snapshot   │  controls           snapshot             │
│                              │                                          │
├──────────────────────────────┴──────────────────────────────────────────┤
│                                                                         │
│  ↺ CDC = incremental reads via cursor field — no full reloads           │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   💡  MOCK API STRATEGY                                                 │
│   No real credentials needed · Runs in CI · Tests are deterministic    │
│                                                                         │
│   token = "mock"  →  SnykMockSession  (in-memory REST/JSON:API)        │
│   client_id = "mock"  →  WizMockSession  (in-memory GraphQL/OAuth2)    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Visual suggestion:** Top half split into two equal columns — Snyk on left (orange accent), Wiz on right (blue accent). Each has a logo placeholder. CDC rows get a small green "↺" badge. Bottom strip spans full width in a light yellow/cream — the mock API highlight box.

**Speaker notes:**
> "Here's what we built. Two connectors, 12 tables across both sources.
>
> Snyk uses a REST API in JSON:API format — everything is wrapped in an
> id/type/attributes/relationships envelope. Our connector flattens that into
> plain records.
>
> Wiz uses a GraphQL API with OAuth2 authentication. The connector handles
> token acquisition and refresh automatically — tokens are cached and reused
> until they're about to expire.
>
> The CDC tables are the important ones for freshness. Snyk issues and Wiz
> issues both support a cursor field — we only pull what's changed since the
> last run. No full table reloads for those.
>
> The bottom box is the part I'll show in the live demo. Both connectors have
> a built-in mock mode. Set the token to the string 'mock' — the connector
> swaps in an in-memory session that simulates real API responses, pagination,
> and CDC filtering. Zero external calls. I'll show this live now."

**Time on slide:** 2 minutes (then switch to live code)

---

## SLIDE 5 — Test Results

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│   HEADLINE                                                              │
│   14 tests. 0 external calls. Runs in under a second.                  │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   $ pytest tests/unit/sources/snyk/ tests/unit/sources/wiz/ -v         │
│                                                                         │
├────────────────────────────────────────┬────────────────────────────────┤
│                                        │                                │
│  TEST                                  │  WHAT IT VALIDATES             │
│  ──────────────────────────────────    │  ──────────────────────────    │
│  ✅ test_initialization                │  Connector boots + auth works  │
│  ✅ test_list_tables                   │  All 6 tables returned         │
│  ✅ test_invalid_table_name            │  Raises on unknown table       │
│  ✅ test_get_table_schema              │  Valid Spark schema per table  │
│  ✅ test_read_table_metadata           │  CDC/snapshot + keys valid     │
│  ✅ test_read_table                    │  Records fetched + parsed      │
│  ✅ test_micro_batch_offset_contract   │  Offset round-trip correct     │
│                                        │                                │
│  ⏭  7 skipped (expected)              │  Write-back — APIs read-only   │
│                                        │                                │
├────────────────────────────────────────┴────────────────────────────────┤
│                                                                         │
│      14 passed   ·   14 skipped   ·   0 failed   ·   0.20s             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Visual suggestion:** Dark terminal-style background for the pytest command line at the top. Main content area is white with a clean two-column table. Bottom bar is bold green with white text showing the final count. Green checkmarks on passing tests.

**Speaker notes:**
> "Here are the results you just saw in the terminal.
>
> Seven core tests run against each connector — fourteen total. Every one passes.
>
> The most important test is micro_batch_offset_contract. This simulates what the
> framework does in production: call read_table, get records and an offset, then
> call read_table again passing that offset back in. The connector must handle
> receiving its own previously-returned offset without re-fetching records. If this
> test passes, the connector is safe for incremental pipeline use.
>
> The 14 skipped tests are write-back tests — they require a test_utils class that
> can write records to the source system. Both Snyk and Wiz are read-only APIs,
> so these are correctly and intentionally skipped.
>
> No mocking libraries. No patching. The mock API is a real in-memory
> implementation that exercises every code path the real API would hit."

**Time on slide:** 2 minutes (after live demo, before wrap-up)

---

## SLIDE 6 — What's Next

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│   HEADLINE                                                              │
│   From mock to production: one config swap.                             │
│   From two connectors to many: one proven pattern.                     │
│                                                                         │
├──────────────────────────────┬──────────────────────────────────────────┤
│                              │                                          │
│   🚀 PATH TO PRODUCTION      │   🔭 BIGGER PICTURE                     │
│                              │                                          │
│   1. Obtain Snyk API token   │   Any new security source follows        │
│      + org UUID              │   the same 4-method pattern:             │
│                              │                                          │
│   2. Obtain Wiz client_id    │   CrowdStrike    ~1 day                  │
│      + client_secret         │   Tenable        ~1 day                  │
│      + API endpoint          │   Lacework        ~1 day                 │
│                              │   Qualys          ~1 day                 │
│   3. Create Unity Catalog    │                                          │
│      connection object       │   4 methods + schemas file               │
│                              │   + mock API + test file                 │
│   4. Deploy pipeline spec    │   = production-ready connector           │
│                              │                                          │
│   5. Data flows to Delta ✅  │                                          │
│                              │                                          │
├──────────────────────────────┴──────────────────────────────────────────┤
│                                                                         │
│   📋 OPEN ITEMS                                                         │
│                                                                         │
│   • README.md for Snyk and Wiz connectors                              │
│   • Live API validation (real credentials)                              │
│   • Submit to Databricks Labs community repo                            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Visual suggestion:** Left column has a numbered step-list in a clean card style with a rocket icon at top. Right column has a "ripple" or "expand" visual — shows the pattern spreading to new sources. Bottom strip is a light blue to-do checklist section.

**Speaker notes:**
> "So what does it take to go from what I showed today to production data in Delta?
>
> Five steps. Get real credentials for each tool, create a Unity Catalog connection
> — which is just Databricks' secure credential store — and deploy the pipeline
> spec. That's it. The connector code doesn't change at all. It's a config swap.
> Estimated time: half a day per connector.
>
> The bigger picture is what I want to leave you with. We now have a proven,
> tested pattern for ingesting data from any security or observability tool.
> CrowdStrike, Tenable, Lacework — any of these would follow the exact same
> structure. Four methods, a schemas file, a mock API, a test file.
> A new connector is a day's work, not a sprint.
>
> The open items are the natural next steps: write README docs for each connector,
> validate against the live APIs once we have credentials, and submit to the
> community repo so other Databricks customers can use this too.
>
> I'll open it up for questions now."

**Time on slide:** 3 minutes

---

## Slide Flow Summary

```
SLIDE 1          SLIDE 2          SLIDE 3          SLIDE 4
The Problem  →   3 Approaches →   Architecture →   What We Built
(1.5 min)        (3 min)          (4 min)          (2 min)
                                                        │
                                                        ▼
                                                   [LIVE CODE]
                                                   [LIVE TESTS]
                                                   (14 min)
                                                        │
                                                        ▼
SLIDE 6          SLIDE 5
What's Next  ←   Test Results
(3 min)          (2 min)
```

---

## Design Notes (for PowerPoint / Google Slides)

| Element | Recommendation |
|---------|---------------|
| **Font** | Inter or Roboto — clean, technical |
| **Primary color** | Databricks red `#FF3621` or brand blue `#1B3A4B` |
| **Code blocks** | Dark background `#1E1E1E`, monospace font, syntax highlight |
| **Accent — passed tests** | Green `#22C55E` |
| **Accent — CDC tables** | Blue `#3B82F6` |
| **Accent — problems/gaps** | Red `#EF4444` |
| **Max bullets per slide** | 6 — if you need more, split the slide |
| **Slide size** | 16:9 widescreen |
| **Title size** | 36–40pt |
| **Body text** | 18–22pt — readable on a shared screen |
| **Footer** | Slide number + "Sam Adhikari · [DATE]" |

---

## Quick Reference — What to Have Open Before the Call

```
Window 1:  Slide deck (present from here)
Window 2:  VS Code / Cursor
           - sources/snyk/snyk.py
           - sources/snyk/snyk_schemas.py
           - sources/snyk/snyk_mock_api.py
           - sources/wiz/wiz_mock_api.py
           - tests/unit/sources/snyk/test_snyk_connector.py
Window 3:  Terminal (pre-navigated to repo root, venv activated)
```

**The one line to remember:**
> *"We implement 4 methods in Python. The framework handles Spark, Delta, CDC, and scheduling. That's the whole story."*

---

*Slide deck content prepared by Sam Adhikari · [DATE]*
*Technical reference: DEMO-GUIDE.md · REPO-OVERVIEW.md*
