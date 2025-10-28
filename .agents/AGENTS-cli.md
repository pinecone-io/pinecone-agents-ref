# Pinecone CLI Guide

> **Prerequisites**: See [AGENTS.md](../AGENTS.md) for universal concepts and CLI vs SDK guidance.
>
> **Getting Started?** See [Quickstart Guide](./AGENTS-quickstart.md) for step-by-step tutorials.

This guide provides comprehensive CLI setup, authentication, and command reference for Pinecone.

## Installation

### macOS (Homebrew)

```bash
brew tap pinecone-io/tap
brew install pinecone-io/tap/pinecone

# Upgrade later
brew update && brew upgrade pinecone
```

### Other Platforms

Download from [GitHub Releases](https://github.com/pinecone-io/cli/releases) (Linux, Windows, macOS)

## Authentication

Choose one method:

### Option 1: User Login (Recommended for Development)

```bash
pc login
pc target -o "my-org" -p "my-project"
```

### Option 2: API Key

```bash
export PINECONE_API_KEY="your-api-key"
# Or: pc auth configure --global-api-key <api-key>
```

### Option 3: Service Account

```bash
export PINECONE_CLIENT_ID="your-client-id"
export PINECONE_CLIENT_SECRET="your-client-secret"
```

**Full CLI reference:** [https://docs.pinecone.io/reference/cli/command-reference](https://docs.pinecone.io/reference/cli/command-reference)

## Index Management

### Creating Indexes

**Create index with integrated embeddings (preferred):**

```bash
pc index create -n my-index -m cosine -c aws -r us-east-1 \
  --model llama-text-embed-v2 \
  --field_map text=content
```

**Create serverless index without integrated embeddings:**

```bash
pc index create-serverless -n my-index -m cosine -c aws -r us-east-1 \
  --dimension 1536
```

### Available Embedding Models

- `llama-text-embed-v2`: High-performance, configurable dimensions, recommended for most use cases
- `multilingual-e5-large`: For multilingual content, 1024 dimensions
- `pinecone-sparse-english-v0`: For keyword/hybrid search scenarios

### Other Index Operations

```bash
# List indexes
pc index list

# Describe index
pc index describe --name my-index

# Configure index (replicas, deletion protection)
pc index configure --name my-index --replicas 3

# Delete index
pc index delete --name my-index
```

## API Key Management

```bash
# Create API key
pc api-key create

# List API keys
pc api-key list

# Delete API key
pc api-key delete --key-id <key-id>
```

## Common CLI Patterns

### Development Setup

```bash
# 1. Install CLI
brew tap pinecone-io/tap && brew install pinecone-io/tap/pinecone

# 2. Authenticate
pc login
pc target -o "my-org" -p "my-project"

# 3. Create index
pc index create -n my-dev-index -m cosine -c aws -r us-east-1 \
  --model llama-text-embed-v2 --field_map text=content

# 4. Verify setup
pc index list
pc index describe --name my-dev-index
```

### Production Deployment

```bash
# Create production index with higher replicas
pc index create -n my-prod-index -m cosine -c aws -r us-east-1 \
  --model llama-text-embed-v2 --field_map text=content \
  --replicas 3

# Configure deletion protection
pc index configure --name my-prod-index --deletion-protection true
```

### Multi-Environment Setup

```bash
# Development
pc index create -n my-app-dev -m cosine -c aws -r us-east-1 \
  --model llama-text-embed-v2 --field_map text=content

# Staging
pc index create -n my-app-staging -m cosine -c aws -r us-east-1 \
  --model llama-text-embed-v2 --field_map text=content

# Production
pc index create -n my-app-prod -m cosine -c aws -r us-east-1 \
  --model llama-text-embed-v2 --field_map text=content \
  --replicas 3 --deletion-protection true
```

## CLI Troubleshooting

### Common Issues

| Issue                   | Solution                                                                         |
| ----------------------- | -------------------------------------------------------------------------------- |
| `pc: command not found` | Install CLI: `brew tap pinecone-io/tap && brew install pinecone-io/tap/pinecone` |
| `Authentication failed` | Run `pc login` or set `PINECONE_API_KEY` environment variable                    |
| `Index already exists`  | Use different name or delete existing: `pc index delete --name <name>`           |
| `Permission denied`     | Check API key permissions or organization access                                 |

### Verification Commands

```bash
# Check CLI version
pc version

# Verify authentication
pc index list

# Check index status
pc index describe --name my-index

# View index stats
pc index stats --name my-index
```

## CLI vs SDK Decision Matrix

| Task                       | Use CLI | Use SDK |
| -------------------------- | ------- | ------- |
| One-time index creation    | ✅      | ❌      |
| Development setup          | ✅      | ❌      |
| Automated deployment       | ✅      | ✅      |
| Application startup checks | ❌      | ✅      |
| Dynamic index creation     | ❌      | ✅      |
| Data operations            | ❌      | ✅      |
| Runtime index management   | ❌      | ✅      |

## Best Practices

### For Development

- Use CLI for initial setup and testing
- Create indexes with descriptive names (e.g., `my-app-dev`)
- Use integrated embeddings for simplicity

### For Production

- Use CLI in deployment pipelines
- Configure appropriate replicas and deletion protection
- Use environment-specific index names
- Document all CLI commands used in deployment

### For Teams

- Share CLI setup instructions in README
- Use consistent naming conventions
- Document authentication method used
- Version control deployment scripts

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: Deploy Pinecone Index
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install Pinecone CLI
        run: |
          curl -L https://github.com/pinecone-io/cli/releases/latest/download/pinecone_linux_amd64.tar.gz | tar xz
          sudo mv pinecone /usr/local/bin/

      - name: Create Production Index
        run: |
          pc auth configure --api-key ${{ secrets.PINECONE_API_KEY }}
          pc index create -n my-app-prod -m cosine -c aws -r us-east-1 \
            --model llama-text-embed-v2 --field_map text=content \
            --replicas 3 --deletion-protection true
        env:
          PINECONE_API_KEY: ${{ secrets.PINECONE_API_KEY }}
```

### Docker Integration

```dockerfile
# Install Pinecone CLI in Docker image
FROM alpine:latest
RUN apk add --no-cache curl
RUN curl -L https://github.com/pinecone-io/cli/releases/latest/download/pinecone_linux_amd64.tar.gz | tar xz -C /usr/local/bin/
COPY deploy-index.sh /scripts/
RUN chmod +x /scripts/deploy-index.sh
```

## Advanced Usage

### Batch Operations

```bash
# Create multiple indexes
for env in dev staging prod; do
  pc index create -n my-app-$env -m cosine -c aws -r us-east-1 \
    --model llama-text-embed-v2 --field_map text=content
done
```

### Index Migration

```bash
# Export index configuration
pc index describe --name old-index > old-index-config.json

# Create new index with same configuration
pc index create -n new-index -m cosine -c aws -r us-east-1 \
  --model llama-text-embed-v2 --field_map text=content

# Delete old index after migration
pc index delete --name old-index
```

## Resources

- **Official CLI Documentation**: [https://docs.pinecone.io/reference/cli/command-reference](https://docs.pinecone.io/reference/cli/command-reference)
- **CLI GitHub Repository**: [https://github.com/pinecone-io/cli](https://github.com/pinecone-io/cli)
- **CLI Releases**: [https://github.com/pinecone-io/cli/releases](https://github.com/pinecone-io/cli/releases)
- **CLI Examples**: [https://docs.pinecone.io/guides/cli](https://docs.pinecone.io/guides/cli)
