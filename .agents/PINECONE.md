# Pinecone Universal Agent Guide

> **Official docs**: [https://docs.pinecone.io/](https://docs.pinecone.io/) - For complete API reference, advanced features, and detailed guides.

This guide covers critical gotchas, best practices, and common patterns for Pinecone across multiple programming languages. For language-specific examples and patterns, see the appropriate language file below.

## Choosing the Right Guide

Based on what the user is asking, consult these guides:

### Getting Started

- **User wants to learn Pinecone** → [PINECONE-quickstart.md](./PINECONE-quickstart.md)
- **User needs a specific use case** → [PINECONE-quickstart.md](./PINECONE-quickstart.md) (then link to language-specific examples)

### Installation & Setup

- **CLI installation/usage** → [PINECONE-cli.md](./PINECONE-cli.md)
- **SDK installation by language**:
  - Python → [PINECONE-python.md](./PINECONE-python.md#installation--setup)
  - TypeScript/Node.js → [PINECONE-typescript.md](./PINECONE-typescript.md#installation--setup)
  - Go → [PINECONE-go.md](./PINECONE-go.md#installation--setup)
  - Java → [PINECONE-java.md](./PINECONE-java.md#installation--setup)

### Implementation

- **Building features in Python** → [PINECONE-python.md](./PINECONE-python.md)
- **Building features in TypeScript/Node.js** → [PINECONE-typescript.md](./PINECONE-typescript.md)
- **Building features in Go** → [PINECONE-go.md](./PINECONE-go.md)
- **Building features in Java** → [PINECONE-java.md](./PINECONE-java.md)

### Universal Concepts

- **Use this file** for CLI vs SDK guidance, common mistakes, constraints, error handling
- **Language-specific info** → See language-specific files above

## Language Detection

Determine the primary programming language by checking for these files:

- **`package.json`** → TypeScript/Node.js (see [PINECONE-typescript.md](./PINECONE-typescript.md))
- **`requirements.txt` or `pyproject.toml`** → Python (see [PINECONE-python.md](./PINECONE-python.md))
- **`pom.xml` or `build.gradle`** → Java (see [PINECONE-java.md](./PINECONE-java.md))
- **`go.mod`** → Go (see [PINECONE-go.md](./PINECONE-go.md))
- **Default fallback** → Python (see [PINECONE-python.md](./PINECONE-python.md))

## Universal Concepts (All Languages)

### ⚠️ Critical: Installation & SDK

> **Before installing anything**: ALWAYS verify if CLI/SDK is already installed before asking users to install or update:
>
> - **CLI**: Run `pc version` - only install if command fails
> - **SDK**: Check package files or use language-specific verification commands
> - Only prompt for installation when verification shows it's missing

**ALWAYS use the current SDK:**

- **Python**: `pip install pinecone` (not `pinecone-client`)
- **TypeScript**: `npm install @pinecone-database/pinecone`
- **Java**: Add to `pom.xml` or `build.gradle`
- **Go**: `go get github.com/pinecone-io/go-pinecone/pinecone`

### 🔧 CLI vs SDK: When to Use Which

**Use the Pinecone CLI for one-time or automated administrative tasks:**

- ✅ **Creating indexes** - `pc index create`
- ✅ **Deleting indexes** - `pc index delete`
- ✅ **Configuring indexes** - `pc index configure` (replicas, deletion protection)
- ✅ **Listing indexes** - `pc index list`
- ✅ **Describing indexes** - `pc index describe`
- ✅ **Creating API keys** - `pc api-key create`
- ✅ **One-off inspection** - Checking stats, configuration
- ✅ **Automated deployment pipelines** - All initial infrastructure setup

**Use the SDK for application code:**

- ✅ **Ensuring index existence and correctness** - Creating/updating indexes as part of application startup
- ✅ **Dynamic index management** - based on application's logic and requirements
- ✅ **Vector operations** - upsert, query, search, delete vectors
- ✅ **Records operations** - upsert, query, search, delete RECORDS (automatic embeddings generation)
- ✅ **Other services** - explicit embeddings generation, reranking, etc.
- ✅ **Unit and integration tests**

## CLI Setup and Usage

For detailed CLI installation, authentication, and command reference, see [PINECONE-cli.md](./PINECONE-cli.md).

## Index Creation

> **⚠️ Use CLI (`pc index create`), NOT SDK in application code. See [PINECONE-cli.md](./PINECONE-cli.md) for detailed commands.**

### Available embedding models (current)

- `llama-text-embed-v2`: High-performance, configurable dimensions, recommended for most use cases
- `multilingual-e5-large`: For multilingual content, 1024 dimensions
- `pinecone-sparse-english-v0`: For keyword/hybrid search scenarios

## Data Operations

### Upserting records (text with integrated embeddings)

**Always use namespaces for data isolation:**

- Multi-user apps: `user_123`
- Session-based: `session_456`
- Content-based: `knowledge_base`, `chat_history`

### Updating records

Use the same upsert operation with existing IDs. Only changed fields need to be included for partial updates.

### Fetching records

Use the fetch method with namespace and record IDs. Always handle errors gracefully.

### Listing record IDs

Use paginated listing with optional prefix filters for efficient ID retrieval.

## Search Operations

### Semantic search with reranking (best practice)

**Always rerank for production quality:**

- Get 2x candidates initially
- Rerank with `bge-reranker-v2-m3` model
- Return final count

### Lexical search (keyword-based)

Use for exact keyword matching with optional required terms and reranking.

### Metadata filtering

**Supported filter operators:**

- `$eq`: equals
- `$ne`: not equals
- `$gt`, `$gte`: greater than, greater than or equal
- `$lt`, `$lte`: less than, less than or equal
- `$in`: in list
- `$nin`: not in list
- `$exists`: field exists
- `$and`, `$or`: logical operators

## 🚨 Common Mistakes (Must Avoid)

### 1. **Nested Metadata** (will cause API errors)

- ❌ Nested objects not allowed
- ✅ Flat structure only
- ✅ String lists are OK

### 2. **Batch Size Limits** (will cause API errors)

- Text records: MAX 96 per batch, 2MB total
- Vector records: MAX 1000 per batch, 2MB total

### 3. **Missing Namespaces** (causes data isolation issues)

- ❌ No namespace
- ✅ Always use namespaces

### 4. **Skipping Reranking** (reduces search quality)

- ⚠️ OK but not optimal
- ✅ Always rerank in production

### 5. **Hardcoded API Keys**

- ❌ Hardcoded keys
- ✅ Use environment variables

## Key Constraints

| Constraint          | Limit                                      | Notes                             |
| ------------------- | ------------------------------------------ | --------------------------------- |
| Metadata per record | 40KB                                       | Flat JSON only, no nested objects |
| Text batch size     | 96 records                                 | Also 2MB total per batch          |
| Vector batch size   | 1000 records                               | Also 2MB total per batch          |
| Query response size | 4MB                                        | Per query response                |
| Metadata types      | strings, ints, floats, bools, string lists | No nested structures              |
| Consistency         | Eventually consistent                      | Wait ~1-5s after upsert           |

## Error Handling (Production)

### Error Types

- **4xx (client errors)**: Fix your request - DON'T retry (except 429)
- **429 (rate limit)**: Retry with exponential backoff
- **5xx (server errors)**: Retry with exponential backoff

### Retry Pattern

Implement exponential backoff with max retries for transient errors only.

## Use Cases

### Search

Build a semantic search system that returns ranked results from your knowledge base. Ideal for search interfaces where users need relevant documents with confidence scores.

### RAG

Build a multi-tenant RAG (Retrieval-Augmented Generation) system that retrieves relevant context per tenant and feeds it to an LLM. Each tenant has isolated data stored in separate Pinecone namespaces.

### Recommendations

Build a recommendation engine that suggests similar items based on semantic similarity. Ideal for e-commerce, content platforms, and user personalization systems.

## Quick Troubleshooting

| Issue                                | Solution                                                     |
| ------------------------------------ | ------------------------------------------------------------ |
| `ModuleNotFoundError: pinecone.grpc` | Wrong SDK - reinstall with correct package                   |
| `Metadata too large` error           | Check 40KB limit, flatten nested objects                     |
| `Batch too large` error              | Reduce to 96 records (text) or 1000 (vectors)                |
| Search returns no results            | Check namespace, wait for indexing (~5s), verify data exists |
| Rate limit (429) errors              | Implement exponential backoff, reduce request rate           |
| Nested metadata error                | Flatten all metadata - no nested objects allowed             |

## Official Documentation Resources

For advanced features not covered in this quick reference:

- **API reference**: [https://docs.pinecone.io/reference/api/introduction](https://docs.pinecone.io/reference/api/introduction)
- **Bulk imports** (S3/GCS): [https://docs.pinecone.io/guides/index-data/import-data](https://docs.pinecone.io/guides/index-data/import-data)
- **Hybrid search**: [https://docs.pinecone.io/guides/search/hybrid-search](https://docs.pinecone.io/guides/search/hybrid-search)
- **Error handling**: [https://docs.pinecone.io/guides/production/error-handling](https://docs.pinecone.io/guides/production/error-handling)
- **Database limits**: [https://docs.pinecone.io/reference/api/database-limits](https://docs.pinecone.io/reference/api/database-limits)

**Remember**: Always use namespaces, always rerank, always handle errors with retry logic.
