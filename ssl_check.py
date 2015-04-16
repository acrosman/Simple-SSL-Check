#!/usr/bin/env python3
'''
ssl_check.py

Provides a basic mechanism to grab SSL certificates from a list of domains to
check their future validity. Outputs a list of all certs, their domain,
authority, expiration date, and signing algorithm.
'''
import argparse
import sys
import pkgutil

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help="File with domains (one per line)",
                    required=True)
parser.add_argument('-v', '--verbose', help="Output extra information",
                    action="store_true")
parser.add_argument('-q', '--quiet', help="Suppress all output",
                    action="store_true")
parser.add_argument('-o', '--outfile', help="File to print results into")


args = parser.parse_args()

# Only allow verbose or quiet, not both
if args.verbose and args.quiet:
    print("Cannot run in verbose mode quietly. Select one not both.")

# Check for input file.
try:
    data_file = open(args.file, 'rt')
except:
    print("Unable to open URL data file")
