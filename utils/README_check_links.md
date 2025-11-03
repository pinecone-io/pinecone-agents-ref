# Link Checker Script

## Summary of Results

✅ **Created**: `check_links.py` - A Python script to extract and verify external links in markdown files

## Usage

### Extract Links Only (No Checking)

```bash
python3 utils/check_links.py --recursive --skip-check
```

### Check All Links

```bash
python3 utils/check_links.py --recursive
```

### Check Specific Files

```bash
python3 utils/check_links.py --files AGENTS.md .agents/AGENTS-cli.md
```

### Verbose Output (Show All Checks)

```bash
python3 utils/check_links.py --recursive --verbose
```

### Custom Timeout

```bash
python3 utils/check_links.py --recursive --timeout 5
```

## Command-Line Options

- `--files` - Check specific markdown files
- `--recursive, -r` - Recursively search for .md files in subdirectories
- `--timeout, -t` - Request timeout in seconds (default: 10)
- `--verbose, -v` - Show all links, not just broken ones
- `--skip-check` - Only extract links, do not check them

## External Links Summary

All external links point to:

- `docs.pinecone.io` - Pinecone official documentation
- `github.com/pinecone-io/cli` - Pinecone CLI GitHub repository
- `sdk.pinecone.io` - Pinecone SDK documentation

All other links (21 out of 22) are working correctly! ✅
