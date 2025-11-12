# Pinecone Agent Reference

Specialized agent instructions for the Pinecone vector database, designed to enhance your AI coding assistant's understanding of Pinecone.

This project uses the [AGENTS.md format](https://agents.md/)—an open format used by over 20k open-source projects and supported by most coding assistants including Cursor, Aider, GitHub Copilot, and many others.

## Quick Start

Download the latest release and run the installation command for your assistant:

### Most Assistants (Cursor, Aider, GitHub Copilot, etc.)

**Linux/macOS:**

```bash
curl -L -o agents.zip https://github.com/pinecone-io/pinecone-agents-ref/releases/latest/download/agents.zip
unzip agents.zip && rm agents.zip
touch AGENTS.md && cat AGENTS-pinecone-snippet.md >> AGENTS.md && rm AGENTS-pinecone-snippet.md
```

**Windows (PowerShell):**

```powershell
Invoke-WebRequest -Uri https://github.com/pinecone-io/pinecone-agents-ref/releases/latest/download/agents.zip -OutFile agents.zip
Expand-Archive -Path agents.zip -DestinationPath . -Force
Remove-Item agents.zip
if (-not (Test-Path AGENTS.md)) { New-Item -Path AGENTS.md -ItemType File }
Add-Content -Path AGENTS.md -Value (Get-Content AGENTS-pinecone-snippet.md)
Remove-Item AGENTS-pinecone-snippet.md
```

### Claude Code

Uses `CLAUDE.md` instead of `AGENTS.md`.

**Linux/macOS:**

```bash
curl -L -o agents.zip https://github.com/pinecone-io/pinecone-agents-ref/releases/latest/download/agents.zip
unzip agents.zip && rm agents.zip
touch CLAUDE.md && cat AGENTS-pinecone-snippet.md >> CLAUDE.md && rm AGENTS-pinecone-snippet.md
```

**Windows (PowerShell):**

```powershell
Invoke-WebRequest -Uri https://github.com/pinecone-io/pinecone-agents-ref/releases/latest/download/agents.zip -OutFile agents.zip
Expand-Archive -Path agents.zip -DestinationPath . -Force
Remove-Item agents.zip
if (-not (Test-Path CLAUDE.md)) { New-Item -Path CLAUDE.md -ItemType File }
Add-Content -Path CLAUDE.md -Value (Get-Content AGENTS-pinecone-snippet.md)
Remove-Item AGENTS-pinecone-snippet.md
```

### Gemini CLI

Uses `GEMINI.md` context files instead of `AGENTS.md`.

**Linux/macOS:**

```bash
curl -L -o agents.zip https://github.com/pinecone-io/pinecone-agents-ref/releases/latest/download/agents.zip
unzip agents.zip && rm agents.zip
touch GEMINI.md && cat AGENTS-pinecone-snippet.md >> GEMINI.md && rm AGENTS-pinecone-snippet.md
```

**Windows (PowerShell):**

```powershell
Invoke-WebRequest -Uri https://github.com/pinecone-io/pinecone-agents-ref/releases/latest/download/agents.zip -OutFile agents.zip
Expand-Archive -Path agents.zip -DestinationPath . -Force
Remove-Item agents.zip
if (-not (Test-Path GEMINI.md)) { New-Item -Path GEMINI.md -ItemType File }
Add-Content -Path GEMINI.md -Value (Get-Content AGENTS-pinecone-snippet.md)
Remove-Item AGENTS-pinecone-snippet.md
```

**Note:** After installation, use `/memory refresh` in Gemini CLI to reload context files.

### After Installation

1. **Wait for re-indexing**: Most assistants need a few moments to recognize the new `.agents/` folder and configuration file.
2. **Verify installation**: You should now have:
   ```
   your-project/
   ├── .agents/
   │   ├── PINECONE.md
   │   ├── PINECONE-quickstart.md
   │   ├── PINECONE-cli.md
   │   ├── PINECONE-python.md
   │   ├── PINECONE-typescript.md
   │   ├── PINECONE-go.md
   │   ├── PINECONE-java.md
   │   └── PINECONE-troubleshooting.md
   └── AGENTS.md (or CLAUDE.md or GEMINI.md)
   ```

## What's Included

Comprehensive Pinecone documentation organized in the `.agents/` folder:

- **PINECONE.md** - Universal concepts, CLI vs SDK guidance, common patterns, and navigation guide
- **PINECONE-quickstart.md** - Step-by-step tutorials (Quick Test, Search, RAG, Recommendations)
- **PINECONE-cli.md** - CLI installation, authentication, and command reference
- **PINECONE-python.md** - Python SDK guide with code examples
- **PINECONE-typescript.md** - TypeScript/Node.js SDK guide with code examples
- **PINECONE-go.md** - Go SDK guide with code examples
- **PINECONE-java.md** - Java SDK guide with code examples
- **PINECONE-troubleshooting.md** - Common issues, solutions, and debugging tips

## How It Works

When you install this reference, two things are added to your project:

1. **`.agents/` folder** - Contains comprehensive Pinecone documentation files
2. **Configuration snippet** - Added to your `AGENTS.md` (or `CLAUDE.md`/`GEMINI.md`) that instructs your assistant to read from the `.agents/` folder

When users ask about Pinecone, your assistant will:

- Read the configuration file and see the Pinecone directive
- Consult `.agents/PINECONE.md` first
- Navigate to language-specific or topic-specific documentation as needed
- Provide accurate, context-aware answers based on the comprehensive documentation

This ensures your assistant has access to curated, up-to-date Pinecone documentation including current best practices, language-specific implementations, common pitfalls, and troubleshooting guides.

## Usage

Once installed and re-indexed, your AI coding assistant will automatically reference the `.agents/PINECONE.md` files when users ask questions about Pinecone. The main guide provides navigation to language-specific documentation based on the user's needs.

## Updating

To update to a newer version:

**Linux/macOS:**

```bash
curl -L -o agents.zip https://github.com/pinecone-io/pinecone-agents-ref/releases/latest/download/agents.zip
rm -rf .agents/PINECONE* && unzip agents.zip && rm agents.zip
```

**Windows (PowerShell):**

```powershell
Invoke-WebRequest -Uri https://github.com/pinecone-io/pinecone-agents-ref/releases/latest/download/agents.zip -OutFile agents.zip
Remove-Item .agents\PINECONE*
Expand-Archive -Path agents.zip -DestinationPath . -Force
Remove-Item agents.zip
```

Your configuration file (`AGENTS.md`, `CLAUDE.md`, or `GEMINI.md`) typically doesn't need changes unless the structure changes.

## Customizing Installation

If you already have a configuration file and want more control over where the Pinecone section is placed:

1. Extract the archive: `unzip agents.zip && rm agents.zip`
2. Open `AGENTS-pinecone-snippet.md` and copy the "Pinecone (Vector Database)" section
3. Manually add it to your configuration file (`AGENTS.md`, `CLAUDE.md`, or `GEMINI.md`) where you prefer
4. Remove the snippet file

---

## For Maintainers

### Creating Releases

The included GitHub Actions workflow (`.github/workflows/release.yml`) automatically packages and creates releases when you push a version tag.

**To create a release:**

```bash
git tag v1.0.0
git push origin v1.0.0
```

The workflow will:

1. Detect the version tag (matches `v*` pattern)
2. Create a GitHub release if one doesn't already exist
3. Package all files from the `.agents/` folder and `AGENTS-pinecone-snippet.md`
4. Create both `agents.zip` and `agents.tar.gz` archives
5. Attach both archives to the release

**Archive structure:**

```
archive/
├── .agents/
│   ├── PINECONE.md
│   ├── PINECONE-quickstart.md
│   ├── PINECONE-cli.md
│   ├── PINECONE-python.md
│   ├── PINECONE-typescript.md
│   ├── PINECONE-go.md
│   ├── PINECONE-java.md
│   └── PINECONE-troubleshooting.md
└── AGENTS-pinecone-snippet.md
```

You can also create releases manually through the GitHub UI. If a release exists for a tag but doesn't have assets yet, you can manually trigger the workflow or push the tag again.

---

## Contributing

Issues and pull requests are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines and instructions.

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.
