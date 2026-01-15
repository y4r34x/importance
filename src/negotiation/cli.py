#!/usr/bin/env python3
"""
Command-line interface for the negotiation package.

Provides entry points for:
- Contract analysis (support contract + auto-renewal detection)
- HTML parsing
- LLM-based field extraction
"""

import sys
import argparse
from pathlib import Path

from negotiation.extraction.detectors import (
    parse_html_file,
    extract_text_content,
    detect_support_contract,
    detect_auto_renew
)


def analyze_contract():
    """
    Main entry point for contract analysis.

    Analyzes HTML files to predict support contract status and auto-renewal status.
    Outputs results as tab-separated values.
    """
    print("Starting contract analysis pipeline...")

    parser = argparse.ArgumentParser(
        description='Analyze HTML file for support contract and auto-renewal status'
    )
    parser.add_argument(
        'html_file',
        type=str,
        help='Path to the HTML file to analyze'
    )

    args = parser.parse_args()

    # Convert to Path object for better handling
    file_path = Path(args.html_file)

    # Parse the HTML file
    soup = parse_html_file(file_path)
    if soup is None:
        sys.exit(1)

    # Extract text content
    text = extract_text_content(soup)
    if not text:
        print("Error: Could not extract text content from HTML file.", file=sys.stderr)
        sys.exit(1)

    # Detect support contract status
    is_support_contract = detect_support_contract(text)

    # Detect auto-renewal status
    is_auto_renew = detect_auto_renew(text)

    # Output results as tab-separated values: support_contract<TAB>auto_renewal
    print(f"{is_support_contract}\t{is_auto_renew}")


def main():
    """Main entry point that dispatches to subcommands."""
    parser = argparse.ArgumentParser(
        description='Contract negotiation ML toolkit',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a contract for support/auto-renewal
  negotiate analyze contract.html

  # Parse HTML to JSON
  python -m negotiation.extraction.html_parser contract.html

  # Extract fields using LLM
  python -m negotiation.extraction.llm_extractor contract.json --url https://...
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # analyze subcommand
    analyze_parser = subparsers.add_parser(
        'analyze',
        help='Analyze contract for support/auto-renewal status'
    )
    analyze_parser.add_argument(
        'html_file',
        type=str,
        help='Path to the HTML file to analyze'
    )

    args = parser.parse_args()

    if args.command == 'analyze':
        # Re-parse with the analyze args
        sys.argv = ['negotiate', args.html_file]
        analyze_contract()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
