# -*- coding: utf-8 -*-
import pandas as pd
import dask.dataframe as dd
from intake.source.utils import reverse_format
import os
import re
import glob
import subprocess
from pathlib import Path
import shutil
import numpy as np
from utils import *

"""Main module."""

__author__ = """Ruth Petrie"""
__contact__ = "ruth.petrie@stfc.ac.uk"
__copyright__ = "Copyright 2018 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"

def write_filelists_by_mip(odir, dset_ids):
    """
    Generate a list of all CMIP6 files write output in odir which creates a file for each MIP
    all files in that mip are added.
    :param odir: mipdir to hold lists of all the files
    :return: No return....
    """

    mipfilelists_dir = Path(odir)
    # Clears all records at the start of each run is this what we want?
    if mipfilelists_dir.exists():
        logging.info(f'REMOVING TREE {mipfilelists_dir}')
        shutil.rmtree(mipfilelists_dir)
    mipfilelists_dir.mkdir()

    for ds in dset_ids:
        mip = ds.split('.')[1]
        ds_datadir = Path(BASE_DATADIR, ds.replace('.', '/'))

        with open(f'{mipfilelists_dir}/{mip}.txt', 'a+') as f:
            filepaths = glob.glob(f'{ds_datadir}/*.nc')
            f.write('\n'.join(filepaths) + '\n')


def get_attrs(filepath):

    activity_id, institution_id, source_id, experiment_id, member_id, table_id, variable_id, grid_label, version = filepath.split('/')[5:-1]
    #TODO: Update this to a lookup not a copy of table_id
    frequency = table_id
    time_range = filepath.split('/')[-1].strip('.nc').split('_')[-1]
    keys = ['variable_id', 'table_id', 'source_id', 'experiment_id', 'member_id', 'grid_label', 'time_range', 'frequency', 'activity_id', 'institution_id', 'version', 'path']
    values = [variable_id, table_id, source_id, experiment_id, member_id, grid_label, time_range, frequency, activity_id, institution_id, version, filepath]
    fileparts = dict([(k, v) for k, v in zip(keys, values)])

    return fileparts


def read_file(filename):

    with open(filename) as r:
        listitems = [line.strip() for line in r]
    return listitems


def create_dataframe():

    df = dd.read_csv(f"{FILE_LIST_BY_MIP_DIR}/*.txt", header=None).compute()
    df.columns = ["path"]
    logging.debug(f'READ CSV: dataframe length {len(df)}')
    logging.debug(f'READ CSV: df.head()')

    filelist = df.path.tolist()
    # filelist = list(filter(_filter_func, files))
    logging.debug(f'GEN FILELIST: Length filelist {len(filelist)}')

    entries = list(map(get_attrs, filelist))
    logging.debug(f'GET ENTRIES: Entries: {entries[0]}')
    logging.debug(f'GET ENTRIES:Length entries: {len(entries)}')
    df = pd.DataFrame(entries)
    logging.debug(f'DF FROM ENTRIES: {df.head()}')

    df["dcpp_init_year"] = df.member_id.map(lambda x: float(x.split("-")[0][1:] if x.startswith("s") else np.nan))
    df["member_id"] = df["member_id"].map(lambda x: x.split("-")[-1] if x.startswith("s") else x)
    logging.debug(f'FIX DCPP INIT: {df.head()}')

    columns = ["activity_id", "institution_id", "source_id", "experiment_id", "member_id", "table_id", "variable_id",
               "grid_label", "dcpp_init_year", "version", "time_range", "path"]
    df = df[columns]
    df = df.sort_values(columns, ascending=True).reset_index(drop=True)
    logging.debug(f'SORTING: {df.head()}')

    return df


def cedaintake_main(datasets_file, ofile, catalog_type, project):

    dataset_ids = read_file(datasets_file)

    # Write all files present to mip (activity) level files
    write_filelists_by_mip(FILE_LIST_BY_MIP_DIR, dataset_ids)

    # Generate a dataframe
    df = create_dataframe()

    # df.to_csv(CSVFILE, compression="gzip", index=False)
    df.to_csv(ofile, index=False)
    logging.info(f'Writen file to {ofile} \n length: {len(df)}')

