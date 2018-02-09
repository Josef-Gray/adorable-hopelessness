"""Set up standard flags."""

import argparse
import logging

def setup_flags(description):
    """Enable standard flags."""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-v", "--verbose", help="enable verbose logging",
                        action="store_true")
    parser.add_argument("--debug", help="enable debug logging",
                        action="store_true")

    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    elif args.verbose:
        logging.basicConfig(level=logging.INFO)

