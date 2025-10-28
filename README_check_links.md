# Link Checker Script

## Summary of Results

✅ **Created**: `check_links.py` - A Python script to extract and verify external links in markdown files

### Link Check Results

**Total External Links Found**: 22 unique URLs

**Broken Links Found**: 1 ❌

### Broken Link Details

- **File**: `.agents/AGENTS-cli.md`
- **Line**: 233
- **URL**: `https://github.com/pinecone-io/cli/releases/latest/download/pinecone_linux_amd64.tar.gz`
- **Error**: 404 Not Found

**Issue**: This specific download URL format (`/latest/download/`) appears to be invalid. GitHub releases typically use format like `/releases/download/v1.0.0/filename`.

**Suggested Fix**: Replace with direct link to releases page or use Homebrew installation method shown elsewhere in the document.

## Usage

### Extract Links Only (No Checking)

```bash
python3 check_links.py --recursive --skip-check
```

### Check All Links

```bash
python3 check_links.py --recursive
```

### Check Specific Files

```bash
python3 check_links.py --files AGENTS.md .agents/AGENTS-cli.md
```

### Verbose Output (Show All Checks)

```bash
python3 check_links.py --recursive --verbose
```

### Custom Timeout

```bash
python3 check_links.py --recursive --timeout 5
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
