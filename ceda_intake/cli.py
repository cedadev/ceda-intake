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
    parser.add_argument('-o', '--output_file', type=str, required=False, default='intake-esm.csv', help='Ouptut csv file')
    parser.add_argument('-t', '--catalog_type', type=str, required=False, default='posix', help='Type of catalog to generate: valid entries are posix or object-store')
    parser.add_argument('-p', '--project', type=str, required=True, help='Project catalog to generate')

    args = parser.parse_args()

    if os.path.exists(args.output_file):
        os.remove(args.output_file)

    make_intake_catalog(args.project)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
