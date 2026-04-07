# Databricks notebook source
# MAGIC %md
# MAGIC # Snyk — Lakewatch-native **Bronze** only
# MAGIC
# MAGIC Reads Lakeflow staging (`cyber_prod.snyk.events`) and writes **`cyber_prod.bronze.snyk_events`**
# MAGIC in the same shape as Lakewatch bronze tables (e.g. `internal_kong`):
# MAGIC
# MAGIC | Column | Type | Notes |
# MAGIC |--------|------|-------|
# MAGIC | `lw_id` | string | SHA-256(`id` \| `modification_time`) dedup key |
# MAGIC | `time` | timestamp | From JSON `modification_time` (aligned with `_raw`) |
# MAGIC | `team_id` | string | Snyk `org` (tenant scope; parallels Kong `team_id`) |
# MAGIC | `data` | variant | Full finding JSON as VARIANT (same payload as `_raw`) |
# MAGIC | `_raw` | variant | Full finding JSON as VARIANT |
# MAGIC | `_metadata` | struct | Autoloader-style: `file_path`, `file_name`, `file_size`, `file_block_*`, `file_modification_time` |
# MAGIC | `ingest_time_utc` | timestamp | Pipeline ingest time |
# MAGIC
# MAGIC **Silver / gold:** Use a separate preset pipeline or jobs to flatten `_raw` to Delta columns and map to OCSF.
# MAGIC **Lakewatch / DASL:** use `demo/snyk_events_preset.yaml` with `dasl_client.preset_development` to model silver/gold from this bronze.
# MAGIC
# MAGIC **Prerequisites:** `cyber_prod.snyk.events` from `snyk_bronze_pipeline`; schema `cyber_prod.bronze` exists.

# COMMAND ----------

import dlt
from pyspark.sql import functions as F
from pyspark.sql.types import LongType, StringType, TimestampType

_SOURCE = "cyber_prod.snyk.events"
_BRONZE_TABLE = "cyber_prod.bronze.snyk_events"

# COMMAND ----------
# MAGIC %md ## Bronze — `cyber_prod.bronze.snyk_events`

# COMMAND ----------


@dlt.table(
    name=_BRONZE_TABLE,
    comment=(
        "Lakewatch-native bronze (internal_kong-style): lw_id, time, team_id, data, _raw, "
        "_metadata, ingest_time_utc."
    ),
    table_properties={"quality": "bronze"},
)
@dlt.expect_or_drop("valid_lw_id", "lw_id IS NOT NULL")
def bronze_snyk_events():
    src = spark.table(_SOURCE)
    json_row = F.to_json(F.struct("*"))
    raw_variant = F.parse_json(json_row)
    return src.select(
        F.sha2(
            F.concat_ws("|", F.col("id"), F.coalesce(F.col("modification_time"), F.lit(""))),
            256,
        ).alias("lw_id"),
        F.to_timestamp(F.get_json_object(json_row, "$.modification_time")).alias("time"),
        F.col("org").cast(StringType()).alias("team_id"),
        raw_variant.alias("data"),
        raw_variant.alias("_raw"),
        F.struct(
            F.lit("snyk://snyk-faker-dev.noop.app/api/events")
            .cast(StringType())
            .alias("file_path"),
            F.lit("snyk_events").cast(StringType()).alias("file_name"),
            F.lit(0).cast(LongType()).alias("file_size"),
            F.lit(0).cast(LongType()).alias("file_block_start"),
            F.lit(0).cast(LongType()).alias("file_block_length"),
            F.current_timestamp().cast(TimestampType()).alias("file_modification_time"),
        ).alias("_metadata"),
        F.current_timestamp().cast(TimestampType()).alias("ingest_time_utc"),
    )
