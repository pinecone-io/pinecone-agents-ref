# Pinecone Java SDK Guide

> **Prerequisites**: See [AGENTS.md](../AGENTS.md) for universal concepts and setup.

This guide provides Java-specific patterns, examples, and best practices for the Pinecone SDK.

## Installation & Setup

> **⚠️ IMPORTANT**: See [PINECONE.md](./PINECONE.md#-mandatory-always-use-latest-version) for the mandatory requirement to always use the latest version when creating projects.

### Finding the Latest Version

**Check latest version on Maven Central:**

- Browse: [https://repo1.maven.org/maven2/io/pinecone/pinecone-client/](https://repo1.maven.org/maven2/io/pinecone/pinecone-client/)
- Or check via CLI: `curl -s https://repo1.maven.org/maven2/io/pinecone/pinecone-client/maven-metadata.xml`

### Maven Dependency

**Install latest version:**

```xml
<dependency>
    <groupId>io.pinecone</groupId>
    <artifactId>pinecone-client</artifactId>
    <version>5.1.0</version>  <!-- Replace with desired version -->
</dependency>
```

### Gradle Dependency

**Install specific version:**

```gradle
implementation 'io.pinecone:pinecone-client:5.1.0'  // Replace with desired version
```

**Using dynamic version (not recommended for production):**

```gradle
implementation 'io.pinecone:pinecone-client:+'  // Gets latest, but can cause unexpected updates
// Or with version range
implementation 'io.pinecone:pinecone-client:[5.1.0,)'  // 5.1.0 or higher
```

**Check versions available (requires `gradle-versions-plugin`):**

```bash
# First add plugin to build.gradle:
# plugins { id 'com.github.ben-manes.versions' version '0.46.0' }

gradle dependencyUpdates
```

**Or check manually:**

```bash
# Check dependency version in your project
gradle dependencies | grep pinecone-client

# Or browse Maven Central directly
```

### Java Imports

```java
import io.pinecone.PineconeClient;
import io.pinecone.PineconeClientConfig;
import io.pinecone.PineconeConnection;
import io.pinecone.PineconeConnectionConfig;
import io.pinecone.gen.*;
```

### Environment Configuration

```java
import io.pinecone.PineconeClient;
import io.pinecone.PineconeClientConfig;

public class PineconeConfig {
    private static final String API_KEY = System.getenv("PINECONE_API_KEY");

    public static PineconeClient createClient() {
        if (API_KEY == null || API_KEY.isEmpty()) {
            throw new IllegalArgumentException("PINECONE_API_KEY environment variable not set");
        }

        PineconeClientConfig config = PineconeClientConfig.builder()
            .apiKey(API_KEY)
            .build();

        return new PineconeClient(config);
    }
}
```

### Production Client Class

```java
import io.pinecone.PineconeClient;
import io.pinecone.PineconeClientConfig;
import io.pinecone.PineconeConnection;
import io.pinecone.PineconeConnectionConfig;

public class PineconeService {
    private final PineconeClient client;
    private final String indexName;

    public PineconeService() {
        String apiKey = System.getenv("PINECONE_API_KEY");
        if (apiKey == null || apiKey.isEmpty()) {
            throw new IllegalArgumentException("PINECONE_API_KEY required");
        }

        PineconeClientConfig config = PineconeClientConfig.builder()
            .apiKey(apiKey)
            .build();

        this.client = new PineconeClient(config);
        this.indexName = System.getenv().getOrDefault("PINECONE_INDEX", "default-index");
    }

    public PineconeConnection getIndex() {
        PineconeConnectionConfig connectionConfig = PineconeConnectionConfig.builder()
            .indexName(indexName)
            .build();

        return client.connect(connectionConfig);
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

```java
import io.pinecone.PineconeClient;
import io.pinecone.PineconeClientConfig;
import io.pinecone.PineconeConnection;
import io.pinecone.PineconeConnectionConfig;
import io.pinecone.gen.*;
import java.util.*;

public class QuickStartExample {
    public static void main(String[] args) {
        // Initialize Pinecone client
        String apiKey = System.getenv("PINECONE_API_KEY");
        if (apiKey == null || apiKey.isEmpty()) {
            throw new IllegalArgumentException("PINECONE_API_KEY environment variable not set");
        }

        PineconeClientConfig config = PineconeClientConfig.builder()
            .apiKey(apiKey)
            .build();

        PineconeClient client = new PineconeClient(config);

        // Sample records
        List<Vector> records = Arrays.asList(
            Vector.builder()
                .id("rec1")
                .values(Arrays.asList(0.1f, 0.2f, 0.3f))
                .metadata(Map.of(
                    "content", "The Eiffel Tower was completed in 1889 and stands in Paris, France.",
                    "category", "history"
                ))
                .build(),
            Vector.builder()
                .id("rec2")
                .values(Arrays.asList(0.4f, 0.5f, 0.6f))
                .metadata(Map.of(
                    "content", "Photosynthesis allows plants to convert sunlight into energy.",
                    "category", "science"
                ))
                .build(),
            Vector.builder()
                .id("rec5")
                .values(Arrays.asList(0.7f, 0.8f, 0.9f))
                .metadata(Map.of(
                    "content", "Shakespeare wrote many famous plays, including Hamlet and Macbeth.",
                    "category", "literature"
                ))
                .build()
        );

        // Target the index
        PineconeConnectionConfig connectionConfig = PineconeConnectionConfig.builder()
            .indexName("agentic-quickstart-test")
            .build();

        PineconeConnection index = client.connect(connectionConfig);

        // Upsert the records into a namespace
        UpsertRequest upsertRequest = UpsertRequest.builder()
            .namespace("example-namespace")
            .vectors(records)
            .build();

        index.upsert(upsertRequest);
    }
}
```

3. **Search with reranking:**

```java
import java.util.concurrent.TimeUnit;

public class SearchExample {
    public static void main(String[] args) throws InterruptedException {
        // Wait for the upserted vectors to be indexed
        TimeUnit.SECONDS.sleep(10);

        // View stats for the index
        DescribeIndexStatsRequest statsRequest = DescribeIndexStatsRequest.builder().build();
        DescribeIndexStatsResponse stats = index.describeIndexStats(statsRequest);
        System.out.println("Stats: " + stats);

        // Define the query
        String query = "Famous historical structures and monuments";

        // Search the dense index
        QueryRequest queryRequest = QueryRequest.builder()
            .namespace("example-namespace")
            .vector(Arrays.asList(0.1f, 0.2f, 0.3f)) // This would be the actual query vector
            .topK(10)
            .includeMetadata(true)
            .build();

        QueryResponse results = index.query(queryRequest);

        // Print the results
        results.getMatches().forEach(hit -> {
            System.out.printf("id: %s | score: %.2f | category: %s | text: %s%n",
                hit.getId(),
                hit.getScore(),
                hit.getMetadata().get("category"),
                hit.getMetadata().get("content"));
        });
    }
}
```

## Data Operations

### Upserting Records

```java
import io.pinecone.gen.*;
import java.util.*;

public class DataOperations {
    private PineconeConnection index;

    public void upsertRecords() {
        // Indexes with integrated embeddings
        List<Vector> records = Arrays.asList(
            Vector.builder()
                .id("doc1")
                .values(Arrays.asList(0.1f, 0.2f, 0.3f)) // vector values
                .metadata(Map.of(
                    "content", "Your text content here",
                    "category", "documentation",
                    "created_at", "2025-01-01",
                    "priority", "high"
                ))
                .build()
        );

        // Always use namespaces
        String namespace = "user_123"; // e.g., "knowledge_base", "session_456"

        UpsertRequest upsertRequest = UpsertRequest.builder()
            .namespace(namespace)
            .vectors(records)
            .build();

        index.upsert(upsertRequest);
    }
}
```

### Updating Records

```java
public void updateRecords() {
    // Update existing records (use same upsert operation with existing IDs)
    List<Vector> updatedRecords = Arrays.asList(
        Vector.builder()
            .id("doc1") // existing record ID
            .values(Arrays.asList(0.4f, 0.5f, 0.6f))
            .metadata(Map.of(
                "content", "Updated content here",
                "category", "updated_docs", // can change metadata
                "last_modified", "2025-01-15"
            ))
            .build()
    );

    // Partial updates - only changed fields need to be included
    List<Vector> partialUpdate = Arrays.asList(
        Vector.builder()
            .id("doc1")
            .metadata(Map.of(
                "category", "urgent", // only updating category field
                "priority", "high"    // adding new field
            ))
            .build()
    );

    UpsertRequest upsertRequest = UpsertRequest.builder()
        .namespace(namespace)
        .vectors(updatedRecords)
        .build();

    index.upsert(upsertRequest);
}
```

### Fetching Records

```java
public void fetchRecords() {
    // Fetch single record
    FetchRequest fetchRequest = FetchRequest.builder()
        .namespace(namespace)
        .ids(Arrays.asList("doc1"))
        .build();

    FetchResponse result = index.fetch(fetchRequest);

    if (result.getVectors() != null && result.getVectors().containsKey("doc1")) {
        Vector record = result.getVectors().get("doc1");
        System.out.println("Content: " + record.getMetadata().get("content"));
        System.out.println("Metadata: " + record.getMetadata());
    }

    // Fetch multiple records
    FetchRequest multiFetchRequest = FetchRequest.builder()
        .namespace(namespace)
        .ids(Arrays.asList("doc1", "doc2", "doc3"))
        .build();

    FetchResponse multiResult = index.fetch(multiFetchRequest);

    multiResult.getVectors().forEach((recordId, record) -> {
        System.out.println("ID: " + recordId + ", Content: " + record.getMetadata().get("content"));
    });
}

// Fetch with error handling
public Map<String, Vector> safeFetch(String namespace, List<String> ids) {
    try {
        FetchRequest fetchRequest = FetchRequest.builder()
            .namespace(namespace)
            .ids(ids)
            .build();

        FetchResponse result = index.fetch(fetchRequest);
        return result.getVectors();
    } catch (Exception e) {
        System.err.println("Fetch failed: " + e.getMessage());
        return new HashMap<>();
    }
}
```

### Listing Record IDs

```java
public List<String> listAllIds(String namespace, String prefix) {
    List<String> allIds = new ArrayList<>();
    String paginationToken = null;

    while (true) {
        ListRequest.Builder listRequestBuilder = ListRequest.builder()
            .namespace(namespace)
            .limit(1000);

        if (prefix != null) {
            listRequestBuilder.prefix(prefix);
        }

        if (paginationToken != null) {
            listRequestBuilder.paginationToken(paginationToken);
        }

        ListResponse result = index.list(listRequestBuilder.build());

        result.getVectors().forEach(vector -> allIds.add(vector.getId()));

        if (result.getPagination() == null || result.getPagination().getNext() == null) {
            break;
        }
        paginationToken = result.getPagination().getNext();
    }

    return allIds;
}

// Usage
List<String> allRecordIds = listAllIds("user_123", null);
List<String> docsOnly = listAllIds("user_123", "doc_");
```

## Search Operations

### Semantic Search with Reranking (Best Practice)

```java
public QueryResponse searchWithRerank(String namespace, List<Float> queryVector, int topK) {
    // Standard search pattern - always rerank for production
    QueryRequest queryRequest = QueryRequest.builder()
        .namespace(namespace)
        .vector(queryVector)
        .topK(topK * 2) // more candidates for reranking
        .includeMetadata(true)
        .includeValues(false)
        .build();

    QueryResponse results = index.query(queryRequest);

    // Note: Reranking would need to be implemented separately
    // or using Pinecone's hosted reranking features
    return results;
}
```

### Lexical Search

```java
// Basic lexical search
public QueryResponse lexicalSearch(String namespace, List<Float> queryVector, int topK) {
    // Keyword-based search using sparse embeddings
    QueryRequest queryRequest = QueryRequest.builder()
        .namespace(namespace)
        .vector(queryVector)
        .topK(topK)
        .includeMetadata(true)
        .includeValues(false)
        .build();

    return index.query(queryRequest);
}

// Lexical search with required terms
public QueryResponse lexicalSearchWithRequiredTerms(
    String namespace,
    List<Float> queryVector,
    List<String> requiredTerms,
    int topK
) {
    // Results must contain specific required words
    Map<String, Object> filter = Map.of(
        "$in", Map.of("content", requiredTerms)
    );

    QueryRequest queryRequest = QueryRequest.builder()
        .namespace(namespace)
        .vector(queryVector)
        .topK(topK)
        .includeMetadata(true)
        .includeValues(false)
        .filter(filter)
        .build();

    return index.query(queryRequest);
}
```

### Metadata Filtering

```java
public QueryResponse searchWithFilters(String namespace, List<Float> queryVector) {
    // Simple filters
    Map<String, Object> simpleFilter = Map.of("category", "documentation");

    // Complex filters
    Map<String, Object> complexFilter = Map.of(
        "$and", Arrays.asList(
            Map.of("category", Map.of("$in", Arrays.asList("docs", "tutorial"))),
            Map.of("priority", Map.of("$ne", "low")),
            Map.of("created_at", Map.of("$gte", "2025-01-01"))
        )
    );

    QueryRequest queryRequest = QueryRequest.builder()
        .namespace(namespace)
        .vector(queryVector)
        .topK(10)
        .includeMetadata(true)
        .includeValues(false)
        .filter(complexFilter)
        .build();

    return index.query(queryRequest);
}

// Search without filters - omit the filter property
public QueryResponse searchWithoutFilters(String namespace, List<Float> queryVector) {
    QueryRequest queryRequest = QueryRequest.builder()
        .namespace(namespace)
        .vector(queryVector)
        .topK(10)
        .includeMetadata(true)
        .includeValues(false)
        .build();

    return index.query(queryRequest);
}

// Dynamic filter pattern - conditionally add filter
public QueryResponse searchWithDynamicFilter(String namespace, List<Float> queryVector, boolean hasFilters) {
    QueryRequest.Builder queryRequestBuilder = QueryRequest.builder()
        .namespace(namespace)
        .vector(queryVector)
        .topK(10)
        .includeMetadata(true)
        .includeValues(false);

    if (hasFilters) {
        Map<String, Object> filter = Map.of("category", Map.of("$eq", "docs"));
        queryRequestBuilder.filter(filter);
    }

    return index.query(queryRequestBuilder.build());
}
```

## Error Handling (Production)

### Retry Pattern

```java
import java.util.concurrent.TimeUnit;
import java.util.function.Supplier;

public class RetryUtils {
    public static <T> T exponentialBackoffRetry(Supplier<T> func, int maxRetries) throws Exception {
        for (int attempt = 0; attempt < maxRetries; attempt++) {
            try {
                return func.get();
            } catch (Exception e) {
                // Extract status code from exception
                int statusCode = extractStatusCode(e);

                // Only retry transient errors
                if (statusCode >= 500 || statusCode == 429) {
                    if (attempt < maxRetries - 1) {
                        long delay = Math.min((long) Math.pow(2, attempt), 60) * 1000; // Exponential backoff, cap at 60s
                        TimeUnit.MILLISECONDS.sleep(delay);
                    } else {
                        throw e;
                    }
                } else {
                    throw e; // Don't retry client errors (4xx except 429)
                }
            }
        }
        throw new RuntimeException("Max retries exceeded");
    }

    private static int extractStatusCode(Exception e) {
        // This would need to be implemented based on the actual exception structure
        // For now, return a default value
        return 500;
    }
}

// Usage
RetryUtils.exponentialBackoffRetry(() -> {
    UpsertRequest upsertRequest = UpsertRequest.builder()
        .namespace(namespace)
        .vectors(records)
        .build();
    return index.upsert(upsertRequest);
}, 5);
```

## Batch Processing

```java
public void batchUpsert(String namespace, List<Vector> records, int batchSize) throws Exception {
    for (int i = 0; i < records.size(); i += batchSize) {
        int endIndex = Math.min(i + batchSize, records.size());
        List<Vector> batch = records.subList(i, endIndex);

        RetryUtils.exponentialBackoffRetry(() -> {
            UpsertRequest upsertRequest = UpsertRequest.builder()
                .namespace(namespace)
                .vectors(batch)
                .build();
            return index.upsert(upsertRequest);
        }, 5);

        TimeUnit.MILLISECONDS.sleep(100); // Rate limiting
    }
}
```

## Common Operations

### Index Management

```java
public class IndexManagement {
    private PineconeClient client;

    // Check if index exists (in application startup)
    public boolean indexExists(String indexName) {
        try {
            ListIndexesRequest request = ListIndexesRequest.builder().build();
            ListIndexesResponse response = client.listIndexes(request);

            return response.getIndexes().stream()
                .anyMatch(index -> index.getName().equals(indexName));
        } catch (Exception e) {
            return false;
        }
    }

    // Get stats (for monitoring/metrics)
    public void printStats(String indexName) {
        PineconeConnectionConfig connectionConfig = PineconeConnectionConfig.builder()
            .indexName(indexName)
            .build();

        PineconeConnection index = client.connect(connectionConfig);

        DescribeIndexStatsRequest request = DescribeIndexStatsRequest.builder().build();
        DescribeIndexStatsResponse stats = index.describeIndexStats(request);

        System.out.println("Total vectors: " + stats.getTotalVectorCount());
        System.out.println("Namespaces: " + stats.getNamespaces().keySet());
    }
}
```

### Data Operations

```java
public class DataOperations {
    private PineconeConnection index;

    // Fetch records
    public void fetchRecords(String namespace, List<String> ids) {
        FetchRequest fetchRequest = FetchRequest.builder()
            .namespace(namespace)
            .ids(ids)
            .build();

        FetchResponse result = index.fetch(fetchRequest);

        result.getVectors().forEach((recordId, record) -> {
            System.out.println(recordId + ": " + record.getMetadata().get("content"));
        });
    }

    // List all IDs (paginated)
    public List<String> listAllIds(String namespace) {
        List<String> allIds = new ArrayList<>();
        String paginationToken = null;

        while (true) {
            ListRequest.Builder listRequestBuilder = ListRequest.builder()
                .namespace(namespace)
                .limit(1000);

            if (paginationToken != null) {
                listRequestBuilder.paginationToken(paginationToken);
            }

            ListResponse result = index.list(listRequestBuilder.build());

            result.getVectors().forEach(vector -> allIds.add(vector.getId()));

            if (result.getPagination() == null || result.getPagination().getNext() == null) {
                break;
            }
            paginationToken = result.getPagination().getNext();
        }

        return allIds;
    }

    // Delete records
    public void deleteRecords(String namespace, List<String> ids) {
        DeleteRequest deleteRequest = DeleteRequest.builder()
            .namespace(namespace)
            .ids(ids)
            .build();

        index.delete(deleteRequest);
    }

    // Delete entire namespace
    public void deleteNamespace(String namespace) {
        DeleteRequest deleteRequest = DeleteRequest.builder()
            .namespace(namespace)
            .deleteAll(true)
            .build();

        index.delete(deleteRequest);
    }
}
```

## Java-Specific Patterns

### Namespace Strategy

```java
public class NamespaceUtils {
    // Multi-user apps
    public static String userNamespace(String userId) {
        return "user_" + userId;
    }

    // Session-based
    public static String sessionNamespace(String sessionId) {
        return "session_" + sessionId;
    }

    // Content-based
    public static String knowledgeBaseNamespace() {
        return "knowledge_base";
    }

    public static String chatHistoryNamespace() {
        return "chat_history";
    }
}
```

### Configuration Management

```java
import java.util.Properties;
import java.io.FileInputStream;
import java.io.IOException;

public class PineconeConfigManager {
    private Properties properties;

    public PineconeConfigManager(String configFile) throws IOException {
        properties = new Properties();
        properties.load(new FileInputStream(configFile));
    }

    public PineconeClient createClient() {
        String apiKey = properties.getProperty("pinecone.api.key");
        if (apiKey == null || apiKey.isEmpty()) {
            throw new IllegalArgumentException("PINECONE_API_KEY required");
        }

        PineconeClientConfig config = PineconeClientConfig.builder()
            .apiKey(apiKey)
            .build();

        return new PineconeClient(config);
    }

    public String getIndexName() {
        return properties.getProperty("pinecone.index.name", "default-index");
    }
}
```

## Use Case Examples

### Semantic Search System

```java
public class SemanticSearchSystem {
    private PineconeConnection index;

    public QueryResponse searchKnowledgeBase(String query, String categoryFilter, int topK) {
        QueryRequest.Builder queryRequestBuilder = QueryRequest.builder()
            .namespace("knowledge_base")
            .vector(convertToVector(query)) // This would need to be implemented
            .topK(topK * 2)
            .includeMetadata(true)
            .includeValues(false);

        if (categoryFilter != null) {
            Map<String, Object> filter = Map.of("category", Map.of("$eq", categoryFilter));
            queryRequestBuilder.filter(filter);
        }

        QueryResponse results = index.query(queryRequestBuilder.build());

        return results;
    }

    private List<Float> convertToVector(String text) {
        // This would need to be implemented based on your embedding model
        return Arrays.asList(0.1f, 0.2f, 0.3f); // Placeholder
    }
}
```

### Multi-Tenant RAG System

```java
public class RagSystem {
    private PineconeConnection index;

    public String ragQuery(String userId, String query, int topK) {
        // Ensure namespace isolation
        String namespace = "user_" + userId;

        // Search only user's namespace
        QueryRequest queryRequest = QueryRequest.builder()
            .namespace(namespace)
            .vector(convertToVector(query))
            .topK(topK * 2)
            .includeMetadata(true)
            .includeValues(false)
            .build();

        QueryResponse results = index.query(queryRequest);

        // Construct context for LLM
        StringBuilder context = new StringBuilder();
        results.getMatches().forEach(hit -> {
            context.append("Document ").append(hit.getId())
                   .append(": ").append(hit.getMetadata().get("content"))
                   .append("\n");
        });

        return context.toString();
    }

    private List<Float> convertToVector(String text) {
        // This would need to be implemented based on your embedding model
        return Arrays.asList(0.1f, 0.2f, 0.3f); // Placeholder
    }
}
```

### Recommendation Engine

```java
public class RecommendationEngine {
    private PineconeConnection index;

    public List<ScoredVector> getRecommendations(String productId, String categoryFilter, int topK) {
        // Get similar products
        QueryRequest queryRequest = QueryRequest.builder()
            .namespace("products")
            .vector(convertToVector("product_" + productId))
            .topK(topK * 2)
            .includeMetadata(true)
            .includeValues(false)
            .build();

        QueryResponse results = index.query(queryRequest);

        // Apply category filtering if specified
        if (categoryFilter != null) {
            return results.getMatches().stream()
                .filter(hit -> categoryFilter.equals(hit.getMetadata().get("category")))
                .limit(topK)
                .collect(Collectors.toList());
        }

        return results.getMatches().stream()
            .limit(topK)
            .collect(Collectors.toList());
    }

    private List<Float> convertToVector(String text) {
        // This would need to be implemented based on your embedding model
        return Arrays.asList(0.1f, 0.2f, 0.3f); // Placeholder
    }
}
```

## Spring Boot Integration

```java
import org.springframework.stereotype.Service;
import org.springframework.beans.factory.annotation.Value;

@Service
public class PineconeService {
    private final PineconeClient client;
    private final String indexName;

    public PineconeService(@Value("${pinecone.api.key}") String apiKey,
                          @Value("${pinecone.index.name:default-index}") String indexName) {
        if (apiKey == null || apiKey.isEmpty()) {
            throw new IllegalArgumentException("PINECONE_API_KEY required");
        }

        PineconeClientConfig config = PineconeClientConfig.builder()
            .apiKey(apiKey)
            .build();

        this.client = new PineconeClient(config);
        this.indexName = indexName;
    }

    public PineconeConnection getIndex() {
        PineconeConnectionConfig connectionConfig = PineconeConnectionConfig.builder()
            .indexName(indexName)
            .build();

        return client.connect(connectionConfig);
    }
}
```

## Application Properties

```properties
# application.properties
pinecone.api.key=${PINECONE_API_KEY}
pinecone.index.name=${PINECONE_INDEX:default-index}
```
