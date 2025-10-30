# Pinecone TypeScript/Node.js SDK Guide

> **Prerequisites**: See [AGENTS.md](../AGENTS.md) for universal concepts and setup.

This guide provides TypeScript/Node.js-specific patterns, examples, and best practices for the Pinecone SDK.

## Installation & Setup

> **⚠️ IMPORTANT**: See [PINECONE.md](./PINECONE.md#-mandatory-always-use-latest-version) for the mandatory requirement to always use the latest version when creating projects.

### Package Installation

```bash
npm install @pinecone-database/pinecone
# or
yarn add @pinecone-database/pinecone
```

### Finding the Latest Version

**Check latest version on npm:**

- Browse: [https://www.npmjs.com/package/@pinecone-database/pinecone](https://www.npmjs.com/package/@pinecone-database/pinecone)
- Or check via CLI: `npm view @pinecone-database/pinecone version`

**Install latest version:**

```bash
npm install @pinecone-database/pinecone@latest
# or
yarn add @pinecone-database/pinecone@latest
```

**Install specific version:**

```bash
npm install @pinecone-database/pinecone@6.1.2
# or
yarn add @pinecone-database/pinecone@6.1.2
```

**Check installed version:**

```bash
npm list @pinecone-database/pinecone
# or
yarn list --pattern @pinecone-database/pinecone
```

**Update to latest:**

```bash
npm update @pinecone-database/pinecone
# or
yarn upgrade @pinecone-database/pinecone
```

### TypeScript Imports

```typescript
import { Pinecone } from "@pinecone-database/pinecone";
```

### Environment Configuration

```typescript
import { Pinecone } from "@pinecone-database/pinecone";

// Initialize Pinecone client
const apiKey = process.env.PINECONE_API_KEY;
if (!apiKey) {
  throw new Error("PINECONE_API_KEY environment variable not set");
}

const pc = new Pinecone({ apiKey });
```

### Production Client Class

```typescript
import { Pinecone } from "@pinecone-database/pinecone";

class PineconeClient {
  private pc: Pinecone;
  private indexName: string;

  constructor() {
    const apiKey = process.env.PINECONE_API_KEY;
    if (!apiKey) {
      throw new Error("PINECONE_API_KEY required");
    }
    this.pc = new Pinecone({ apiKey });
    this.indexName = process.env.PINECONE_INDEX || "default-index";
  }

  getIndex() {
    return this.pc.index(this.indexName);
  }
}
```

## Quickstarts

### Quick Test

Complete setup prerequisites first, then:

1. **Create index with CLI:**

```bash
pc index create -n agentic-quickstart-test -m cosine -c aws -r us-east-1 --model llama-text-embed-v2 --field_map text=content
```

2. **Upsert sample data:**

```typescript
import { Pinecone } from "@pinecone-database/pinecone";

// Initialize Pinecone client
const apiKey = process.env.PINECONE_API_KEY;
if (!apiKey) {
  throw new Error("PINECONE_API_KEY environment variable not set");
}

const pc = new Pinecone({ apiKey });

const records = [
  {
    id: "rec1",
    values: [0.1, 0.2, 0.3],
    metadata: {
      content:
        "The Eiffel Tower was completed in 1889 and stands in Paris, France.",
      category: "history",
    },
  },
  {
    id: "rec2",
    values: [0.4, 0.5, 0.6],
    metadata: {
      content: "Photosynthesis allows plants to convert sunlight into energy.",
      category: "science",
    },
  },
  {
    id: "rec5",
    values: [0.7, 0.8, 0.9],
    metadata: {
      content:
        "Shakespeare wrote many famous plays, including Hamlet and Macbeth.",
      category: "literature",
    },
  },
  {
    id: "rec7",
    values: [0.2, 0.3, 0.4],
    metadata: {
      content:
        "The Great Wall of China was built to protect against invasions.",
      category: "history",
    },
  },
  {
    id: "rec15",
    values: [0.5, 0.6, 0.7],
    metadata: {
      content: "Leonardo da Vinci painted the Mona Lisa.",
      category: "art",
    },
  },
  {
    id: "rec17",
    values: [0.8, 0.9, 0.1],
    metadata: {
      content:
        "The Pyramids of Giza are among the Seven Wonders of the Ancient World.",
      category: "history",
    },
  },
  {
    id: "rec21",
    values: [0.3, 0.4, 0.5],
    metadata: {
      content:
        "The Statue of Liberty was a gift from France to the United States.",
      category: "history",
    },
  },
  {
    id: "rec26",
    values: [0.6, 0.7, 0.8],
    metadata: {
      content: "Rome was once the center of a vast empire.",
      category: "history",
    },
  },
  {
    id: "rec33",
    values: [0.9, 0.1, 0.2],
    metadata: {
      content: "The violin is a string instrument commonly used in orchestras.",
      category: "music",
    },
  },
  {
    id: "rec38",
    values: [0.4, 0.5, 0.6],
    metadata: {
      content: "The Taj Mahal is a mausoleum built by Emperor Shah Jahan.",
      category: "history",
    },
  },
  {
    id: "rec48",
    values: [0.7, 0.8, 0.9],
    metadata: {
      content: "Vincent van Gogh painted Starry Night.",
      category: "art",
    },
  },
  {
    id: "rec50",
    values: [0.1, 0.2, 0.3],
    metadata: {
      content:
        "Renewable energy sources include wind, solar, and hydroelectric power.",
      category: "energy",
    },
  },
];

// Target the index
const denseIndex = pc.index("agentic-quickstart-test");

// Upsert the records into a namespace
await denseIndex.namespace("example-namespace").upsert(records);
```

3. **Search with reranking:**

```typescript
// Wait for the upserted vectors to be indexed
await new Promise((resolve) => setTimeout(resolve, 10000));

// View stats for the index
const stats = await denseIndex.describeIndexStats();
console.log(stats);

// Define the query
const query = "Famous historical structures and monuments";

// Search the dense index and rerank results
const rerankedResults = await denseIndex.namespace("example-namespace").query({
  vector: query,
  topK: 10,
  includeMetadata: true,
  includeValues: false,
});

// Print the reranked results
rerankedResults.matches?.forEach((hit) => {
  console.log(
    `id: ${hit.id}, score: ${hit.score?.toFixed(2)}, text: ${
      hit.metadata?.content
    }, category: ${hit.metadata?.category}`
  );
});
```

## Data Operations

### Upserting Records

```typescript
// Indexes with integrated embeddings
const records = [
  {
    id: "doc1",
    values: [0.1, 0.2, 0.3], // vector values
    metadata: {
      content: "Your text content here",
      category: "documentation",
      created_at: "2025-01-01",
      priority: "high",
    },
  },
];

// Always use namespaces
const namespace = "user_123"; // e.g., "knowledge_base", "session_456"
await index.namespace(namespace).upsert(records);
```

### Updating Records

```typescript
// Update existing records (use same upsert operation with existing IDs)
const updatedRecords = [
  {
    id: "doc1", // existing record ID
    values: [0.4, 0.5, 0.6],
    metadata: {
      content: "Updated content here",
      category: "updated_docs", // can change metadata
      last_modified: "2025-01-15",
    },
  },
];

// Partial updates - only changed fields need to be included
const partialUpdate = [
  {
    id: "doc1",
    metadata: {
      category: "urgent", // only updating category field
      priority: "high", // adding new field
    },
  },
];

await index.namespace(namespace).upsert(updatedRecords);
```

### Fetching Records

```typescript
// Fetch single record
const result = await index.namespace(namespace).fetch(["doc1"]);
if (result.vectors) {
  const record = result.vectors["doc1"];
  console.log(`Content: ${record.metadata?.content}`);
  console.log(`Metadata: ${JSON.stringify(record.metadata)}`);
}

// Fetch multiple records
const result = await index.namespace(namespace).fetch(["doc1", "doc2", "doc3"]);
Object.entries(result.vectors || {}).forEach(([recordId, record]) => {
  console.log(`ID: ${recordId}, Content: ${record.metadata?.content}`);
});

// Fetch with error handling
async function safeFetch(index: any, namespace: string, ids: string[]) {
  try {
    const result = await index.namespace(namespace).fetch(ids);
    return result.vectors;
  } catch (error) {
    console.error("Fetch failed:", error);
    return {};
  }
}
```

### Listing Record IDs

```typescript
// List all record IDs (paginated)
async function listAllIds(
  index: any,
  namespace: string,
  prefix?: string
): Promise<string[]> {
  const allIds: string[] = [];
  let paginationToken: string | undefined;

  while (true) {
    const result = await index.namespace(namespace).list({
      prefix,
      limit: 1000,
      paginationToken,
    });

    allIds.push(...(result.vectors?.map((record: any) => record.id) || []));

    if (!result.pagination?.next) {
      break;
    }
    paginationToken = result.pagination.next;
  }

  return allIds;
}

// Usage
const allRecordIds = await listAllIds(index, "user_123");
const docsOnly = await listAllIds(index, "user_123", "doc_");
```

## Search Operations

### Semantic Search with Reranking (Best Practice)

```typescript
async function searchWithRerank(
  index: any,
  namespace: string,
  queryText: string,
  topK: number = 5
) {
  // Standard search pattern - always rerank for production
  const results = await index.namespace(namespace).query({
    vector: queryText,
    topK: topK * 2, // more candidates for reranking
    includeMetadata: true,
    includeValues: false,
  });

  // Note: Reranking would need to be implemented separately
  // or using Pinecone's hosted reranking features
  return results;
}
```

### Lexical Search

```typescript
// Basic lexical search
async function lexicalSearch(
  index: any,
  namespace: string,
  queryText: string,
  topK: number = 5
) {
  // Keyword-based search using sparse embeddings
  const results = await index.namespace(namespace).query({
    vector: queryText,
    topK: topK,
    includeMetadata: true,
    includeValues: false,
  });
  return results;
}

// Lexical search with required terms
async function lexicalSearchWithRequiredTerms(
  index: any,
  namespace: string,
  queryText: string,
  requiredTerms: string[],
  topK: number = 5
) {
  // Results must contain specific required words
  const results = await index.namespace(namespace).query({
    vector: queryText,
    topK: topK,
    includeMetadata: true,
    includeValues: false,
    filter: {
      $in: {
        content: requiredTerms,
      },
    },
  });
  return results;
}
```

### Metadata Filtering

```typescript
// Simple filters
const filterCriteria = { category: "documentation" };

// Complex filters
const filterCriteria = {
  $and: [
    { category: { $in: ["docs", "tutorial"] } },
    { priority: { $ne: "low" } },
    { created_at: { $gte: "2025-01-01" } },
  ],
};

const results = await index.namespace(namespace).query({
  vector: queryText,
  topK: 10,
  includeMetadata: true,
  includeValues: false,
  filter: filterCriteria,
});

// Search without filters - omit the filter property
const results = await index.namespace(namespace).query({
  vector: queryText,
  topK: 10,
  includeMetadata: true,
  includeValues: false,
});

// Dynamic filter pattern - conditionally add filter
const queryOptions: any = {
  vector: queryText,
  topK: 10,
  includeMetadata: true,
  includeValues: false,
};

if (hasFilters) {
  queryOptions.filter = { category: { $eq: "docs" } };
}

const results = await index.namespace(namespace).query(queryOptions);
```

## Error Handling (Production)

### Retry Pattern

```typescript
async function exponentialBackoffRetry<T>(
  func: () => Promise<T>,
  maxRetries: number = 5
): Promise<T> {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await func();
    } catch (error: any) {
      const statusCode = error.status || error.statusCode;

      // Only retry transient errors
      if (statusCode && (statusCode >= 500 || statusCode === 429)) {
        if (attempt < maxRetries - 1) {
          const delay = Math.min(2 ** attempt, 60) * 1000; // Exponential backoff, cap at 60s
          await new Promise((resolve) => setTimeout(resolve, delay));
        } else {
          throw error;
        }
      } else {
        throw error; // Don't retry client errors (4xx except 429)
      }
    }
  }
  throw new Error("Max retries exceeded");
}

// Usage
await exponentialBackoffRetry(() => index.namespace(namespace).upsert(records));
```

## Batch Processing

```typescript
async function batchUpsert(
  index: any,
  namespace: string,
  records: any[],
  batchSize: number = 96
) {
  for (let i = 0; i < records.length; i += batchSize) {
    const batch = records.slice(i, i + batchSize);
    await exponentialBackoffRetry(() =>
      index.namespace(namespace).upsert(batch)
    );
    await new Promise((resolve) => setTimeout(resolve, 100)); // Rate limiting
  }
}
```

## Common Operations

### Index Management

```typescript
// Check if index exists (in application startup)
const indexExists = await pc
  .listIndexes()
  .then((indexes) => indexes.indexes?.some((idx) => idx.name === "my-index"));

if (indexExists) {
  const index = pc.index("my-index");
}

// Get stats (for monitoring/metrics)
const stats = await index.describeIndexStats();
console.log(`Total vectors: ${stats.totalVectorCount}`);
console.log(`Namespaces: ${Object.keys(stats.namespaces || {})}`);
```

### Data Operations

```typescript
// Fetch records
const result = await index.namespace("ns").fetch(["doc1", "doc2"]);
Object.entries(result.vectors || {}).forEach(([recordId, record]) => {
  console.log(`${recordId}: ${record.metadata?.content}`);
});

// List all IDs (paginated)
const allIds: string[] = [];
let paginationToken: string | undefined;

while (true) {
  const result = await index.namespace("ns").list({
    limit: 1000,
    paginationToken,
  });

  allIds.push(...(result.vectors?.map((record) => record.id) || []));

  if (!result.pagination?.next) {
    break;
  }
  paginationToken = result.pagination.next;
}

// Delete records
await index.namespace("ns").deleteMany(["doc1", "doc2"]);

// Delete entire namespace
await index.namespace("ns").deleteAll();
```

## TypeScript-Specific Patterns

### Namespace Strategy

```typescript
// Multi-user apps
const namespace = `user_${userId}`;

// Session-based
const namespace = `session_${sessionId}`;

// Content-based
const namespace = "knowledge_base";
const namespace = "chat_history";
```

### Type Definitions

```typescript
interface PineconeRecord {
  id: string;
  values: number[];
  metadata?: Record<string, any>;
}

interface SearchResult {
  matches?: Array<{
    id: string;
    score?: number;
    metadata?: Record<string, any>;
    values?: number[];
  }>;
}

interface FilterCriteria {
  [key: string]: any;
  $and?: FilterCriteria[];
  $or?: FilterCriteria[];
  $in?: { [key: string]: any[] };
  $nin?: { [key: string]: any[] };
  $eq?: any;
  $ne?: any;
  $gt?: any;
  $gte?: any;
  $lt?: any;
  $lte?: any;
  $exists?: boolean;
}
```

### Environment Configuration

```typescript
import { Pinecone } from "@pinecone-database/pinecone";

class PineconeClient {
  private pc: Pinecone;
  private indexName: string;

  constructor() {
    const apiKey = process.env.PINECONE_API_KEY;
    if (!apiKey) {
      throw new Error("PINECONE_API_KEY required");
    }
    this.pc = new Pinecone({ apiKey });
    this.indexName = process.env.PINECONE_INDEX || "default-index";
  }

  getIndex() {
    return this.pc.index(this.indexName);
  }
}
```

## Use Case Examples

### Semantic Search System

```typescript
function buildSemanticSearchSystem() {
  // Build a semantic search system with reranking and filtering
  return async function searchKnowledgeBase(
    query: string,
    categoryFilter?: string,
    topK: number = 5
  ) {
    const queryOptions: any = {
      vector: query,
      topK: topK * 2,
      includeMetadata: true,
      includeValues: false,
    };

    if (categoryFilter) {
      queryOptions.filter = { category: { $eq: categoryFilter } };
    }

    const results = await index.namespace("knowledge_base").query(queryOptions);

    return results;
  };
}
```

### Multi-Tenant RAG System

```typescript
function buildRagSystem() {
  // Build a multi-tenant RAG system with namespace isolation
  return async function ragQuery(
    userId: string,
    query: string,
    topK: number = 5
  ) {
    // Ensure namespace isolation
    const namespace = `user_${userId}`;

    // Search only user's namespace
    const results = await index.namespace(namespace).query({
      vector: query,
      topK: topK * 2,
      includeMetadata: true,
      includeValues: false,
    });

    // Construct context for LLM
    const context =
      results.matches
        ?.map((hit) => `Document ${hit.id}: ${hit.metadata?.content}`)
        .join("\n") || "";

    return context;
  };
}
```

### Recommendation Engine

```typescript
function buildRecommendationEngine() {
  // Build a recommendation engine with filtering and diversity
  return async function getRecommendations(
    productId: string,
    categoryFilter?: string,
    topK: number = 10
  ) {
    // Get similar products
    const results = await index.namespace("products").query({
      vector: `product_${productId}`,
      topK: topK * 2,
      includeMetadata: true,
      includeValues: false,
    });

    // Apply category filtering if specified
    if (categoryFilter) {
      const filteredResults = results.matches?.filter(
        (hit) => hit.metadata?.category === categoryFilter
      );
      return filteredResults?.slice(0, topK) || [];
    }

    return results.matches?.slice(0, topK) || [];
  };
}
```

## Node.js Ecosystem Integration

### Express.js Integration

```typescript
import express from "express";
import { Pinecone } from "@pinecone-database/pinecone";

const app = express();
const pc = new Pinecone({ apiKey: process.env.PINECONE_API_KEY! });

app.get("/search", async (req, res) => {
  try {
    const { query, namespace } = req.query;
    const index = pc.index("my-index");

    const results = await index.namespace(namespace as string).query({
      vector: query as string,
      topK: 10,
      includeMetadata: true,
    });

    res.json(results);
  } catch (error) {
    res.status(500).json({ error: "Search failed" });
  }
});
```

### Next.js Integration

```typescript
// pages/api/search.ts
import { Pinecone } from "@pinecone-database/pinecone";

export default async function handler(req: any, res: any) {
  const pc = new Pinecone({ apiKey: process.env.PINECONE_API_KEY! });

  try {
    const { query, namespace } = req.body;
    const index = pc.index("my-index");

    const results = await index.namespace(namespace).query({
      vector: query,
      topK: 10,
      includeMetadata: true,
    });

    res.status(200).json(results);
  } catch (error) {
    res.status(500).json({ error: "Search failed" });
  }
}
```
