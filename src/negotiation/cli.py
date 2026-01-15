#!/usr/bin/env python3
"""
Command-line interface for the negotiation package.

Provides entry points for:
- Contract analysis (support contract + auto-renewal detection)
- HTML parsing
- LLM-based field extraction
"""

import sys
import json
import argparse
from pathlib import Path

from negotiation.models.predictor import TermPredictor


def analyze_contract():
    """
    Main entry point for contract analysis.

    Analyzes HTML files to predict support contract status and auto-renewal status.
    Note: This command requires the detectors module which is not currently available.
    """
    print("Error: The 'analyze' command requires the detectors module which is not available.", file=sys.stderr)
    print("Use 'negotiate predict' for term prediction instead.", file=sys.stderr)
    sys.exit(1)


def predict_terms():
    """
    Predict contract terms using the Random Forest model.

    Can operate in three modes:
    - Prediction: Given some terms, predict the others
    - Evaluation: Run cross-validation to show model accuracy
    - Importance: Show which terms predict which others
    """
    parser = argparse.ArgumentParser(
        description='Predict contract terms using ML model'
    )
    parser.add_argument(
        '--evaluate', '-e',
        action='store_true',
        help='Run cross-validation and show accuracy per term'
    )
    parser.add_argument(
        '--importance', '-i',
        action='store_true',
        help='Show feature importance (which terms predict which)'
    )
    parser.add_argument(
        '--data', '-d',
        type=str,
        default='data/training/cuad.tsv',
        help='Path to training data TSV file'
    )
    # Term arguments (use kebab-case for CLI, convert to proper names)
    for term in TermPredictor.TERM_COLUMNS:
        arg_name = '--' + term.lower().replace(' ', '-').replace('/', '-')
        parser.add_argument(
            arg_name,
            type=str,
            choices=['yes', 'no', '1', '0'],
            help=f'Known value for {term}'
        )

    args = parser.parse_args()

    # Initialize and fit the model
    print("Loading model...", file=sys.stderr)
    predictor = TermPredictor()
    predictor.fit(args.data)
    print("Model fitted on", len(predictor.data), "contracts", file=sys.stderr)

    if args.evaluate:
        print("\n=== Cross-Validation Results (5-fold) ===\n")
        results = predictor.evaluate()
        print(f"{'Term':<35} {'Accuracy':>10} {'Baseline':>10} {'Lift':>8}")
        print("-" * 65)
        for term, scores in sorted(results.items(), key=lambda x: -x[1]['lift']):
            print(f"{term:<35} {scores['accuracy']:>10.1%} {scores['baseline']:>10.1%} {scores['lift']:>+8.1%}")
        return

    if args.importance:
        print("\n=== Feature Importance ===\n")
        results = predictor.feature_importance()
        for term, features in results.items():
            print(f"\n{term}:")
            for f in features[:3]:  # Top 3
                print(f"  {f['feature']}: {f['importance']:.3f}")
        return

    # Prediction mode: collect known terms from args
    known_terms = {}
    for term in TermPredictor.TERM_COLUMNS:
        arg_name = term.lower().replace(' ', '-').replace('/', '-').replace('-', '_')
        value = getattr(args, arg_name, None)
        if value is not None:
            known_terms[term] = 1 if value in ('yes', '1') else 0

    if not known_terms:
        print("No terms provided. Use --help to see available term arguments.", file=sys.stderr)
        print("\nExample:", file=sys.stderr)
        print("  negotiate predict --audit-rights yes --anti-assignment no", file=sys.stderr)
        sys.exit(1)

    print(f"\nKnown terms: {known_terms}", file=sys.stderr)
    print("\n=== Predictions ===\n")

    results = predictor.predict(known_terms)
    # Sort by probability descending
    sorted_results = sorted(results.items(), key=lambda x: -x[1]['probability'])

    for term, pred in sorted_results:
        val = "Yes" if pred['prediction'] == 1 else "No"
        prob = pred['probability']
        bar = "█" * int(prob * 20)
        print(f"{term:<35} {val:<4} ({prob:.0%}) {bar}")


def main():
    """Main entry point that dispatches to subcommands."""
    parser = argparse.ArgumentParser(
        description='Contract negotiation ML toolkit',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a contract for support/auto-renewal
  negotiate analyze contract.html

  # Predict terms from known values
  negotiate predict --audit-rights yes --anti-assignment no

  # Evaluate model accuracy
  negotiate predict --evaluate

  # Show feature importance
  negotiate predict --importance
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

    # predict subcommand
    predict_parser = subparsers.add_parser(
        'predict',
        help='Predict contract terms using ML model'
    )
    predict_parser.add_argument(
        '--evaluate', '-e',
        action='store_true',
        help='Run cross-validation'
    )
    predict_parser.add_argument(
        '--importance', '-i',
        action='store_true',
        help='Show feature importance'
    )

    args, remaining = parser.parse_known_args()

    if args.command == 'analyze':
        sys.argv = ['negotiate', args.html_file]
        analyze_contract()
    elif args.command == 'predict':
        sys.argv = ['negotiate'] + remaining + (['--evaluate'] if args.evaluate else []) + (['--importance'] if args.importance else [])
        predict_terms()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
