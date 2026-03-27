---
name: data-engineering-ai
description: "Unified data engineering skill. Covers batch/streaming pipelines, data warehousing, dbt transformations, Airflow DAGs, vector databases, and embedding strategies for RAG and semantic search."
risk: safe
source: self
tags: "[data-engineering, dbt, airflow, vector-db, embeddings, rag, pipeline, spark]"
date_added: "2026-03-27"
triggers: data pipeline, ETL, ELT, dbt, Airflow, DAG, Spark, data warehouse, lakehouse, vector database, Pinecone, Weaviate, Qdrant, pgvector, embedding, RAG, semantic search, Kafka, streaming, data quality
---

# Data Engineering & AI Data

Unified dispatcher for all data engineering and AI data work.
Replaces: `data-engineer`, `dbt-transformation-patterns`, `airflow-dag-patterns`, `vector-database-engineer`, `embedding-strategies`.

## ⚡ Decision Tree — What are you building?

### 1. Data pipeline architecture

**Batch vs Streaming decision:**
- Batch: SLA > 1 hour, cost sensitivity, analytical workloads → dbt + Airflow
- Micro-batch: SLA 1–60 min, near-real-time → Spark Structured Streaming
- Streaming: SLA < 1 min, real-time events → Kafka + Flink / Kafka Streams

**Storage layer:**
- Warehouse (structured, BI): BigQuery · Snowflake · Redshift
- Lakehouse (mixed, ML-ready): Delta Lake · Apache Iceberg · Apache Hudi
- Operational store: PostgreSQL · DynamoDB

**Checklist before implementation:**
- [ ] Source schemas and SLAs defined
- [ ] Data contracts agreed with upstream teams
- [ ] PII identified and access controls planned
- [ ] Idempotency strategy for reruns

Safety rules: validate data before writing to production sinks · protect PII · enforce least-privilege access.

### 2. dbt transformations

Structure:
```
models/
  staging/      # raw → typed, renamed, deduplicated (1:1 with source)
  intermediate/ # joins, business logic
  marts/        # final analytical tables (one per use case)
```

Rules:
- Staging models: one source file per source system, no joins
- All models have `description:` in `schema.yml`
- Use `ref()` for model dependencies, `source()` for raw sources
- Required tests per model: `unique` + `not_null` on primary keys
- Use incremental models for tables > 10M rows

```sql
-- models/marts/orders.sql
{{ config(materialized='incremental', unique_key='order_id') }}

SELECT
    o.order_id,
    o.customer_id,
    SUM(i.amount) AS total_amount,
    o.created_at
FROM {{ ref('stg_orders') }} o
JOIN {{ ref('stg_order_items') }} i USING (order_id)
{% if is_incremental() %}
WHERE o.created_at > (SELECT MAX(created_at) FROM {{ this }})
{% endif %}
GROUP BY 1, 2, 4
```

### 3. Airflow DAGs

Structure every DAG with:
```python
from airflow.decorators import dag, task
from datetime import datetime, timedelta

@dag(
    schedule="0 6 * * *",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    default_args={"retries": 2, "retry_delay": timedelta(minutes=5)},
    tags=["etl", "orders"],
)
def orders_pipeline():
    @task()
    def extract() -> list[dict]: ...

    @task()
    def transform(data: list[dict]) -> list[dict]: ...

    @task()
    def load(data: list[dict]) -> None: ...

    load(transform(extract()))
```

Rules:
- Use `@dag` / `@task` decorators (TaskFlow API) over classic operators where possible
- Set `catchup=False` unless backfilling is intentional
- Use `retries` + `retry_delay` on all production DAGs
- Idempotent tasks: safe to re-run without duplicating data
- Use `XCom` only for small metadata; pass large data via object storage
- Test DAGs: `pytest` with `dag.test()` in a local environment

### 4. Vector databases (semantic search / RAG)

**Technology selection:**

| Need | Best Choice |
|------|-------------|
| Managed, simple API | Pinecone |
| Self-hosted, rich filtering | Qdrant |
| GraphQL + multimodal | Weaviate |
| PostgreSQL stack | pgvector |
| Large-scale open-source | Milvus |

**Implementation pattern:**
```python
# Chunk → Embed → Store → Retrieve
chunks = chunk_document(doc, size=512, overlap=50)
embeddings = embed_batch(chunks, model="text-embedding-3-large")
index.upsert(vectors=zip(ids, embeddings, metadatas))

# Query
query_vec = embed(user_query)
results = index.query(vector=query_vec, top_k=5, filter={"domain": "physics"})
```

Index types: HNSW (best recall, high memory) · IVF (scalable, lower recall) · PQ (compressed, fast).

Always implement hybrid search (vector + keyword BM25) for production RAG.

### 5. Embedding strategies

**Model selection:**

| Model | Dimensions | Best For |
|-------|------------|----------|
| text-embedding-3-large | 3072 | High accuracy (English) |
| text-embedding-3-small | 1536 | Speed + cost |
| multilingual-e5-large | 1024 | Multilingual (e.g., German content) |
| bge-m3 | 1024 | Open-source multilingual |

**Chunking strategy:**
- Fixed-size: simple, predictable; use for homogeneous content
- Sentence/paragraph: better semantic coherence; use for prose
- Recursive character splitting: good default for mixed content
- Overlap: 10–20% of chunk size to preserve context at boundaries

**For this project (German text):** use `multilingual-e5-large` or `bge-m3` for Markdown-docs/ content.

## Do not use this skill when
- You only need exploratory data analysis without pipelines
- You are doing ML model training (not data serving)
- The task is pure SQL without orchestration or transformation tooling
