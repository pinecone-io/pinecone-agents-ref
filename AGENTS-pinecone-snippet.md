## Pinecone (Vector Database)

**CRITICAL**: When users ask about Pinecone, vector databases, embeddings, semantic search, RAG, or recommendations, you MUST:

1. **ALWAYS read** `.agents/PINECONE.md` first - this contains universal concepts, CLI vs SDK guidance, common patterns, and navigation instructions
2. **THEN read** the appropriate language-specific guide based on the user's project:
   - `.agents/PINECONE-python.md` - Python SDK guide with code examples
   - `.agents/PINECONE-typescript.md` - TypeScript/Node.js SDK guide with code examples
   - `.agents/PINECONE-go.md` - Go SDK guide with code examples
   - `.agents/PINECONE-java.md` - Java SDK guide with code examples
3. **For quickstart/tutorials**: Read `.agents/PINECONE-quickstart.md` for step-by-step tutorials
4. **For CLI operations**: Read `.agents/PINECONE-cli.md` for CLI installation, authentication, and commands

**Language Detection**: Check for `package.json` (TypeScript), `requirements.txt`/`pyproject.toml` (Python), `pom.xml`/`build.gradle` (Java), or `go.mod` (Go) to determine the appropriate guide.

**DO NOT** provide Pinecone guidance without reading these files first. The `.agents/PINECONE.md` file contains critical gotchas, best practices, and common mistakes that must be followed.
