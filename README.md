# Pinecone Agent Reference

This repository contains specialized agent instructions for the Pinecone vector database, designed to be integrated into your AI coding assistant's configuration file.

[AGENTS.md](https://agents.md/) is an open format used by over 20k open-source projects and is supported by most coding assistants including Cursor, Aider, GitHub Copilot, and many others.

## What's Included

This repository provides comprehensive Pinecone documentation organized into the `.agents/` folder:

- **PINECONE.md** - Universal concepts, CLI vs SDK guidance, common patterns, and navigation guide
- **PINECONE-quickstart.md** - Step-by-step tutorials (Quick Test, Search, RAG, Recommendations)
- **PINECONE-cli.md** - CLI installation, authentication, and command reference
- **PINECONE-python.md** - Python SDK guide with code examples
- **PINECONE-typescript.md** - TypeScript/Node.js SDK guide with code examples
- **PINECONE-go.md** - Go SDK guide with code examples
- **PINECONE-java.md** - Java SDK guide with code examples

## Quick Start

The general process is to download the latest release, extract the archive, and add the Pinecone section to your assistant's configuration file.

### Most Assistants (Cursor, Aider, GitHub Copilot, etc.)

**Linux/macOS (Bash/Zsh):**

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

Claude Code uses `CLAUDE.md` instead of `AGENTS.md`.

**Linux/macOS (Bash/Zsh):**

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

That's it! Your project now has the `.agents/` folder with all Pinecone documentation and your configuration file has been updated.

### Verify Installation

After running the commands above, you should have:

```
your-project/
├── .agents/                    # Agent documentation folder
│   ├── PINECONE.md             # Main universal guide
│   ├── PINECONE-quickstart.md  # Quickstart tutorials
│   ├── PINECONE-cli.md         # CLI documentation
│   ├── PINECONE-python.md      # Python SDK guide
│   ├── PINECONE-typescript.md  # TypeScript/Node.js SDK guide
│   ├── PINECONE-go.md          # Go SDK guide
│   └── PINECONE-java.md        # Java SDK guide
└── AGENTS.md                   # Your project's agent guide (with Pinecone section)

```

### Customizing the Integration

The third command appends `AGENTS-pinecone-snippet.md` to your `AGENTS.md`. If you already have an `AGENTS.md` file and want more control over where the Pinecone section is placed:

1. Extract the archive: `unzip agents.zip && rm agents.zip`
2. Open `AGENTS-pinecone-snippet.md` and copy the "Pinecone (Vector Database)" section
3. Manually add it to your `AGENTS.md` where you prefer
4. Remove the snippet file: `rm AGENTS-pinecone-snippet.md`

## Updating

To update to a newer version, simply download the latest release and extract the archive. Your configuration file (`AGENTS.md` or `CLAUDE.md` if using Claude Code) typically doesn't need changes unless the structure changes.

**Linux/macOS (Bash/Zsh):**

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

## Usage

Once installed, your AI coding assistant will automatically reference the `.agents/PINECONE.md` files when users ask questions about Pinecone. The main guide provides navigation to language-specific documentation based on the user's needs.

## For Maintainers: Creating Releases

The included GitHub Actions workflow (`.github/workflows/release.yml`) automatically packages and creates releases when you push a version tag.

### How to Create a Release

Simply tag and push your code:

```bash
git tag v1.0.0
git push origin v1.0.0
```

The workflow will automatically:

1. Detect the version tag (matches `v*` pattern, e.g., `v1.0.0`, `v2.1.3`)
2. Create a GitHub release if one doesn't already exist for that tag
3. Package all files from the `.agents/` folder
4. Include the `AGENTS-pinecone-snippet.md` file for easy integration
5. Create both `agents.zip` and `agents.tar.gz` archives
6. Attach both archives to the release as downloadable assets

### How It Works

The workflow triggers automatically on tag push (`push: tags: v*`) and:

1. Extracts the tag name (e.g., `v1.0.0`)
2. Checks if a GitHub release already exists for that tag
   - If a release exists → uses that release and attaches assets
   - If no release exists → creates a new release automatically
3. Packages the following files:
   - All files from `.agents/` folder (7 Pinecone documentation files)
   - `AGENTS-pinecone-snippet.md` file
4. Creates archives with the structure:
   ```
   archive/
   ├── .agents/
   │   ├── PINECONE.md
   │   ├── PINECONE-quickstart.md
   │   ├── PINECONE-cli.md
   │   ├── PINECONE-python.md
   │   ├── PINECONE-typescript.md
   │   ├── PINECONE-go.md
   │   └── PINECONE-java.md
   └── AGENTS-pinecone-snippet.md
   ```
5. Uploads both `agents.zip` and `agents.tar.gz` to the release

### Manual Release Option

You can still create releases manually through the GitHub UI if you prefer. If you create a release for a tag that doesn't have assets yet, you can manually trigger the workflow or just push the tag again to have it run automatically.

## Contributing

Issues and pull requests are welcome! Please see the repository's contribution guidelines (if available).

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.
