# -*- coding: utf-8 -*-

"""Console script for ceda_intake."""

__author__ = """Ruth Petrie"""
__contact__ = "ruth.petrie@stfc.ac.uk"
__copyright__ = "Copyright 2018 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"

import os
import sys
import argparse
from ceda_intake.lib import make_intake_catalog


def main():
    """Console script for ceda_intake."""

    parser = argparse.ArgumentParser()
    parser.add_argument('--test', dest='test_mode', action='store_true', 
                        help='Create small catalog in test mode')
    parser.add_argument('-p', '--project', type=str, required=True, 
                        help='Project catalog to generate')

    args = parser.parse_args()

    make_intake_catalog(args.project, test_mode=args.test_mode)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

