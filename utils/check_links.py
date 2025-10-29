#!/usr/bin/env python3
"""
Script to check external links in markdown files for broken links (404s or other errors).
"""

import re
import sys
import os
from urllib.parse import urlparse
from pathlib import Path
import argparse
from typing import List, Tuple, Dict
import logging

# Try to import requests, fallback to urllib if not available
try:
    import requests
    USE_REQUESTS = True
except ImportError:
    import urllib.request
    import urllib.error
    USE_REQUESTS = False

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def extract_links_from_markdown(content: str) -> List[Tuple[str, int]]:
    """
    Extract all URLs from markdown content.
    Returns list of tuples: (url, line_number)
    """
    links = []
    
    # Pattern to match markdown links: [text](url)
    markdown_link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    
    # Pattern to match raw URLs
    raw_url_pattern = r'https?://[^\s\)]+'
    
    lines = content.split('\n')
    for line_num, line in enumerate(lines, start=1):
        seen_in_line = set()
        
        # Check for markdown links first (priority)
        for match in re.finditer(markdown_link_pattern, line):
            url = match.group(2).strip()
            # Clean any trailing markdown syntax that may have been captured
            if '](' in url:
                url = url.split('](')[0]
            if url.startswith('http') and url not in seen_in_line:
                links.append((url, line_num))
                seen_in_line.add(url)
        
        # Check for raw URLs only in parts not matched by markdown links
        # Remove markdown link patterns from line for raw URL extraction
        line_without_md = re.sub(markdown_link_pattern, '', line)
        for match in re.finditer(raw_url_pattern, line_without_md):
            url = match.group(0).strip()
            # Remove trailing punctuation
            url = url.rstrip('.,;:!?)')
            if url not in seen_in_line:
                links.append((url, line_num))
                seen_in_line.add(url)
    
    return links


def check_url(url: str, timeout: int = 10, allow_redirects: bool = True) -> Tuple[bool, int, str]:
    """
    Check if URL is accessible.
    Returns: (is_valid, status_code, error_message)
    """
    try:
        if USE_REQUESTS:
            response = requests.head(
                url,
                timeout=timeout,
                allow_redirects=allow_redirects,
                headers={'User-Agent': 'Mozilla/5.0 (compatible; LinkChecker/1.0)'}
            )
            status_code = response.status_code
            is_valid = status_code < 400
            error_message = f"{status_code} {response.reason}" if not is_valid else ""
        else:
            request = urllib.request.Request(url, method='HEAD')
            request.add_header('User-Agent', 'Mozilla/5.0 (compatible; LinkChecker/1.0)')
            try:
                with urllib.request.urlopen(request, timeout=timeout) as response:
                    status_code = response.status
                    is_valid = status_code < 400
                    error_message = f"{status_code}" if not is_valid else ""
            except urllib.error.HTTPError as e:
                status_code = e.code
                is_valid = status_code < 400
                error_message = f"{status_code} {e.reason}"
            
        return (is_valid, status_code, error_message)
    except Exception as e:
        return (False, 0, str(e))


def scan_file(file_path: Path) -> List[Dict]:
    """
    Scan a single markdown file for links.
    Returns list of link info dictionaries.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        links = extract_links_from_markdown(content)
        results = []
        
        for url, line_num in links:
            results.append({
                'file': str(file_path),
                'url': url,
                'line': line_num
            })
        
        return results
    except Exception as e:
        logger.error(f"Error reading {file_path}: {e}")
        return []


def main():
    parser = argparse.ArgumentParser(
        description='Check external links in markdown files for broken links.'
    )
    parser.add_argument(
        '--files',
        nargs='+',
        help='Specific markdown files to check (default: all .md files in current directory)'
    )
    parser.add_argument(
        '--recursive', '-r',
        action='store_true',
        help='Recursively search for markdown files'
    )
    parser.add_argument(
        '--timeout', '-t',
        type=int,
        default=10,
        help='Request timeout in seconds (default: 10)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show all links, not just broken ones'
    )
    parser.add_argument(
        '--skip-check',
        action='store_true',
        help='Only extract links, do not check them'
    )
    
    args = parser.parse_args()
    
    # Find markdown files
    if args.files:
        md_files = [Path(f) for f in args.files if f.endswith('.md')]
    else:
        md_files = list(Path('.').glob('**/*.md' if args.recursive else '*.md'))
    
    if not md_files:
        logger.warning("No markdown files found.")
        return 1
    
    logger.info(f"Found {len(md_files)} markdown file(s)")
    
    # Collect all links
    all_links = []
    for md_file in md_files:
        logger.info(f"Scanning: {md_file}")
        links = scan_file(md_file)
        all_links.extend(links)
    
    # Remove duplicates
    unique_links = {}
    for link_info in all_links:
        key = (link_info['file'], link_info['url'])
        if key not in unique_links:
            unique_links[key] = link_info
    
    logger.info(f"\nFound {len(unique_links)} unique external links")
    
    if args.skip_check:
        print("\nExternal links found:")
        for link_info in unique_links.values():
            print(f"  {link_info['file']}:{link_info['line']} - {link_info['url']}")
        return 0
    
    # Check links
    print("\nChecking links...")
    broken_links = []
    checked = 0
    
    for link_info in unique_links.values():
        url = link_info['url']
        checked += 1
        print(f"[{checked}/{len(unique_links)}] Checking: {url}")
        
        is_valid, status_code, error = check_url(url, timeout=args.timeout)
        
        if args.verbose:
            if is_valid:
                print(f"  ✓ {status_code} - OK")
            else:
                print(f"  ✗ {error}")
        
        if not is_valid:
            broken_links.append({
                **link_info,
                'status_code': status_code,
                'error': error
            })
    
    # Report results
    print("\n" + "="*80)
    if broken_links:
        print(f"\n❌ Found {len(broken_links)} broken link(s):\n")
        for link in broken_links:
            print(f"  File: {link['file']}")
            print(f"  Line: {link['line']}")
            print(f"  URL:  {link['url']}")
            print(f"  Error: {link['error']}")
            print()
        return 1
    else:
        print("\n✓ All links are working!")
        return 0


if __name__ == '__main__':
    sys.exit(main())

