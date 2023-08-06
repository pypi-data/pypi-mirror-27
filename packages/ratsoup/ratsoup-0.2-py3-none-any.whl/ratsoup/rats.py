"""Rat soup package."""
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-r', '--rats',
                    help='Add more rats.', action='store_true')
parser.add_argument('-s', '--soup',
                    help='Give thems the soups.', action='store_true')
args = parser.parse_args()

# import sys


def rats():
    """More rats."""
    return 'More rats have arrived.'


def soup():
    """Soup."""
    return 'The rats appreciate the soup.'


def main():
    """."""
    if args.rats:
        return rats()
    if args.soup:
        return soup()
    else:
        return 'No soup for the rats.'
