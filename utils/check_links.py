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


def is_downloadable_file(url: str, content_type: str = None) -> bool:
    """
    Check if URL points to a downloadable file (not HTML).
    Checks both URL extension and Content-Type header.
    """
    # Check Content-Type header first if available
    if content_type:
        content_type_lower = content_type.lower()
        # If it's clearly HTML, it's not a downloadable file
        if 'text/html' in content_type_lower:
            return False
        # If it's a known file type, it's downloadable
        file_type_indicators = [
            'application/pdf',
            'application/zip',
            'application/x-zip',
            'application/gzip',
            'application/x-gzip',
            'application/octet-stream',
            'image/',
            'video/',
            'audio/',
            'application/json',  # JSON files
            'text/plain',  # Plain text files (but not HTML)
        ]
        if any(indicator in content_type_lower for indicator in file_type_indicators):
            return True
    
    # Check URL extension as fallback
    url_lower = url.lower()
    file_extensions = [
        '.pdf', '.zip', '.gz', '.tar', '.rar', '.7z',
        '.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp', '.ico',
        '.mp4', '.mp3', '.avi', '.mov', '.wmv',
        '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
        '.csv', '.tsv', '.json', '.xml',
        '.exe', '.dmg', '.deb', '.rpm',
    ]
    return any(url_lower.endswith(ext) for ext in file_extensions)


def check_url(url: str, timeout: int = 10, allow_redirects: bool = True) -> Tuple[bool, int, str]:
    """
    Check if URL is accessible.
    Returns: (is_valid, status_code, error_message)
    Uses HEAD request first to avoid downloading files, falls back to GET for HTML pages
    that may need content verification for false 404 detection.
    """
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; LinkChecker/1.0)'}
        MAX_BODY_SIZE = 8192  # Only read first 8KB for HTML content verification
        
        if USE_REQUESTS:
            # Try HEAD request first (doesn't download body)
            try:
                head_response = requests.head(
                    url,
                    timeout=timeout,
                    allow_redirects=allow_redirects,
                    headers=headers
                )
                status_code = head_response.status_code
                content_type = head_response.headers.get('Content-Type', '')
                
                # Check if page is valid
                is_valid = status_code < 400
                
                # If it's a downloadable file, just use HEAD result (no need to download)
                if is_downloadable_file(url, content_type):
                    error_message = f"{status_code} {head_response.reason}" if not is_valid else ""
                    return (is_valid, status_code, error_message)
                
                # For HTML pages with 200 status, verify it's not a false 404
                # by downloading a small portion
                if is_valid and status_code == 200:
                    # Use GET with stream=True to limit download size
                    get_response = requests.get(
                        url,
                        timeout=timeout,
                        allow_redirects=allow_redirects,
                        headers=headers,
                        stream=True
                    )
                    # Read only first MAX_BODY_SIZE bytes
                    content_chunk = b''
                    for chunk in get_response.iter_content(chunk_size=1024):
                        content_chunk += chunk
                        if len(content_chunk) >= MAX_BODY_SIZE:
                            break
                    
                    content_lower = content_chunk.decode('utf-8', errors='ignore').lower()
                    
                    # Extract title tag content
                    title_pattern = r'<title[^>]*>(.*?)</title>'
                    title_matches = re.findall(title_pattern, content_lower, re.DOTALL | re.IGNORECASE)
                    if title_matches:
                        title_text = title_matches[0].strip()
                        # Check for various 404 indicators in title
                        if any(phrase in title_text for phrase in [
                            'page not found',
                            'not found',
                            '404',
                            'page does not exist',
                            'couldn\'t find the page',
                            'we couldn\'t find'
                        ]):
                            is_valid = False
                            error_message = f"200 (but page shows '{title_matches[0].strip()}' in title)"
                        else:
                            error_message = ""
                    else:
                        # No title tag found, check body content for 404 indicators
                        if 'page not found' in content_lower[:MAX_BODY_SIZE] or '404' in content_lower[:MAX_BODY_SIZE]:
                            is_valid = False
                            error_message = "200 (but page content suggests 404)"
                        else:
                            error_message = ""
                else:
                    error_message = f"{status_code} {head_response.reason}" if not is_valid else ""
                    
            except requests.exceptions.RequestException as e:
                # If HEAD fails (e.g., 405 Method Not Allowed), try GET with limited size
                try:
                    get_response = requests.get(
                        url,
                        timeout=timeout,
                        allow_redirects=allow_redirects,
                        headers=headers,
                        stream=True
                    )
                    status_code = get_response.status_code
                    content_type = get_response.headers.get('Content-Type', '')
                    
                    is_valid = status_code < 400
                    
                    # If it's a downloadable file, don't read body
                    if is_downloadable_file(url, content_type):
                        error_message = f"{status_code} {get_response.reason}" if not is_valid else ""
                        return (is_valid, status_code, error_message)
                    
                    # For HTML with 200, check content (already streaming, limit read)
                    if is_valid and status_code == 200:
                        content_chunk = b''
                        for chunk in get_response.iter_content(chunk_size=1024):
                            content_chunk += chunk
                            if len(content_chunk) >= MAX_BODY_SIZE:
                                break
                        
                        content_lower = content_chunk.decode('utf-8', errors='ignore').lower()
                        title_pattern = r'<title[^>]*>(.*?)</title>'
                        title_matches = re.findall(title_pattern, content_lower, re.DOTALL | re.IGNORECASE)
                        if title_matches:
                            title_text = title_matches[0].strip()
                            if any(phrase in title_text for phrase in [
                                'page not found',
                                'not found',
                                '404',
                                'page does not exist',
                                'couldn\'t find the page',
                                'we couldn\'t find'
                            ]):
                                is_valid = False
                                error_message = f"200 (but page shows '{title_matches[0].strip()}' in title)"
                            else:
                                error_message = ""
                        else:
                            if 'page not found' in content_lower[:MAX_BODY_SIZE] or '404' in content_lower[:MAX_BODY_SIZE]:
                                is_valid = False
                                error_message = "200 (but page content suggests 404)"
                            else:
                                error_message = ""
                    else:
                        error_message = f"{status_code} {get_response.reason}" if not is_valid else ""
                except Exception as inner_e:
                    return (False, 0, str(inner_e))
        else:
            # Fallback to urllib
            # Try HEAD first
            try:
                head_request = urllib.request.Request(url, headers=headers, method='HEAD')
                try:
                    with urllib.request.urlopen(head_request, timeout=timeout) as response:
                        status_code = response.status
                        content_type = response.headers.get('Content-Type', '')
                        is_valid = status_code < 400
                        
                        # If downloadable file, just use HEAD result
                        if is_downloadable_file(url, content_type):
                            error_message = f"{status_code}" if not is_valid else ""
                            return (is_valid, status_code, error_message)
                        
                        # For HTML with 200, need to verify with GET (limited)
                        if is_valid and status_code == 200:
                            # Use GET but read limited amount
                            get_request = urllib.request.Request(url, headers=headers)
                            with urllib.request.urlopen(get_request, timeout=timeout) as get_response:
                                content = get_response.read(MAX_BODY_SIZE).decode('utf-8', errors='ignore').lower()
                                title_pattern = r'<title[^>]*>(.*?)</title>'
                                title_matches = re.findall(title_pattern, content, re.DOTALL | re.IGNORECASE)
                                if title_matches:
                                    title_text = title_matches[0].strip()
                                    if any(phrase in title_text for phrase in [
                                        'page not found',
                                        'not found',
                                        '404',
                                        'page does not exist',
                                        'couldn\'t find the page',
                                        'we couldn\'t find'
                                    ]):
                                        is_valid = False
                                        error_message = f"200 (but page shows '{title_matches[0].strip()}' in title)"
                                    else:
                                        error_message = ""
                                else:
                                    if 'page not found' in content[:MAX_BODY_SIZE] or '404' in content[:MAX_BODY_SIZE]:
                                        is_valid = False
                                        error_message = "200 (but page content suggests 404)"
                                    else:
                                        error_message = ""
                        else:
                            error_message = f"{status_code}" if not is_valid else ""
                except urllib.error.HTTPError as e:
                    status_code = e.code
                    is_valid = status_code < 400
                    error_message = f"{status_code} {e.reason}"
            except (urllib.error.URLError, ValueError) as e:
                # HEAD not supported or failed, try GET with limited read
                try:
                    get_request = urllib.request.Request(url, headers=headers)
                    with urllib.request.urlopen(get_request, timeout=timeout) as response:
                        status_code = response.status
                        content_type = response.headers.get('Content-Type', '')
                        is_valid = status_code < 400
                        
                        # If downloadable file, don't read more than headers
                        if is_downloadable_file(url, content_type):
                            error_message = f"{status_code}" if not is_valid else ""
                            return (is_valid, status_code, error_message)
                        
                        # For HTML with 200, read limited content
                        if is_valid and status_code == 200:
                            content = response.read(MAX_BODY_SIZE).decode('utf-8', errors='ignore').lower()
                            title_pattern = r'<title[^>]*>(.*?)</title>'
                            title_matches = re.findall(title_pattern, content, re.DOTALL | re.IGNORECASE)
                            if title_matches:
                                title_text = title_matches[0].strip()
                                if any(phrase in title_text for phrase in [
                                    'page not found',
                                    'not found',
                                    '404',
                                    'page does not exist',
                                    'couldn\'t find the page',
                                    'we couldn\'t find'
                                ]):
                                    is_valid = False
                                    error_message = f"200 (but page shows '{title_matches[0].strip()}' in title)"
                                else:
                                    error_message = ""
                            else:
                                if 'page not found' in content[:MAX_BODY_SIZE] or '404' in content[:MAX_BODY_SIZE]:
                                    is_valid = False
                                    error_message = "200 (but page content suggests 404)"
                                else:
                                    error_message = ""
                        else:
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

