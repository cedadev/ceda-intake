# -*- coding: utf-8 -*-

"""Console script for ceda_intake."""

__author__ = """Ruth Petrie"""
__contact__ = "ruth.petrie@stfc.ac.uk"
__copyright__ = "Copyright 2018 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"

import sys
import argparse
from utils import *
import ceda_intake as cedaintake

def main():
    """Console script for ceda_intake."""

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dataset_ids', type=str, required=True, help='File with list of valid ESGF dataset ids')
    parser.add_argument('-o', '--output_file', type=str, required=False, default='intake-esm.csv', help='Ouptut csv file')
    parser.add_argument('-t', '--catalog_type', type=str, required=False, default='posix', help='Type of catalog to generate: valid entries are posix or s3')
    parser.add_argument('-p', '--project', type=str, required=False, default='cmip6', help='Project catalogue to generate')

    parser.add_argument('_', nargs='*')
    args = parser.parse_args()

    if os.path.exists(args.output_file):
        os.remove(args.output_file)

    # print("Arguments: " + str(args._))
    logging.info(f'Reading from dataset ids file: {args.dataset_ids}')
    #
    # print("Replace this message by putting your code into "
    #       "ceda_intake.cli.main")
    cedaintake.cedaintake_main(args.dataset_ids, args.outputfile, args.catalog_type, args.project)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
