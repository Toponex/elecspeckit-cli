#!/usr/bin/env python3
"""
IEEE Xplore Search Client

Search IEEE Xplore for technical papers, standards, and conference proceedings.
Supports advanced queries, filtering, and BibTeX export.

Usage:
    python search_ieee_xplore.py "signal integrity PCB design"
    python search_ieee_xplore.py "embedded security" --year-start 2020 --limit 50
    python search_ieee_xplore.py "FPGA" --format bibtex --output fpga_papers.bib

Note: IEEE Xplore API requires authentication. Set IEEEXPLORE_API_KEY environment
variable or use --api-key parameter.

Author: ElecSpeckit
License: MIT
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


def setup_utf8_output():
    """Setup UTF-8 output for Windows console."""
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class IEEEXploreClient:
    """Client for IEEE Xplore API."""

    BASE_URL = "https://ieeexploreapi.ieee.org/api/v1/search/articles"

    def __init__(self, api_key: Optional[str] = None, email: Optional[str] = None):
        """
        Initialize IEEE Xplore client.

        Args:
            api_key: IEEE Xplore API key (or set IEEEXPLORE_API_KEY env var)
            email: Contact email for polite API usage
        """
        self.api_key = api_key or os.environ.get('IEEEXPLORE_API_KEY')
        if not self.api_key:
            raise ValueError(
                "IEEE Xplore API key required. Set IEEEXPLORE_API_KEY environment "
                "variable or pass api_key parameter.\n"
                "Get API key from: https://developer.ieee.org/member/register"
            )

        self.email = email or os.environ.get('USER_EMAIL', 'user@example.com')
        self.rate_limit_delay = 1.0  # seconds between requests
        self.last_request_time = 0

    def _rate_limit(self):
        """Implement rate limiting between requests."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - time_since_last)
        self.last_request_time = time.time()

    def _make_request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make API request to IEEE Xplore.

        Args:
            params: Query parameters

        Returns:
            JSON response as dictionary
        """
        self._rate_limit()

        # Add API key to params
        params['apikey'] = self.api_key

        # Build URL
        url = f"{self.BASE_URL}?{urlencode(params)}"

        # Create request with headers
        headers = {
            'User-Agent': f'ElecSpeckit-CitationManager/1.0 ({self.email})',
            'Accept': 'application/json'
        }

        request = Request(url, headers=headers)

        try:
            with urlopen(request, timeout=30) as response:
                return json.loads(response.read().decode('utf-8'))
        except HTTPError as e:
            if e.code == 401:
                raise ValueError("Invalid API key. Check your IEEEXPLORE_API_KEY.")
            elif e.code == 429:
                raise RuntimeError("Rate limit exceeded. Please wait before retrying.")
            else:
                raise RuntimeError(f"HTTP error {e.code}: {e.reason}")
        except URLError as e:
            raise RuntimeError(f"Network error: {e.reason}")
        except Exception as e:
            raise RuntimeError(f"Request failed: {str(e)}")

    def search(
        self,
        query: str,
        max_results: int = 100,
        start_year: Optional[int] = None,
        end_year: Optional[int] = None,
        content_type: Optional[str] = None,
        sort_by: str = "relevance"
    ) -> List[Dict[str, Any]]:
        """
        Search IEEE Xplore.

        Args:
            query: Search query string
            max_results: Maximum number of results to return
            start_year: Filter by publication year (start)
            end_year: Filter by publication year (end)
            content_type: Filter by content type (Conferences, Journals, Standards, etc.)
            sort_by: Sort order (relevance, newest, oldest, most_cited)

        Returns:
            List of article metadata dictionaries
        """
        results = []
        start_record = 1
        max_records_per_request = 200  # IEEE API limit

        while len(results) < max_results:
            # Calculate how many records to request
            records_needed = min(max_results - len(results), max_records_per_request)

            # Build query parameters
            params = {
                'querytext': query,
                'max_records': records_needed,
                'start_record': start_record,
                'sort_order': self._map_sort_order(sort_by)
            }

            # Add optional filters
            if start_year:
                params['start_year'] = start_year
            if end_year:
                params['end_year'] = end_year
            if content_type:
                params['content_type'] = content_type

            # Make request
            try:
                response = self._make_request(params)
            except Exception as e:
                print(f"Error during search: {e}", file=sys.stderr)
                break

            # Extract articles
            articles = response.get('articles', [])
            if not articles:
                break

            results.extend(articles)

            # Check if we've retrieved all available results
            total_records = response.get('total_records', 0)
            if start_record + len(articles) > total_records:
                break

            start_record += len(articles)

            # Progress indicator
            print(f"Retrieved {len(results)}/{min(max_results, total_records)} results...",
                  file=sys.stderr)

        return results[:max_results]

    def _map_sort_order(self, sort_by: str) -> str:
        """Map user-friendly sort option to API parameter."""
        mapping = {
            'relevance': 'relevance',
            'newest': 'pub_date desc',
            'oldest': 'pub_date asc',
            'most_cited': 'article_citing desc'
        }
        return mapping.get(sort_by, 'relevance')


def format_bibtex_entry(article: Dict[str, Any]) -> str:
    """
    Format IEEE article metadata as BibTeX entry.

    Args:
        article: Article metadata from IEEE API

    Returns:
        Formatted BibTeX string
    """
    # Determine entry type
    content_type = article.get('content_type', '').lower()
    if 'conference' in content_type:
        entry_type = 'inproceedings'
    elif 'journal' in content_type or 'magazine' in content_type:
        entry_type = 'article'
    elif 'standard' in content_type:
        entry_type = 'standard'
    else:
        entry_type = 'misc'

    # Generate citation key
    first_author = article.get('authors', {}).get('authors', [{}])[0].get('full_name', 'Unknown')
    last_name = first_author.split()[-1].lower() if first_author != 'Unknown' else 'unknown'
    year = article.get('publication_year', 'nodate')
    key = f"{last_name}{year}"

    # Build BibTeX entry
    lines = [f'@{entry_type}{{{key},']

    # Title
    title = article.get('title', 'Untitled')
    lines.append(f'  title        = {{{title}}},')

    # Authors
    authors_data = article.get('authors', {}).get('authors', [])
    if authors_data:
        author_names = [a.get('full_name', '') for a in authors_data]
        authors_str = ' and '.join(author_names)
        lines.append(f'  author       = {{{authors_str}}},')

    # Publication venue
    if entry_type == 'inproceedings':
        booktitle = article.get('publication_title', '')
        if booktitle:
            lines.append(f'  booktitle    = {{{booktitle}}},')
    elif entry_type == 'article':
        journal = article.get('publication_title', '')
        if journal:
            lines.append(f'  journal      = {{{journal}}},')

        volume = article.get('volume', '')
        if volume:
            lines.append(f'  volume       = {{{volume}}},')

        issue = article.get('issue', '')
        if issue:
            lines.append(f'  number       = {{{issue}}},')
    elif entry_type == 'standard':
        organization = article.get('publisher', 'IEEE')
        lines.append(f'  organization = {{{organization}}},')

        std_number = article.get('standard_number', '')
        if std_number:
            lines.append(f'  number       = {{{std_number}}},')

    # Year
    year = article.get('publication_year', '')
    if year:
        lines.append(f'  year         = {{{year}}},')

    # Pages
    start_page = article.get('start_page', '')
    end_page = article.get('end_page', '')
    if start_page and end_page:
        lines.append(f'  pages        = {{{start_page}--{end_page}}},')

    # DOI
    doi = article.get('doi', '')
    if doi:
        lines.append(f'  doi          = {{{doi}}},')

    # URL
    html_url = article.get('html_url', '')
    if html_url:
        lines.append(f'  url          = {{{html_url}}},')

    lines.append('}')

    return '\n'.join(lines)


def export_results(
    results: List[Dict[str, Any]],
    output_format: str = 'json',
    output_file: Optional[Path] = None
):
    """
    Export search results to file or stdout.

    Args:
        results: List of article metadata
        output_format: 'json' or 'bibtex'
        output_file: Optional output file path
    """
    if output_format == 'json':
        output_text = json.dumps(results, indent=2, ensure_ascii=False)
    elif output_format == 'bibtex':
        entries = [format_bibtex_entry(article) for article in results]
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
        description='Search IEEE Xplore for technical papers and standards',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Basic search
  python search_ieee_xplore.py "signal integrity PCB design"

  # Search with year filter
  python search_ieee_xplore.py "embedded security" --year-start 2020 --year-end 2024

  # Export to BibTeX
  python search_ieee_xplore.py "FPGA" --format bibtex --output fpga_papers.bib

  # Advanced search with filters
  python search_ieee_xplore.py "5G antenna" --content-type Journals --sort-by most_cited --limit 50

Get your API key from:
  https://developer.ieee.org/member/register
        '''
    )

    parser.add_argument('query', help='Search query')
    parser.add_argument('--api-key', help='IEEE Xplore API key')
    parser.add_argument('--limit', type=int, default=100,
                       help='Maximum number of results (default: 100)')
    parser.add_argument('--year-start', type=int,
                       help='Filter by publication year (start)')
    parser.add_argument('--year-end', type=int,
                       help='Filter by publication year (end)')
    parser.add_argument('--content-type',
                       choices=['Conferences', 'Journals', 'Magazines', 'Standards', 'Books'],
                       help='Filter by content type')
    parser.add_argument('--sort-by',
                       choices=['relevance', 'newest', 'oldest', 'most_cited'],
                       default='relevance',
                       help='Sort order (default: relevance)')
    parser.add_argument('--format', '-f',
                       choices=['json', 'bibtex'],
                       default='json',
                       help='Output format (default: json)')
    parser.add_argument('--output', '-o', type=Path,
                       help='Output file path')

    args = parser.parse_args()

    try:
        # Initialize client
        client = IEEEXploreClient(api_key=args.api_key)

        print(f"Searching IEEE Xplore for: {args.query}", file=sys.stderr)
        print(f"Parameters: limit={args.limit}, sort={args.sort_by}", file=sys.stderr)
        if args.year_start or args.year_end:
            print(f"Year range: {args.year_start or 'any'} to {args.year_end or 'any'}",
                  file=sys.stderr)
        print(file=sys.stderr)

        # Perform search
        results = client.search(
            query=args.query,
            max_results=args.limit,
            start_year=args.year_start,
            end_year=args.year_end,
            content_type=args.content_type,
            sort_by=args.sort_by
        )

        print(f"\n✓ Found {len(results)} results", file=sys.stderr)
        print(file=sys.stderr)

        # Export results
        export_results(results, args.format, args.output)

    except ValueError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        print(file=sys.stderr)
        print("To get an API key, visit:", file=sys.stderr)
        print("https://developer.ieee.org/member/register", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
