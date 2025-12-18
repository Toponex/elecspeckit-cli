#!/usr/bin/env python3
"""
Quick Document Number to BibTeX Converter

Convert technical document identifiers (standard numbers, vendor doc IDs, patent numbers)
to properly formatted BibTeX entries.

Usage:
    python docnum_to_bibtex.py "IEEE 802.11-2020"
    python docnum_to_bibtex.py "TI-SLUU551C" --format json
    python docnum_to_bibtex.py --input doc_nums.txt --output references.bib

Supported Identifier Types:
    - IEEE Standards: IEEE 802.11-2020, IEEE Std 1547-2018
    - IEC Standards: IEC 61010-1:2020, IEC 62368-1
    - IPC Standards: IPC-2221B, IPC-A-610
    - JEDEC Standards: JESD22-A114, JESD79-4
    - ISO Standards: ISO 9001:2015
    - Vendor Documents: TI-SLUU551C, AD-AN1234
    - Patents: US10245678B2, EP3456789A1

Author: ElecSpeckit
License: MIT
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, Optional, List


def setup_utf8_output():
    """Setup UTF-8 output for Windows console."""
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def parse_ieee_standard(doc_num: str) -> Optional[Dict]:
    """
    Parse IEEE standard number.

    Examples: IEEE 802.11-2020, IEEE Std 1547-2018
    """
    patterns = [
        r'IEEE\s+(?:Std\s+)?(\d+(?:\.\d+)?)-?(\d{4})',
        r'(\d+(?:\.\d+)?)-?(\d{4})'
    ]

    for pattern in patterns:
        match = re.search(pattern, doc_num, re.IGNORECASE)
        if match:
            std_num = match.group(1)
            year = match.group(2)

            return {
                'type': 'standard',
                'key': f'ieee{std_num.replace(".", "")}_{year}',
                'organization': 'Institute of Electrical and Electronics Engineers',
                'number': f'{std_num}-{year}',
                'title': f'IEEE Standard {std_num}-{year}',
                'year': year,
                'doi': f'10.1109/IEEESTD.{year}.example'  # Placeholder
            }

    return None


def parse_iec_standard(doc_num: str) -> Optional[Dict]:
    """
    Parse IEC standard number.

    Examples: IEC 61010-1:2020, IEC 62368-1
    """
    pattern = r'IEC\s+(\d+(?:-\d+)?):?(\d{4})?'
    match = re.search(pattern, doc_num, re.IGNORECASE)

    if match:
        std_num = match.group(1)
        year = match.group(2) or '2020'

        return {
            'type': 'standard',
            'key': f'iec{std_num.replace("-", "_")}_{year}',
            'organization': 'International Electrotechnical Commission',
            'number': f'{std_num}:{year}',
            'title': f'IEC {std_num}:{year}',
            'year': year
        }

    return None


def parse_ipc_standard(doc_num: str) -> Optional[Dict]:
    """
    Parse IPC standard number.

    Examples: IPC-2221B, IPC-A-610
    """
    pattern = r'IPC-([A-Z]-)?(\d+)([A-Z])?'
    match = re.search(pattern, doc_num, re.IGNORECASE)

    if match:
        prefix = match.group(1) or ''
        number = match.group(2)
        revision = match.group(3) or ''

        full_num = f'{prefix}{number}{revision}'

        return {
            'type': 'standard',
            'key': f'ipc{number}{revision.lower()}',
            'organization': 'IPC - Association Connecting Electronics Industries',
            'number': f'IPC-{full_num}',
            'title': f'IPC-{full_num}',
            'year': '2020'  # Placeholder
        }

    return None


def parse_jedec_standard(doc_num: str) -> Optional[Dict]:
    """
    Parse JEDEC standard number.

    Examples: JESD22-A114, JESD79-4
    """
    pattern = r'JESD(\d+)-([A-Z]?\d+)'
    match = re.search(pattern, doc_num, re.IGNORECASE)

    if match:
        series = match.group(1)
        spec = match.group(2)

        return {
            'type': 'standard',
            'key': f'jesd{series}_{spec.lower()}',
            'organization': 'JEDEC Solid State Technology Association',
            'number': f'JESD{series}-{spec}',
            'title': f'JEDEC Standard JESD{series}-{spec}',
            'year': '2020'  # Placeholder
        }

    return None


def parse_vendor_document(doc_num: str) -> Optional[Dict]:
    """
    Parse vendor document number.

    Examples: TI-SLUU551C, AD-AN1234, LT-AN123
    """
    patterns = [
        r'(TI|AD|LT|ON|ST|NXP|MAXIM)-([A-Z]+\d+)([A-Z])?',
        r'([A-Z]{2,})-([A-Z]+\d+)([A-Z])?'
    ]

    vendor_map = {
        'TI': 'Texas Instruments',
        'AD': 'Analog Devices',
        'LT': 'Linear Technology',
        'ON': 'ON Semiconductor',
        'ST': 'STMicroelectronics',
        'NXP': 'NXP Semiconductors',
        'MAXIM': 'Maxim Integrated'
    }

    for pattern in patterns:
        match = re.search(pattern, doc_num, re.IGNORECASE)
        if match:
            vendor_code = match.group(1).upper()
            doc_id = match.group(2)
            revision = match.group(3) or ''

            vendor_name = vendor_map.get(vendor_code, vendor_code)

            return {
                'type': 'manual',
                'key': f'{vendor_code.lower()}_{doc_id.lower()}',
                'organization': vendor_name,
                'number': f'{doc_id}{revision}',
                'title': f'{vendor_code} {doc_id}{revision}',
                'year': '2020',  # Placeholder
                'note': f'Rev. {revision}' if revision else None
            }

    return None


def parse_patent_number(doc_num: str) -> Optional[Dict]:
    """
    Parse patent number.

    Examples: US10245678B2, EP3456789A1
    """
    pattern = r'([A-Z]{2})(\d+)([A-Z]\d)?'
    match = re.search(pattern, doc_num)

    if match:
        country = match.group(1)
        number = match.group(2)
        kind = match.group(3) or ''

        return {
            'type': 'patent',
            'key': f'{country.lower()}{number}',
            'number': f'{country}{number}{kind}',
            'title': f'Patent {country}{number}{kind}',
            'year': '2020',  # Placeholder
            'author': 'Inventor Name'  # Placeholder
        }

    return None


def parse_document_number(doc_num: str) -> Optional[Dict]:
    """
    Parse any supported document number format.

    Args:
        doc_num: Document identifier string

    Returns:
        Dictionary with parsed metadata, or None if not recognized
    """
    parsers = [
        parse_ieee_standard,
        parse_iec_standard,
        parse_ipc_standard,
        parse_jedec_standard,
        parse_vendor_document,
        parse_patent_number
    ]

    for parser in parsers:
        result = parser(doc_num)
        if result:
            return result

    return None


def format_bibtex_entry(metadata: Dict) -> str:
    """
    Format metadata as BibTeX entry.

    Args:
        metadata: Parsed metadata dictionary

    Returns:
        Formatted BibTeX string
    """
    entry_type = metadata.get('type', 'misc')
    key = metadata.get('key', 'unknown')

    lines = [f'@{entry_type}{{{key},']

    # Field order for different entry types
    if entry_type == 'standard':
        fields = ['title', 'number', 'organization', 'year', 'month', 'doi', 'url']
    elif entry_type == 'manual':
        fields = ['title', 'number', 'organization', 'year', 'month', 'note', 'url']
    elif entry_type == 'patent':
        fields = ['title', 'number', 'author', 'year', 'month', 'assignee', 'url']
    else:
        fields = ['title', 'author', 'year', 'note', 'url']

    # Format fields
    for field in fields:
        if field in metadata and metadata[field]:
            value = metadata[field]
            lines.append(f'  {field:12} = {{{value}}},')

    lines.append('}')

    return '\n'.join(lines)


def process_single_document(doc_num: str, output_format: str = 'bibtex') -> str:
    """
    Process single document number.

    Args:
        doc_num: Document identifier
        output_format: 'bibtex' or 'json'

    Returns:
        Formatted output string
    """
    metadata = parse_document_number(doc_num)

    if not metadata:
        return f"Error: Could not parse document number: {doc_num}"

    if output_format == 'json':
        return json.dumps(metadata, indent=2)
    else:
        return format_bibtex_entry(metadata)


def process_batch(input_file: Path, output_file: Optional[Path] = None,
                 output_format: str = 'bibtex'):
    """
    Process multiple document numbers from file.

    Args:
        input_file: Input file with one document number per line
        output_file: Optional output file path
        output_format: 'bibtex' or 'json'
    """
    try:
        doc_nums = input_file.read_text(encoding='utf-8').strip().split('\n')
    except Exception as e:
        print(f"Error reading input file: {e}", file=sys.stderr)
        return

    results = []
    errors = []

    for doc_num in doc_nums:
        doc_num = doc_num.strip()
        if not doc_num or doc_num.startswith('#'):
            continue

        result = process_single_document(doc_num, output_format)
        if result.startswith('Error:'):
            errors.append(result)
        else:
            results.append(result)

    # Output results
    output_text = '\n\n'.join(results)

    if output_file:
        try:
            output_file.write_text(output_text, encoding='utf-8')
            print(f"✓ Converted {len(results)} document(s) to {output_file}")
            if errors:
                print(f"⚠ {len(errors)} error(s):", file=sys.stderr)
                for error in errors:
                    print(f"  {error}", file=sys.stderr)
        except Exception as e:
            print(f"Error writing output file: {e}", file=sys.stderr)
    else:
        print(output_text)
        if errors:
            print('\n' + '\n'.join(errors), file=sys.stderr)


def main():
    """Main entry point."""
    setup_utf8_output()

    parser = argparse.ArgumentParser(
        description='Convert technical document numbers to BibTeX entries',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Convert single standard number
  python docnum_to_bibtex.py "IEEE 802.11-2020"

  # Convert with JSON output
  python docnum_to_bibtex.py "IPC-2221B" --format json

  # Batch convert from file
  python docnum_to_bibtex.py --input doc_nums.txt --output references.bib

Supported formats:
  - IEEE Standards: IEEE 802.11-2020
  - IEC Standards: IEC 61010-1:2020
  - IPC Standards: IPC-2221B
  - JEDEC Standards: JESD22-A114
  - Vendor Docs: TI-SLUU551C
  - Patents: US10245678B2
        '''
    )

    parser.add_argument('doc_num', nargs='?', help='Document number to convert')
    parser.add_argument('--input', '-i', type=Path, help='Input file with document numbers')
    parser.add_argument('--output', '-o', type=Path, help='Output file path')
    parser.add_argument('--format', '-f', choices=['bibtex', 'json'], default='bibtex',
                       help='Output format (default: bibtex)')

    args = parser.parse_args()

    # Validate arguments
    if not args.doc_num and not args.input:
        parser.error('Either doc_num or --input must be specified')

    if args.doc_num and args.input:
        parser.error('Cannot specify both doc_num and --input')

    # Process
    if args.input:
        process_batch(args.input, args.output, args.format)
    else:
        result = process_single_document(args.doc_num, args.format)

        if args.output:
            try:
                args.output.write_text(result, encoding='utf-8')
                print(f"✓ Output written to {args.output}")
            except Exception as e:
                print(f"Error writing output: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            print(result)


if __name__ == '__main__':
    main()
