# Pinecone Go SDK Guide

> **Prerequisites**: See [AGENTS.md](../AGENTS.md) for universal concepts and setup.

This guide provides Go-specific patterns, examples, and best practices for the Pinecone SDK.

## Installation & Setup

### Go Module Installation

```bash
go get github.com/pinecone-io/go-pinecone/pinecone
```

### Finding the Latest Version

**Check latest version on GitHub:**

- Releases: [https://github.com/pinecone-io/go-pinecone/releases](https://github.com/pinecone-io/go-pinecone/releases)
- Or via Go: `go list -m -versions github.com/pinecone-io/go-pinecone/pinecone`

**Install latest version:**

```bash
go get github.com/pinecone-io/go-pinecone/pinecone@latest
```

**Install specific version:**

```bash
go get github.com/pinecone-io/go-pinecone/pinecone@v4.1.4  # Replace with desired version
```

**Check installed version:**

```bash
go list -m github.com/pinecone-io/go-pinecone/pinecone
```

**Update dependencies:**

```bash
go get -u github.com/pinecone-io/go-pinecone/pinecone
go mod tidy
```

> **⚠️ Best Practice**: Always use the latest version of the Pinecone SDK unless the user explicitly requests a specific version. Check the latest version using the methods above and update your installation accordingly.

### Go Imports

```go
import (
    "context"
    "fmt"
    "os"
    "time"

    "github.com/pinecone-io/go-pinecone/pinecone"
)
```

### Environment Configuration

```go
import (
    "context"
    "fmt"
    "os"

    "github.com/pinecone-io/go-pinecone/pinecone"
)

func createClient() (*pinecone.Client, error) {
    apiKey := os.Getenv("PINECONE_API_KEY")
    if apiKey == "" {
        return nil, fmt.Errorf("PINECONE_API_KEY environment variable not set")
    }

    client, err := pinecone.NewClient(pinecone.NewClientParams{
        ApiKey: apiKey,
    })

    if err != nil {
        return nil, fmt.Errorf("failed to create Pinecone client: %w", err)
    }

    return client, nil
}
```

### Production Client Struct

```go
import (
    "context"
    "fmt"
    "os"

    "github.com/pinecone-io/go-pinecone/pinecone"
)

type PineconeService struct {
    client    *pinecone.Client
    indexName string
}

func NewPineconeService() (*PineconeService, error) {
    apiKey := os.Getenv("PINECONE_API_KEY")
    if apiKey == "" {
        return nil, fmt.Errorf("PINECONE_API_KEY required")
    }

    client, err := pinecone.NewClient(pinecone.NewClientParams{
        ApiKey: apiKey,
    })

    if err != nil {
        return nil, fmt.Errorf("failed to create Pinecone client: %w", err)
    }

    indexName := os.Getenv("PINECONE_INDEX")
    if indexName == "" {
        indexName = "default-index"
    }

    return &PineconeService{
        client:    client,
        indexName: indexName,
    }, nil
}

func (ps *PineconeService) GetIndex() *pinecone.Index {
    return ps.client.Index(ps.indexName)
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

```go
package main

import (
    "context"
    "fmt"
    "os"

    "github.com/pinecone-io/go-pinecone/pinecone"
)

func main() {
    // Initialize Pinecone client
    apiKey := os.Getenv("PINECONE_API_KEY")
    if apiKey == "" {
        panic("PINECONE_API_KEY environment variable not set")
    }

    client, err := pinecone.NewClient(pinecone.NewClientParams{
        ApiKey: apiKey,
    })
    if err != nil {
        panic(fmt.Sprintf("Failed to create client: %v", err))
    }

    // Sample records
    records := []pinecone.Vector{
        {
            Id: "rec1",
            Values: []float32{0.1, 0.2, 0.3},
            Metadata: map[string]interface{}{
                "content":  "The Eiffel Tower was completed in 1889 and stands in Paris, France.",
                "category": "history",
            },
        },
        {
            Id: "rec2",
            Values: []float32{0.4, 0.5, 0.6},
            Metadata: map[string]interface{}{
                "content":  "Photosynthesis allows plants to convert sunlight into energy.",
                "category": "science",
            },
        },
        {
            Id: "rec5",
            Values: []float32{0.7, 0.8, 0.9},
            Metadata: map[string]interface{}{
                "content":  "Shakespeare wrote many famous plays, including Hamlet and Macbeth.",
                "category": "literature",
            },
        },
    }

    // Target the index
    index := client.Index("agentic-quickstart-test")

    // Upsert the records into a namespace
    ctx := context.Background()
    _, err = index.Upsert(ctx, pinecone.UpsertParams{
        Vectors:   records,
        Namespace: "example-namespace",
    })

    if err != nil {
        panic(fmt.Sprintf("Failed to upsert: %v", err))
    }
}
```

3. **Search with reranking:**

```go
import (
    "context"
    "fmt"
    "time"
)

func searchExample() {
    // Wait for the upserted vectors to be indexed
    time.Sleep(10 * time.Second)

    // View stats for the index
    ctx := context.Background()
    stats, err := index.DescribeIndexStats(ctx)
    if err != nil {
        panic(fmt.Sprintf("Failed to get stats: %v", err))
    }
    fmt.Printf("Stats: %+v\n", stats)

    // Define the query
    query := []float32{0.1, 0.2, 0.3} // This would be the actual query vector

    // Search the dense index
    results, err := index.Query(ctx, pinecone.QueryParams{
        Vector:      query,
        TopK:        10,
        Namespace:   "example-namespace",
        IncludeMetadata: true,
        IncludeValues:   false,
    })

    if err != nil {
        panic(fmt.Sprintf("Failed to query: %v", err))
    }

    // Print the results
    for _, hit := range results.Matches {
        fmt.Printf("id: %s | score: %.2f | category: %s | text: %s\n",
            hit.Id,
            hit.Score,
            hit.Metadata["category"],
            hit.Metadata["content"])
    }
}
```

## Data Operations

### Upserting Records

```go
func upsertRecords() error {
    // Indexes with integrated embeddings
    records := []pinecone.Vector{
        {
            Id: "doc1",
            Values: []float32{0.1, 0.2, 0.3}, // vector values
            Metadata: map[string]interface{}{
                "content":    "Your text content here",
                "category":   "documentation",
                "created_at": "2025-01-01",
                "priority":   "high",
            },
        },
    }

    // Always use namespaces
    namespace := "user_123" // e.g., "knowledge_base", "session_456"

    ctx := context.Background()
    _, err := index.Upsert(ctx, pinecone.UpsertParams{
        Vectors:   records,
        Namespace: namespace,
    })

    return err
}
```

### Updating Records

```go
func updateRecords() error {
    // Update existing records (use same upsert operation with existing IDs)
    updatedRecords := []pinecone.Vector{
        {
            Id: "doc1", // existing record ID
            Values: []float32{0.4, 0.5, 0.6},
            Metadata: map[string]interface{}{
                "content":       "Updated content here",
                "category":      "updated_docs", // can change metadata
                "last_modified": "2025-01-15",
            },
        },
    }

    // Partial updates - only changed fields need to be included
    partialUpdate := []pinecone.Vector{
        {
            Id: "doc1",
            Metadata: map[string]interface{}{
                "category": "urgent", // only updating category field
                "priority": "high",   // adding new field
            },
        },
    }

    ctx := context.Background()
    _, err := index.Upsert(ctx, pinecone.UpsertParams{
        Vectors:   updatedRecords,
        Namespace: namespace,
    })

    return err
}
```

### Fetching Records

```go
func fetchRecords() error {
    // Fetch single record
    ctx := context.Background()
    result, err := index.Fetch(ctx, pinecone.FetchParams{
        Ids:       []string{"doc1"},
        Namespace: namespace,
    })

    if err != nil {
        return err
    }

    if record, exists := result.Vectors["doc1"]; exists {
        fmt.Printf("Content: %v\n", record.Metadata["content"])
        fmt.Printf("Metadata: %+v\n", record.Metadata)
    }

    // Fetch multiple records
    multiResult, err := index.Fetch(ctx, pinecone.FetchParams{
        Ids:       []string{"doc1", "doc2", "doc3"},
        Namespace: namespace,
    })

    if err != nil {
        return err
    }

    for recordId, record := range multiResult.Vectors {
        fmt.Printf("ID: %s, Content: %v\n", recordId, record.Metadata["content"])
    }

    return nil
}

// Fetch with error handling
func safeFetch(namespace string, ids []string) (map[string]pinecone.Vector, error) {
    ctx := context.Background()
    result, err := index.Fetch(ctx, pinecone.FetchParams{
        Ids:       ids,
        Namespace: namespace,
    })

    if err != nil {
        fmt.Printf("Fetch failed: %v\n", err)
        return nil, err
    }

    return result.Vectors, nil
}
```

### Listing Record IDs

```go
func listAllIds(namespace string, prefix string) ([]string, error) {
    var allIds []string
    var paginationToken string

    for {
        params := pinecone.ListParams{
            Namespace: namespace,
            Limit:     1000,
        }

        if prefix != "" {
            params.Prefix = prefix
        }

        if paginationToken != "" {
            params.PaginationToken = paginationToken
        }

        ctx := context.Background()
        result, err := index.List(ctx, params)
        if err != nil {
            return nil, err
        }

        for _, vector := range result.Vectors {
            allIds = append(allIds, vector.Id)
        }

        if result.Pagination == nil || result.Pagination.Next == "" {
            break
        }
        paginationToken = result.Pagination.Next
    }

    return allIds, nil
}

// Usage
allRecordIds, err := listAllIds("user_123", "")
if err != nil {
    panic(err)
}

docsOnly, err := listAllIds("user_123", "doc_")
if err != nil {
    panic(err)
}
```

## Search Operations

### Semantic Search with Reranking (Best Practice)

```go
func searchWithRerank(namespace string, queryVector []float32, topK int) (*pinecone.QueryResponse, error) {
    // Standard search pattern - always rerank for production
    ctx := context.Background()
    results, err := index.Query(ctx, pinecone.QueryParams{
        Vector:         queryVector,
        TopK:           topK * 2, // more candidates for reranking
        Namespace:      namespace,
        IncludeMetadata: true,
        IncludeValues:   false,
    })

    if err != nil {
        return nil, err
    }

    // Note: Reranking would need to be implemented separately
    // or using Pinecone's hosted reranking features
    return results, nil
}
```

### Lexical Search

```go
// Basic lexical search
func lexicalSearch(namespace string, queryVector []float32, topK int) (*pinecone.QueryResponse, error) {
    // Keyword-based search using sparse embeddings
    ctx := context.Background()
    results, err := index.Query(ctx, pinecone.QueryParams{
        Vector:         queryVector,
        TopK:           topK,
        Namespace:      namespace,
        IncludeMetadata: true,
        IncludeValues:   false,
    })

    return results, err
}

// Lexical search with required terms
func lexicalSearchWithRequiredTerms(namespace string, queryVector []float32, requiredTerms []string, topK int) (*pinecone.QueryResponse, error) {
    // Results must contain specific required words
    filter := map[string]interface{}{
        "$in": map[string]interface{}{
            "content": requiredTerms,
        },
    }

    ctx := context.Background()
    results, err := index.Query(ctx, pinecone.QueryParams{
        Vector:         queryVector,
        TopK:           topK,
        Namespace:      namespace,
        IncludeMetadata: true,
        IncludeValues:   false,
        Filter:         filter,
    })

    return results, err
}
```

### Metadata Filtering

```go
func searchWithFilters(namespace string, queryVector []float32) (*pinecone.QueryResponse, error) {
    // Simple filters
    simpleFilter := map[string]interface{}{
        "category": "documentation",
    }

    // Complex filters
    complexFilter := map[string]interface{}{
        "$and": []map[string]interface{}{
            {
                "category": map[string]interface{}{
                    "$in": []string{"docs", "tutorial"},
                },
            },
            {
                "priority": map[string]interface{}{
                    "$ne": "low",
                },
            },
            {
                "created_at": map[string]interface{}{
                    "$gte": "2025-01-01",
                },
            },
        },
    }

    ctx := context.Background()
    results, err := index.Query(ctx, pinecone.QueryParams{
        Vector:         queryVector,
        TopK:           10,
        Namespace:      namespace,
        IncludeMetadata: true,
        IncludeValues:   false,
        Filter:         complexFilter,
    })

    return results, err
}

// Search without filters - omit the filter property
func searchWithoutFilters(namespace string, queryVector []float32) (*pinecone.QueryResponse, error) {
    ctx := context.Background()
    results, err := index.Query(ctx, pinecone.QueryParams{
        Vector:         queryVector,
        TopK:           10,
        Namespace:      namespace,
        IncludeMetadata: true,
        IncludeValues:   false,
    })

    return results, err
}

// Dynamic filter pattern - conditionally add filter
func searchWithDynamicFilter(namespace string, queryVector []float32, hasFilters bool) (*pinecone.QueryResponse, error) {
    params := pinecone.QueryParams{
        Vector:         queryVector,
        TopK:           10,
        Namespace:      namespace,
        IncludeMetadata: true,
        IncludeValues:   false,
    }

    if hasFilters {
        filter := map[string]interface{}{
            "category": map[string]interface{}{
                "$eq": "docs",
            },
        }
        params.Filter = filter
    }

    ctx := context.Background()
    return index.Query(ctx, params)
}
```

## Error Handling (Production)

### Retry Pattern

```go
import (
    "context"
    "fmt"
    "math"
    "time"
)

func exponentialBackoffRetry(ctx context.Context, fn func() error, maxRetries int) error {
    for attempt := 0; attempt < maxRetries; attempt++ {
        err := fn()
        if err == nil {
            return nil
        }

        // Extract status code from error
        statusCode := extractStatusCode(err)

        // Only retry transient errors
        if statusCode >= 500 || statusCode == 429 {
            if attempt < maxRetries-1 {
                delay := time.Duration(math.Min(math.Pow(2, float64(attempt)), 60)) * time.Second
                select {
                case <-ctx.Done():
                    return ctx.Err()
                case <-time.After(delay):
                    continue
                }
            }
        }

        return err // Don't retry client errors (4xx except 429)
    }

    return fmt.Errorf("max retries exceeded")
}

func extractStatusCode(err error) int {
    // This would need to be implemented based on the actual error structure
    // For now, return a default value
    return 500
}

// Usage
ctx := context.Background()
err := exponentialBackoffRetry(ctx, func() error {
    _, err := index.Upsert(ctx, pinecone.UpsertParams{
        Vectors:   records,
        Namespace: namespace,
    })
    return err
}, 5)
```

## Batch Processing

```go
func batchUpsert(namespace string, records []pinecone.Vector, batchSize int) error {
    ctx := context.Background()

    for i := 0; i < len(records); i += batchSize {
        end := i + batchSize
        if end > len(records) {
            end = len(records)
        }

        batch := records[i:end]

        err := exponentialBackoffRetry(ctx, func() error {
            _, err := index.Upsert(ctx, pinecone.UpsertParams{
                Vectors:   batch,
                Namespace: namespace,
            })
            return err
        }, 5)

        if err != nil {
            return err
        }

        time.Sleep(100 * time.Millisecond) // Rate limiting
    }

    return nil
}
```

## Common Operations

### Index Management

```go
func (ps *PineconeService) indexExists(indexName string) bool {
    ctx := context.Background()
    indexes, err := ps.client.ListIndexes(ctx)
    if err != nil {
        return false
    }

    for _, idx := range indexes {
        if idx.Name == indexName {
            return true
        }
    }

    return false
}

// Get stats (for monitoring/metrics)
func (ps *PineconeService) printStats() error {
    ctx := context.Background()
    stats, err := ps.GetIndex().DescribeIndexStats(ctx)
    if err != nil {
        return err
    }

    fmt.Printf("Total vectors: %d\n", stats.TotalVectorCount)
    fmt.Printf("Namespaces: %v\n", stats.Namespaces)

    return nil
}
```

### Data Operations

```go
func (ps *PineconeService) fetchRecords(namespace string, ids []string) error {
    ctx := context.Background()
    result, err := ps.GetIndex().Fetch(ctx, pinecone.FetchParams{
        Ids:       ids,
        Namespace: namespace,
    })

    if err != nil {
        return err
    }

    for recordId, record := range result.Vectors {
        fmt.Printf("%s: %v\n", recordId, record.Metadata["content"])
    }

    return nil
}

// List all IDs (paginated)
func (ps *PineconeService) listAllIds(namespace string) ([]string, error) {
    var allIds []string
    var paginationToken string

    for {
        params := pinecone.ListParams{
            Namespace: namespace,
            Limit:     1000,
        }

        if paginationToken != "" {
            params.PaginationToken = paginationToken
        }

        ctx := context.Background()
        result, err := ps.GetIndex().List(ctx, params)
        if err != nil {
            return nil, err
        }

        for _, vector := range result.Vectors {
            allIds = append(allIds, vector.Id)
        }

        if result.Pagination == nil || result.Pagination.Next == "" {
            break
        }
        paginationToken = result.Pagination.Next
    }

    return allIds, nil
}

// Delete records
func (ps *PineconeService) deleteRecords(namespace string, ids []string) error {
    ctx := context.Background()
    _, err := ps.GetIndex().Delete(ctx, pinecone.DeleteParams{
        Ids:       ids,
        Namespace: namespace,
    })

    return err
}

// Delete entire namespace
func (ps *PineconeService) deleteNamespace(namespace string) error {
    ctx := context.Background()
    _, err := ps.GetIndex().Delete(ctx, pinecone.DeleteParams{
        Namespace:  namespace,
        DeleteAll: true,
    })

    return err
}
```

## Go-Specific Patterns

### Namespace Strategy

```go
// Multi-user apps
func userNamespace(userID string) string {
    return fmt.Sprintf("user_%s", userID)
}

// Session-based
func sessionNamespace(sessionID string) string {
    return fmt.Sprintf("session_%s", sessionID)
}

// Content-based
func knowledgeBaseNamespace() string {
    return "knowledge_base"
}

func chatHistoryNamespace() string {
    return "chat_history"
}
```

### Configuration Management

```go
import (
    "encoding/json"
    "os"
)

type Config struct {
    PineconeAPIKey  string `json:"pinecone_api_key"`
    PineconeIndex   string `json:"pinecone_index"`
}

func loadConfig(configFile string) (*Config, error) {
    data, err := os.ReadFile(configFile)
    if err != nil {
        return nil, err
    }

    var config Config
    err = json.Unmarshal(data, &config)
    if err != nil {
        return nil, err
    }

    // Override with environment variables if present
    if apiKey := os.Getenv("PINECONE_API_KEY"); apiKey != "" {
        config.PineconeAPIKey = apiKey
    }

    if indexName := os.Getenv("PINECONE_INDEX"); indexName != "" {
        config.PineconeIndex = indexName
    }

    return &config, nil
}
```

## Use Case Examples

### Semantic Search System

```go
type SemanticSearchSystem struct {
    index *pinecone.Index
}

func NewSemanticSearchSystem(client *pinecone.Client, indexName string) *SemanticSearchSystem {
    return &SemanticSearchSystem{
        index: client.Index(indexName),
    }
}

func (s *SemanticSearchSystem) SearchKnowledgeBase(query string, categoryFilter string, topK int) (*pinecone.QueryResponse, error) {
    params := pinecone.QueryParams{
        Vector:         convertToVector(query), // This would need to be implemented
        TopK:           topK * 2,
        Namespace:      "knowledge_base",
        IncludeMetadata: true,
        IncludeValues:   false,
    }

    if categoryFilter != "" {
        params.Filter = map[string]interface{}{
            "category": map[string]interface{}{
                "$eq": categoryFilter,
            },
        }
    }

    ctx := context.Background()
    return s.index.Query(ctx, params)
}

func convertToVector(text string) []float32 {
    // This would need to be implemented based on your embedding model
    return []float32{0.1, 0.2, 0.3} // Placeholder
}
```

### Multi-Tenant RAG System

```go
type RagSystem struct {
    index *pinecone.Index
}

func NewRagSystem(client *pinecone.Client, indexName string) *RagSystem {
    return &RagSystem{
        index: client.Index(indexName),
    }
}

func (r *RagSystem) RagQuery(userID string, query string, topK int) (string, error) {
    // Ensure namespace isolation
    namespace := fmt.Sprintf("user_%s", userID)

    // Search only user's namespace
    ctx := context.Background()
    results, err := r.index.Query(ctx, pinecone.QueryParams{
        Vector:         convertToVector(query),
        TopK:           topK * 2,
        Namespace:      namespace,
        IncludeMetadata: true,
        IncludeValues:   false,
    })

    if err != nil {
        return "", err
    }

    // Construct context for LLM
    var context strings.Builder
    for _, hit := range results.Matches {
        context.WriteString(fmt.Sprintf("Document %s: %v\n", hit.Id, hit.Metadata["content"]))
    }

    return context.String(), nil
}
```

### Recommendation Engine

```go
type RecommendationEngine struct {
    index *pinecone.Index
}

func NewRecommendationEngine(client *pinecone.Client, indexName string) *RecommendationEngine {
    return &RecommendationEngine{
        index: client.Index(indexName),
    }
}

func (r *RecommendationEngine) GetRecommendations(productID string, categoryFilter string, topK int) ([]pinecone.ScoredVector, error) {
    // Get similar products
    ctx := context.Background()
    results, err := r.index.Query(ctx, pinecone.QueryParams{
        Vector:         convertToVector(fmt.Sprintf("product_%s", productID)),
        TopK:           topK * 2,
        Namespace:      "products",
        IncludeMetadata: true,
        IncludeValues:   false,
    })

    if err != nil {
        return nil, err
    }

    // Apply category filtering if specified
    if categoryFilter != "" {
        var filteredResults []pinecone.ScoredVector
        for _, hit := range results.Matches {
            if hit.Metadata["category"] == categoryFilter {
                filteredResults = append(filteredResults, hit)
            }
        }

        if len(filteredResults) > topK {
            filteredResults = filteredResults[:topK]
        }

        return filteredResults, nil
    }

    if len(results.Matches) > topK {
        return results.Matches[:topK], nil
    }

    return results.Matches, nil
}
```

## HTTP Server Integration

```go
import (
    "encoding/json"
    "net/http"
)

type SearchHandler struct {
    searchSystem *SemanticSearchSystem
}

func NewSearchHandler(searchSystem *SemanticSearchSystem) *SearchHandler {
    return &SearchHandler{
        searchSystem: searchSystem,
    }
}

func (h *SearchHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    if r.Method != http.MethodPost {
        http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
        return
    }

    var req struct {
        Query    string `json:"query"`
        Category string `json:"category"`
        TopK     int    `json:"top_k"`
    }

    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        http.Error(w, "Invalid JSON", http.StatusBadRequest)
        return
    }

    results, err := h.searchSystem.SearchKnowledgeBase(req.Query, req.Category, req.TopK)
    if err != nil {
        http.Error(w, "Search failed", http.StatusInternalServerError)
        return
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(results)
}
```

## Configuration Files

```json
// config.json
{
  "pinecone_api_key": "your-api-key",
  "pinecone_index": "default-index"
}
```

```go
// main.go
func main() {
    config, err := loadConfig("config.json")
    if err != nil {
        panic(err)
    }

    client, err := pinecone.NewClient(pinecone.NewClientParams{
        ApiKey: config.PineconeAPIKey,
    })
    if err != nil {
        panic(err)
    }

    searchSystem := NewSemanticSearchSystem(client, config.PineconeIndex)

    http.Handle("/search", NewSearchHandler(searchSystem))
    http.ListenAndServe(":8080", nil)
}
```
