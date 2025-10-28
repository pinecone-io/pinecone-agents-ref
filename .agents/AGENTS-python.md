# Pinecone Python SDK Guide

> **Prerequisites**: See [AGENTS.md](../AGENTS.md) for universal concepts and setup.

This guide provides Python-specific patterns, examples, and best practices for the Pinecone SDK.

## Installation & Setup

### Current API (2025)

```python
from pinecone import Pinecone
```

### Environment Configuration

```python
import os
from pinecone import Pinecone

# Initialize Pinecone client
api_key = os.getenv("PINECONE_API_KEY")
if not api_key:
    raise ValueError("PINECONE_API_KEY environment variable not set")

pc = Pinecone(api_key=api_key)
```

### Production Client Class

```python
class PineconeClient:
    def __init__(self):
        self.api_key = os.getenv("PINECONE_API_KEY")
        if not self.api_key:
            raise ValueError("PINECONE_API_KEY required")
        self.pc = Pinecone(api_key=self.api_key)
        self.index_name = os.getenv("PINECONE_INDEX", "default-index")

    def get_index(self):
        return self.pc.Index(self.index_name)
```

## Quickstarts

### Quick Test

Complete setup prerequisites first, then:

1. **Create index with CLI:**

```bash
pc index create -n agentic-quickstart-test -m cosine -c aws -r us-east-1 --model llama-text-embed-v2 --field_map text=content
```

2. **Upsert sample data:**

```python
from pinecone import Pinecone
import os

# Initialize Pinecone client
api_key = os.getenv("PINECONE_API_KEY")
if not api_key:
    raise ValueError("PINECONE_API_KEY environment variable not set")

pc = Pinecone(api_key=api_key)

records = [
    { "_id": "rec1", "content": "The Eiffel Tower was completed in 1889 and stands in Paris, France.", "category": "history" },
    { "_id": "rec2", "content": "Photosynthesis allows plants to convert sunlight into energy.", "category": "science" },
    { "_id": "rec5", "content": "Shakespeare wrote many famous plays, including Hamlet and Macbeth.", "category": "literature" },
    { "_id": "rec7", "content": "The Great Wall of China was built to protect against invasions.", "category": "history" },
    { "_id": "rec15", "content": "Leonardo da Vinci painted the Mona Lisa.", "category": "art" },
    { "_id": "rec17", "content": "The Pyramids of Giza are among the Seven Wonders of the Ancient World.", "category": "history" },
    { "_id": "rec21", "content": "The Statue of Liberty was a gift from France to the United States.", "category": "history" },
    { "_id": "rec26", "content": "Rome was once the center of a vast empire.", "category": "history" },
    { "_id": "rec33", "content": "The violin is a string instrument commonly used in orchestras.", "category": "music" },
    { "_id": "rec38", "content": "The Taj Mahal is a mausoleum built by Emperor Shah Jahan.", "category": "history" },
    { "_id": "rec48", "content": "Vincent van Gogh painted Starry Night.", "category": "art" },
    { "_id": "rec50", "content": "Renewable energy sources include wind, solar, and hydroelectric power.", "category": "energy" }
]

# Target the index
dense_index = pc.Index("agentic-quickstart-test")

# Upsert the records into a namespace
dense_index.upsert_records("example-namespace", records)
```

3. **Search with reranking:**

```python
import time

# Wait for the upserted vectors to be indexed
time.sleep(10)

# View stats for the index
stats = dense_index.describe_index_stats()
print(stats)

# Define the query
query = "Famous historical structures and monuments"

# Search the dense index and rerank results
reranked_results = dense_index.search(
    namespace="example-namespace",
    query={
        "top_k": 10,
        "inputs": {
            'text': query
        }
    },
    rerank={
        "model": "bge-reranker-v2-m3",
        "top_n": 10,
        "rank_fields": ["content"]
    }
)

# Print the reranked results
for hit in reranked_results['result']['hits']:
    print(f"id: {hit['_id']}, score: {round(hit['_score'], 2)}, text: {hit['fields']['content']}, category: {hit['fields']['category']}")

# Access search results
# IMPORTANT: With reranking, use dict-style access for hit object
for hit in reranked_results.result.hits:
    doc_id = hit["_id"]              # Dict access for id
    score = hit["_score"]            # Dict access for score
    content = hit.fields["content"]  # hit.fields is also a dict
    metadata = hit.fields.get("metadata_field", "")  # Use .get() for optional fields
```

## Data Operations

### Upserting Records

```python
# Indexes with integrated embeddings
records = [
    {
        "_id": "doc1",
        "content": "Your text content here",  # must match field_map
        "category": "documentation",
        "created_at": "2025-01-01",
        "priority": "high"
    }
]

# Always use namespaces
namespace = "user_123"  # e.g., "knowledge_base", "session_456"
index.upsert_records(namespace, records)
```

### Updating Records

```python
# Update existing records (use same upsert operation with existing IDs)
updated_records = [
    {
        "_id": "doc1",  # existing record ID
        "content": "Updated content here",
        "category": "updated_docs",  # can change metadata
        "last_modified": "2025-01-15"
    }
]

# Partial updates - only changed fields need to be included
partial_update = [
    {
        "_id": "doc1",
        "category": "urgent",  # only updating category field
        "priority": "high"     # adding new field
    }
]

index.upsert_records(namespace, updated_records)
```

### Fetching Records

```python
# Fetch single record
result = index.fetch(namespace=namespace, ids=["doc1"])
if result.records:
    record = result.records["doc1"]
    print(f"Content: {record.fields.content}")
    print(f"Metadata: {record.metadata}")

# Fetch multiple records
result = index.fetch(namespace=namespace, ids=["doc1", "doc2", "doc3"])
for record_id, record in result.records.items():
    print(f"ID: {record_id}, Content: {record.fields.content}")

# Fetch with error handling
def safe_fetch(index, namespace, ids):
    try:
        result = index.fetch(namespace=namespace, ids=ids)
        return result.records
    except Exception as e:
        print(f"Fetch failed: {e}")
        return {}
```

### Listing Record IDs

```python
# List all record IDs (paginated)
def list_all_ids(index, namespace, prefix=None):
    """List all record IDs with optional prefix filter"""
    all_ids = []
    pagination_token = None

    while True:
        result = index.list(
            namespace=namespace,
            prefix=prefix,  # filter by ID prefix
            limit=1000,
            pagination_token=pagination_token
        )

        all_ids.extend([record.id for record in result.records])

        if not result.pagination or not result.pagination.next:
            break
        pagination_token = result.pagination.next

    return all_ids

# Usage
all_record_ids = list_all_ids(index, "user_123")
docs_only = list_all_ids(index, "user_123", prefix="doc_")
```

## Search Operations

### Semantic Search with Reranking (Best Practice)

```python
def search_with_rerank(index, namespace, query_text, top_k=5):
    """Standard search pattern - always rerank for production"""
    results = index.search(
        namespace=namespace,
        query={
            "top_k": top_k * 2,  # more candidates for reranking
            "inputs": {
                "text": query_text  # must match index config
            }
        },
        rerank={
            "model": "bge-reranker-v2-m3",
            "top_n": top_k,
            "rank_fields": ["content"]
        }
    )
    return results
```

### Lexical Search

```python
# Basic lexical search
def lexical_search(index, namespace, query_text, top_k=5):
    """Keyword-based search using sparse embeddings"""
    results = index.search(
        namespace=namespace,
        query={
            "inputs": {"text": query_text},
            "top_k": top_k
        }
    )
    return results

# Lexical search with required terms
def lexical_search_with_required_terms(index, namespace, query_text, required_terms, top_k=5):
    """Results must contain specific required words"""
    results = index.search(
        namespace=namespace,
        query={
            "inputs": {"text": query_text},
            "top_k": top_k,
            "match_terms": required_terms  # results must contain these terms
        }
    )
    return results

# Lexical search with reranking
def lexical_search_with_rerank(index, namespace, query_text, top_k=5):
    """Lexical search with reranking for better relevance"""
    results = index.search(
        namespace=namespace,
        query={
            "inputs": {"text": query_text},
            "top_k": top_k * 2  # get more candidates for reranking
        },
        rerank={
            "model": "bge-reranker-v2-m3",
            "top_n": top_k,
            "rank_fields": ["content"]
        }
    )
    return results

# Example usage
search_results = lexical_search_with_required_terms(
    index,
    "knowledge_base",
    "machine learning algorithms neural networks",
    required_terms=["algorithms"]  # must contain "algorithms"
)
```

### Metadata Filtering

```python
# Simple filters
filter_criteria = {"category": "documentation"}

# Complex filters
filter_criteria = {
    "$and": [
        {"category": {"$in": ["docs", "tutorial"]}},
        {"priority": {"$ne": "low"}},
        {"created_at": {"$gte": "2025-01-01"}}
    ]
}

results = index.search(
    namespace=namespace,
    query={
        "top_k": 10,
        "inputs": {"text": query_text},
        "filter": filter_criteria  # Filter goes inside query object
    }
)

# Search without filters - omit the "filter" key
results = index.search(
    namespace=namespace,
    query={
        "top_k": 10,
        "inputs": {"text": query_text}
        # No filter key at all
    }
)

# Dynamic filter pattern - conditionally add filter to query dict
query_dict = {
    "top_k": 10,
    "inputs": {"text": "query"}
}
if has_filters:  # Only add filter if it exists
    query_dict["filter"] = {"category": {"$eq": "docs"}}

results = index.search(namespace=namespace, query=query_dict, rerank={...})
```

## Error Handling (Production)

### Retry Pattern

```python
import time
from pinecone.exceptions import PineconeException

def exponential_backoff_retry(func, max_retries=5):
    for attempt in range(max_retries):
        try:
            return func()
        except PineconeException as e:
            status_code = getattr(e, 'status', None)

            # Only retry transient errors
            if status_code and (status_code >= 500 or status_code == 429):
                if attempt < max_retries - 1:
                    delay = min(2 ** attempt, 60)  # Exponential backoff, cap at 60s
                    time.sleep(delay)
                else:
                    raise
            else:
                raise  # Don't retry client errors (4xx except 429)

# Usage
exponential_backoff_retry(lambda: index.upsert_records(namespace, records))
```

## Batch Processing

```python
def batch_upsert(index, namespace, records, batch_size=96):
    for i in range(0, len(records), batch_size):
        batch = records[i:i + batch_size]
        exponential_backoff_retry(
            lambda: index.upsert_records(namespace, batch)
        )
        time.sleep(0.1)  # Rate limiting
```

## Common Operations

### Index Management

```python
# Check if index exists (in application startup)
if pc.has_index("my-index"):
    index = pc.Index("my-index")

# Get stats (for monitoring/metrics)
stats = index.describe_index_stats()
print(f"Total vectors: {stats.total_vector_count}")
print(f"Namespaces: {list(stats.namespaces.keys())}")
```

### Data Operations

```python
# Fetch records
result = index.fetch(namespace="ns", ids=["doc1", "doc2"])
for record_id, record in result.records.items():
    print(f"{record_id}: {record.fields.content}")

# List all IDs (paginated)
all_ids = []
pagination_token = None
while True:
    result = index.list(namespace="ns", limit=1000, pagination_token=pagination_token)
    all_ids.extend([record.id for record in result.records])
    if not result.pagination or not result.pagination.next:
        break
    pagination_token = result.pagination.next

# Delete records
index.delete(namespace="ns", ids=["doc1", "doc2"])

# Delete entire namespace
index.delete(namespace="ns", delete_all=True)
```

## Python-Specific Patterns

### Namespace Strategy

```python
# Multi-user apps
namespace = f"user_{user_id}"

# Session-based
namespace = f"session_{session_id}"

# Content-based
namespace = "knowledge_base"
namespace = "chat_history"
```

### Environment Configuration

```python
import os
from pinecone import Pinecone

class PineconeClient:
    def __init__(self):
        self.api_key = os.getenv("PINECONE_API_KEY")
        if not self.api_key:
            raise ValueError("PINECONE_API_KEY required")
        self.pc = Pinecone(api_key=self.api_key)
        self.index_name = os.getenv("PINECONE_INDEX", "default-index")

    def get_index(self):
        return self.pc.Index(self.index_name)
```

## Use Case Examples

### Semantic Search System

```python
def build_semantic_search_system():
    """Build a semantic search system with reranking and filtering"""

    # Create search function
    def search_knowledge_base(query, category_filter=None, top_k=5):
        query_dict = {
            "top_k": top_k * 2,
            "inputs": {"text": query}
        }

        if category_filter:
            query_dict["filter"] = {"category": {"$eq": category_filter}}

        results = index.search(
            namespace="knowledge_base",
            query=query_dict,
            rerank={
                "model": "bge-reranker-v2-m3",
                "top_n": top_k,
                "rank_fields": ["content"]
            }
        )

        return results

    return search_knowledge_base
```

### Multi-Tenant RAG System

```python
def build_rag_system():
    """Build a multi-tenant RAG system with namespace isolation"""

    def rag_query(user_id, query, top_k=5):
        # Ensure namespace isolation
        namespace = f"user_{user_id}"

        # Search only user's namespace
        results = index.search(
            namespace=namespace,
            query={
                "top_k": top_k * 2,
                "inputs": {"text": query}
            },
            rerank={
                "model": "bge-reranker-v2-m3",
                "top_n": top_k,
                "rank_fields": ["content"]
            }
        )

        # Construct context for LLM
        context = "\n".join([
            f"Document {hit['_id']}: {hit.fields['content']}"
            for hit in results.result.hits
        ])

        return context

    return rag_query
```

### Recommendation Engine

```python
def build_recommendation_engine():
    """Build a recommendation engine with filtering and diversity"""

    def get_recommendations(product_id, category_filter=None, top_k=10):
        # Get similar products
        results = index.search(
            namespace="products",
            query={
                "top_k": top_k * 2,
                "inputs": {"text": f"product_{product_id}"}
            },
            rerank={
                "model": "bge-reranker-v2-m3",
                "top_n": top_k,
                "rank_fields": ["content"]
            }
        )

        # Apply category filtering if specified
        if category_filter:
            filtered_results = [
                hit for hit in results.result.hits
                if hit.fields.get("category") == category_filter
            ]
            return filtered_results[:top_k]

        return results.result.hits

    return get_recommendations
```
