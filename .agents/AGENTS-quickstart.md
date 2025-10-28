# Pinecone Quickstart Guide

> **Prerequisites**: See [AGENTS.md](../AGENTS.md) for universal concepts and setup.

> **Important for all quickstarts**: Execute all steps completely. Keep setup minimal (directories, virtual environments, dependencies only). Do not expect the user to satisfy any prerequisites except providing API keys. For summaries, use only README.md and SUMMARY.md.

This guide provides step-by-step instructions for building your first Pinecone applications. Choose your programming language below to see examples.

## Choosing Your Quickstart

When you are asked to help get started with Pinecone:

1. **Detect or ask for programming language**:

   - Check project files for: `package.json` (JavaScript/TypeScript), `requirements.txt` or `pyproject.toml` (Python), `pom.xml` or `build.gradle` (Java), `go.mod` (Go)
   - If no language can be determined, ask the user which language they prefer

2. **Ask the user to choose a quickstart option**:

   - **Quick Test**: Create an index, upsert data, and perform semantic search.
   - **Use Case**:
     - **Search**: Build a semantic search system that returns ranked results from your knowledge base. This pattern is ideal for search interfaces where users need a list of relevant documents with confidence scores.
     - **RAG**: Build a multi-tenant RAG (Retrieval-Augmented Generation) system that retrieves relevant context per tenant and feeds it to an LLM to generate answers. Each tenant (organization, workspace, or user) has isolated data stored in separate Pinecone namespaces. This pattern is ideal for knowledge bases, customer support platforms, and collaborative workspaces.
     - **Recommendations**: Build a recommendation engine that suggests similar items based on semantic similarity. This pattern is ideal for e-commerce, content platforms, and user personalization systems.

3. **Based on the choices, use the appropriate language-specific pattern below.**

## Language-Specific Quickstarts

- **Python**: See [AGENTS-python.md](./AGENTS-python.md#quickstarts)
- **TypeScript/Node.js**: See [AGENTS-typescript.md](./AGENTS-typescript.md#quickstarts)
- **Go**: See [AGENTS-go.md](./AGENTS-go.md#quickstarts)
- **Java**: See [AGENTS-java.md](./AGENTS-java.md#quickstarts)

---

## Quickstart Options

### 1. Quick Test

**Create an index, upsert data, and perform semantic search.**

- Best for: First-time users, learning the basics
- Time: 10-15 minutes
- Skills: Basic familiarity with your chosen language

### 2. Semantic Search System

**Build a search system that returns ranked results from your knowledge base.**

- Best for: Search interfaces, document retrieval
- Use case: Users need a list of relevant documents with confidence scores
- Skills: Intermediate programming

### 3. Multi-Tenant RAG System

**Build a RAG system with namespace isolation for multiple tenants.**

- Best for: Knowledge bases, customer support, collaborative workspaces
- Use case: Each tenant needs isolated access to their data
- Skills: Intermediate programming, familiarity with LLMs
- Requirements: LLM API key or access (OpenAI, Anthropic, Groq, or local via Ollama)

### 4. Recommendation Engine

**Build a recommendation engine using semantic similarity.**

- Best for: E-commerce, content platforms, personalization
- Use case: Suggest similar items to users
- Skills: Intermediate programming

---

## Setup Prerequisites (All Quickstarts)

Before starting any quickstart, complete these steps:

### 1. Install Pinecone CLI

**macOS:**

```bash
brew tap pinecone-io/tap
brew install pinecone-io/tap/pinecone
brew update && brew upgrade pinecone
```

**Other platforms:**
Download from [GitHub Releases](https://github.com/pinecone-io/cli/releases)

**Verify installation:**

```bash
pc version
```

### 2. Install SDK (Choose Your Language)

**Python:**

```bash
pip install pinecone
```

**TypeScript/Node.js:**

```bash
npm install @pinecone-database/pinecone
# or
yarn add @pinecone-database/pinecone
```

**Go:**

```bash
go get github.com/pinecone-io/go-pinecone/pinecone@latest
```

**Java (Maven):**

```xml
<dependency>
    <groupId>io.pinecone</groupId>
    <artifactId>pinecone-client</artifactId>
    <version>5.1.0</version>
</dependency>
```

**Java (Gradle):**

```gradle
implementation 'io.pinecone:pinecone-client:5.1.0'
```

### 3. Configure API Key

```bash
# Set your Pinecone API key
export PINECONE_API_KEY="your-api-key-here"

# Authenticate CLI
pc auth configure --api-key $PINECONE_API_KEY
```

Get your API key from: [https://app.pinecone.io/](https://app.pinecone.io/)

### 4. Optional: LLM API Key (For RAG Quickstart Only)

If building a RAG system, you'll need an LLM. Common options:

```bash
# OpenAI
export OPENAI_API_KEY="your-openai-key-here"

# Anthropic
export ANTHROPIC_API_KEY="your-anthropic-key-here"

# Groq
export GROQ_API_KEY="your-groq-key-here"

# Or use a local LLM (e.g., via Ollama)
# No API key needed, just ensure Ollama is running locally
```

**Note**: Any LLM can be used, including local models. For local models, you may need to adapt the API calls in the examples.

---

## Quick Test

**Objective**: Create an index, upsert data, and perform semantic search.

### Steps

1. **Create an index** with integrated embeddings using CLI
2. **Prepare sample data** from different domains (history, science, art, etc.)
3. **Upsert data** into the index
4. **Search** for semantically similar documents
5. **Rerank results** for better accuracy

### Language Examples

- **Python**: See [AGENTS-python.md - Quick Test](./AGENTS-python.md#quick-test)
- **TypeScript**: See [AGENTS-typescript.md - Quick Test](./AGENTS-typescript.md#quick-test)
- **Go**: See [AGENTS-go.md - Quick Test](./AGENTS-go.md#quick-test)
- **Java**: See [AGENTS-java.md - Quick Test](./AGENTS-java.md#quick-test)

### Key Concepts Learned

- Index creation with integrated embeddings
- Namespace usage for data isolation
- Semantic search basics
- Reranking for improved results

---

## Build a Semantic Search System

**Objective**: Build a production-ready search system for your knowledge base.

### Steps

1. **Create an index** with integrated embeddings
2. **Create documents** with rich metadata (20+ documents recommended)
3. **Store documents** in Pinecone using proper namespaces
4. **Build search function** with:
   - Semantic search
   - Reranking with `bge-reranker-v2-m3` model
   - Metadata filtering
   - Error handling
5. **Test with sample queries**
6. **Review results** and iterate

### Production Patterns

- Always use shielded namespaces
- Always rerank results
- Implement exponential backoff retry
- Handle edge cases gracefully

### Language Examples

See the "Use Case Examples" section in your language guide:

- **Python**: [AGENTS-python.md - Semantic Search](./AGENTS-python.md#semantic-search-system)
- **TypeScript**: [AGENTS-typescript.md - Semantic Search](./AGENTS-typescript.md#semantic-search-system)
- **Go**: [AGENTS-go.md - Semantic Search](./AGENTS-go.md#semantic-search-system)
- **Java**: [AGENTS-java.md - Semantic Search](./AGENTS-java.md#semantic-search-system)

---

## Build a Multi-Tenant RAG System

**Objective**: Build a RAG system with namespace isolation for multiple tenants.

### Steps

1. **Create an index** with integrated embeddings
2. **Create tenant data** (emails, documents, etc.) with metadata
3. **Store data per tenant** using separate namespaces
4. **Build RAG function** that:
   - Enforces namespace isolation
   - Searches only specified user's namespace
   - Retrieves and reranks results
   - Constructs LLM prompt
   - Returns answer with citations
5. **Test with multi-tenant queries**
6. **Verify data isolation**

### Key Features

- **Namespace isolation**: Each tenant's data is completely isolated
- **LLM integration**: Works with any LLM (OpenAI, Anthropic, models provided by Groq, local models via Ollama, etc.)
- **Metadata citation**: Includes source references
- **Context window management**: Handles large result sets intelligently

### Language Examples

See the "Use Case Examples" section in your language guide:

- **Python**: [AGENTS-python.md - RAG System](./AGENTS-python.md#multi-tenant-rag-system)
- **TypeScript**: [AGENTS-typescript.md - RAG System](./AGENTS-typescript.md#multi-tenant-rag-system)
- **Go**: [AGENTS-go.md - RAG System](./AGENTS-go.md#multi-tenant-rag-system)
- **Java**: [AGENTS-java.md - RAG System](./AGENTS-java.md#multi-tenant-rag-system)

---

## Build a Recommendation Engine

**Objective**: Build a recommendation engine using semantic similarity.

### Steps

1. **Create an index** with integrated embeddings
2. **Create product listings** with rich metadata (20+ products)
3. **Store products** in Pinecone
4. **Build recommendation function** that:
   - Finds similar items using vector similarity
   - Filters by category, price, etc.
   - Implements diversity strategies
   - Returns formatted recommendations
5. **Test appearance recommendations**
6. **Review accuracy**

### Key Features

- **Semantic similarity**: Finds similar products based on meaning
- **Metadata filtering**: Can filter by any attribute
- **Diversity strategies**: Prevents category clustering
- **Multi-item support**: Can aggregate preferences

### Language Examples

See the "Use Case Examples" section in your language guide:

- **Python**: [AGENTS-python.md - Recommendations](./AGENTS-python.md#recommendation-engine)
- **TypeScript**: [AGENTS-typescript.md - Recommendations](./AGENTS-typescript.md#recommendation-engine)
- **Go**: [AGENTS-go.md - Recommendations](./AGENTS-go.md#recommendation-engine)
- **Java**: [AGENTS-java.md - Recommendations](./AGENTS-java.md#recommendation-engine)

---

## Common CLI Commands

All quickstarts use these CLI commands:

### Create Index

```bash
pc index create -n <index-name> -m cosine -c aws -r us-east-1 \
  --model llama-text-embed-v2 \
  --field_map text=content
```

### List Indexes

```bash
pc index list
```

### Describe Index

```bash
pc index describe --name <index-name>
```

### Delete Index

```bash
pc index delete --name <index-name>
```

See [AGENTS-cli.md](./AGENTS-cli.md) for complete CLI reference.

---

## Next Steps

After completing a quickstart:

1. **Explore advanced features**: [AGENTS.md](../AGENTS.md#official-documentation-resources)
2. **Learn data operations**: See language-specific sections on upsert, fetch, delete
3. **Master search patterns**: Understand filtering, reranking, hybrid search
4. **Production best practices**: Error handling, retry logic, monitoring

## Troubleshooting

| Issue                            | Solution                                 |
| -------------------------------- | ---------------------------------------- |
| `ModuleNotFoundError` or similar | Reinstall SDK with latest version        |
| Search returns no results        | Check namespace, wait ~5s after upsert   |
| 404 on index operations          | Verify index exists with `pc index list` |
| Rate limit errors                | Implement exponential backoff retry      |

See [AGENTS.md](../AGENTS.md#quick-troubleshooting) for more troubleshooting tips.

---

**Remember**: Always use namespaces, always rerank, always handle errors with retry logic.
