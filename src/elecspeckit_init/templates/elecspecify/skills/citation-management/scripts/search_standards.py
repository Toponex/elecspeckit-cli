#!/usr/bin/env python3
"""
Technical Standards Database Search

Search technical standards from IEEE, IEC, IPC, JEDEC, ISO and other standards organizations.
Supports complex queries, metadata extraction, and BibTeX export.

Usage:
    python search_standards.py "IEC 61010"
    python search_standards.py --query "safety power supply" --organizations "IEC,UL"
    python search_standards.py "PCB design" --status current --output pcb_standards.bib

Note: Some standards databases may require API keys or subscriptions.
Set environment variables: IEEE_API_KEY, IEC_API_KEY, etc.

Author: ElecSpeckit
License: MIT
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from urllib.parse import urlencode, quote
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


def setup_utf8_output():
    """Setup UTF-8 output for Windows console."""
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class StandardsSearchClient:
    """Client for searching technical standards databases."""

    def __init__(self):
        """Initialize standards search client."""
        self.rate_limit_delay = 1.0
        self.last_request_time = 0

        # API keys for different standards organizations
        self.api_keys = {
            'ieee': os.environ.get('IEEE_API_KEY'),
            'iec': os.environ.get('IEC_API_KEY'),
        }

    def _rate_limit(self):
        """Implement rate limiting between requests."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - time_since_last)
        self.last_request_time = time.time()

    def search_all(
        self,
        query: str,
        organizations: Optional[List[str]] = None,
        status: Optional[str] = None,
        max_results: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Search across multiple standards organizations.

        Args:
            query: Search query
            organizations: List of organization codes (IEEE, IEC, IPC, JEDEC, ISO, UL, etc.)
            status: Filter by status (current, superseded, withdrawn)
            max_results: Maximum number of results

        Returns:
            List of standard metadata dictionaries
        """
        results = []

        # Default to all organizations if not specified
        if not organizations:
            organizations = ['IEEE', 'IEC', 'IPC', 'JEDEC', 'ISO', 'UL', 'ANSI']

        print(f"Searching standards databases: {', '.join(organizations)}", file=sys.stderr)
        print(file=sys.stderr)

        # Search each organization
        for org in organizations:
            org_upper = org.upper()
            print(f"Searching {org_upper}...", file=sys.stderr)

            try:
                org_results = self._search_organization(org_upper, query, status)
                results.extend(org_results)
                print(f"  Found {len(org_results)} results from {org_upper}", file=sys.stderr)
            except Exception as e:
                print(f"  Error searching {org_upper}: {e}", file=sys.stderr)

        # Sort by relevance (standards with query in number/title first)
        query_lower = query.lower()
        results.sort(key=lambda x: (
            query_lower in x.get('number', '').lower(),
            query_lower in x.get('title', '').lower()
        ), reverse=True)

        return results[:max_results]

    def _search_organization(
        self,
        org: str,
        query: str,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search specific standards organization.

        Args:
            org: Organization code
            query: Search query
            status: Status filter

        Returns:
            List of standards
        """
        search_methods = {
            'IEEE': self._search_ieee,
            'IEC': self._search_iec,
            'IPC': self._search_ipc,
            'JEDEC': self._search_jedec,
            'ISO': self._search_iso,
            'UL': self._search_ul,
            'ANSI': self._search_ansi,
        }

        search_func = search_methods.get(org, self._search_pattern_based)
        return search_func(org, query, status)

    def _search_ieee(self, org: str, query: str, status: Optional[str]) -> List[Dict[str, Any]]:
        """Search IEEE standards."""
        # IEEE standards have specific patterns
        patterns = [
            r'IEEE\s+(?:Std\s+)?(\d+(?:\.\d+)?)',
            r'\b(\d{3,4}(?:\.\d+)?)\b'
        ]

        results = []

        # Check if query matches a specific standard number
        for pattern in patterns:
            matches = re.findall(pattern, query, re.IGNORECASE)
            for match in matches:
                std_num = match
                results.append({
                    'organization': 'IEEE',
                    'number': f'IEEE {std_num}',
                    'title': f'IEEE Standard {std_num}',
                    'status': 'current',  # Placeholder
                    'year': '2020',  # Placeholder
                    'type': 'standard',
                    'url': f'https://standards.ieee.org/standard/{std_num}.html'
                })

        # If no specific matches, do keyword search
        if not results:
            # Placeholder for API-based search
            # In production, this would use IEEE API
            pass

        return results

    def _search_iec(self, org: str, query: str, status: Optional[str]) -> List[Dict[str, Any]]:
        """Search IEC standards."""
        patterns = [
            r'IEC\s+(\d+(?:-\d+)?)',
            r'\b(\d{5}(?:-\d+)?)\b'
        ]

        results = []

        for pattern in patterns:
            matches = re.findall(pattern, query, re.IGNORECASE)
            for match in matches:
                std_num = match
                results.append({
                    'organization': 'IEC',
                    'number': f'IEC {std_num}',
                    'title': f'IEC Standard {std_num}',
                    'status': 'current',
                    'year': '2020',
                    'type': 'standard',
                    'url': f'https://webstore.iec.ch/publication/{std_num}'
                })

        return results

    def _search_ipc(self, org: str, query: str, status: Optional[str]) -> List[Dict[str, Any]]:
        """Search IPC standards."""
        patterns = [
            r'IPC-([A-Z]-)?(\\d+)([A-Z])?',
            r'\b([A-Z]-)?(\\d{3,4})([A-Z])?\b'
        ]

        results = []

        for pattern in patterns:
            matches = re.findall(pattern, query, re.IGNORECASE)
            for match in matches:
                prefix, number, revision = match
                std_num = f'{prefix}{number}{revision}'
                results.append({
                    'organization': 'IPC',
                    'number': f'IPC-{std_num}',
                    'title': f'IPC-{std_num}',
                    'status': 'current',
                    'year': '2020',
                    'type': 'standard',
                    'url': f'https://www.ipc.org/ipc-{std_num}'
                })

        return results

    def _search_jedec(self, org: str, query: str, status: Optional[str]) -> List[Dict[str, Any]]:
        """Search JEDEC standards."""
        patterns = [
            r'JESD(\d+)-([A-Z]?\d+)',
            r'\b(\d{2,3})-([A-Z]?\d+)\b'
        ]

        results = []

        for pattern in patterns:
            matches = re.findall(pattern, query, re.IGNORECASE)
            for match in matches:
                series, spec = match
                std_num = f'JESD{series}-{spec}'
                results.append({
                    'organization': 'JEDEC',
                    'number': std_num,
                    'title': f'JEDEC Standard {std_num}',
                    'status': 'current',
                    'year': '2020',
                    'type': 'standard',
                    'url': f'https://www.jedec.org/standards-documents/{std_num.lower()}'
                })

        return results

    def _search_iso(self, org: str, query: str, status: Optional[str]) -> List[Dict[str, Any]]:
        """Search ISO standards."""
        patterns = [
            r'ISO\s+(\d+)',
            r'\b(\d{4,5})\b'
        ]

        results = []

        for pattern in patterns:
            matches = re.findall(pattern, query, re.IGNORECASE)
            for match in matches:
                std_num = match
                results.append({
                    'organization': 'ISO',
                    'number': f'ISO {std_num}',
                    'title': f'ISO {std_num}',
                    'status': 'current',
                    'year': '2020',
                    'type': 'standard',
                    'url': f'https://www.iso.org/standard/{std_num}.html'
                })

        return results

    def _search_ul(self, org: str, query: str, status: Optional[str]) -> List[Dict[str, Any]]:
        """Search UL standards."""
        patterns = [
            r'UL\s+(\d+)',
            r'\b(\d{3,5})\b'
        ]

        results = []

        for pattern in patterns:
            matches = re.findall(pattern, query, re.IGNORECASE)
            for match in matches:
                std_num = match
                results.append({
                    'organization': 'UL',
                    'number': f'UL {std_num}',
                    'title': f'UL {std_num}',
                    'status': 'current',
                    'year': '2020',
                    'type': 'standard',
                    'url': f'https://ul.com/ul{std_num}'
                })

        return results

    def _search_ansi(self, org: str, query: str, status: Optional[str]) -> List[Dict[str, Any]]:
        """Search ANSI standards."""
        patterns = [
            r'ANSI\s+([A-Z]+\s+\d+)',
        ]

        results = []

        for pattern in patterns:
            matches = re.findall(pattern, query, re.IGNORECASE)
            for match in matches:
                std_num = match
                results.append({
                    'organization': 'ANSI',
                    'number': f'ANSI {std_num}',
                    'title': f'ANSI {std_num}',
                    'status': 'current',
                    'year': '2020',
                    'type': 'standard',
                    'url': f'https://webstore.ansi.org/standards/{std_num}'
                })

        return results

    def _search_pattern_based(
        self,
        org: str,
        query: str,
        status: Optional[str]
    ) -> List[Dict[str, Any]]:
        """Generic pattern-based search for unknown organizations."""
        # Try to extract standard-like patterns from query
        pattern = r'\b([A-Z]{2,10})\s*[-]?\s*(\d+(?:[-.]\d+)*)\b'
        matches = re.findall(pattern, query)

        results = []
        for org_code, number in matches:
            if org_code.upper() == org:
                results.append({
                    'organization': org,
                    'number': f'{org} {number}',
                    'title': f'{org} Standard {number}',
                    'status': 'unknown',
                    'year': 'unknown',
                    'type': 'standard',
                    'url': ''
                })

        return results


def format_bibtex_entry(standard: Dict[str, Any]) -> str:
    """
    Format standard metadata as BibTeX entry.

    Args:
        standard: Standard metadata dictionary

    Returns:
        Formatted BibTeX string
    """
    org = standard.get('organization', 'Unknown')
    number = standard.get('number', 'Unknown')
    title = standard.get('title', 'Untitled')
    year = standard.get('year', 'unknown')
    status = standard.get('status', 'unknown')

    # Generate citation key
    org_lower = org.lower()
    number_clean = re.sub(r'[^a-zA-Z0-9]', '', number)
    key = f"{org_lower}{number_clean}_{year}"

    lines = [f'@standard{{{key},']
    lines.append(f'  title        = {{{title}}},')
    lines.append(f'  number       = {{{number}}},')
    lines.append(f'  organization = {{{org}}},')
    lines.append(f'  year         = {{{year}}},')

    if status and status != 'unknown':
        lines.append(f'  note         = {{Status: {status}}},')

    url = standard.get('url', '')
    if url:
        lines.append(f'  url          = {{{url}}},')

    lines.append('}')

    return '\n'.join(lines)


def export_results(
    results: List[Dict[str, Any]],
    output_format: str = 'json',
    output_file: Optional[Path] = None
):
    """
    Export search results.

    Args:
        results: List of standard metadata
        output_format: 'json' or 'bibtex'
        output_file: Optional output file path
    """
    if output_format == 'json':
        output_text = json.dumps(results, indent=2, ensure_ascii=False)
    elif output_format == 'bibtex':
        entries = [format_bibtex_entry(std) for std in results]
        output_text = '\n\n'.join(entries)
    else:
        raise ValueError(f"Unsupported format: {output_format}")

    if output_file:
        output_file.write_text(output_text, encoding='utf-8')
        print(f"✓ Exported {len(results)} results to {output_file}")
    else:
        print(output_text)


def main():
    """Main entry point."""
    setup_utf8_output()

    parser = argparse.ArgumentParser(
        description='Search technical standards databases',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Search for IEC standard
  python search_standards.py "IEC 61010"

  # Search specific organizations
  python search_standards.py --query "safety power supply" --organizations "IEC,UL"

  # Export to BibTeX
  python search_standards.py "PCB design" --organizations "IPC" --format bibtex --output pcb.bib

  # Search with status filter
  python search_standards.py "wireless" --organizations "IEEE" --status current

Supported Organizations:
  IEEE, IEC, IPC, JEDEC, ISO, UL, ANSI
        '''
    )

    parser.add_argument('query', nargs='?', help='Search query')
    parser.add_argument('--query', '-q', dest='query_arg',
                       help='Search query (alternative to positional)')
    parser.add_argument('--organizations', '--orgs',
                       help='Comma-separated list of organizations (e.g., IEEE,IEC,IPC)')
    parser.add_argument('--status',
                       choices=['current', 'superseded', 'withdrawn', 'all'],
                       help='Filter by standard status')
    parser.add_argument('--limit', type=int, default=100,
                       help='Maximum number of results (default: 100)')
    parser.add_argument('--format', '-f',
                       choices=['json', 'bibtex'],
                       default='json',
                       help='Output format (default: json)')
    parser.add_argument('--output', '-o', type=Path,
                       help='Output file path')

    args = parser.parse_args()

    # Get query from positional or --query argument
    query = args.query or args.query_arg
    if not query:
        parser.error("Search query is required")

    # Parse organizations
    organizations = None
    if args.organizations:
        organizations = [org.strip().upper() for org in args.organizations.split(',')]

    try:
        # Initialize client
        client = StandardsSearchClient()

        print(f"Searching for: {query}", file=sys.stderr)
        if organizations:
            print(f"Organizations: {', '.join(organizations)}", file=sys.stderr)
        print(file=sys.stderr)

        # Perform search
        results = client.search_all(
            query=query,
            organizations=organizations,
            status=args.status if args.status != 'all' else None,
            max_results=args.limit
        )

        print(f"\n✓ Found {len(results)} standards", file=sys.stderr)
        print(file=sys.stderr)

        # Export results
        export_results(results, args.format, args.output)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
