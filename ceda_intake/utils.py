#!/usr/bin/env Python

import logging
import sys
import os

logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler(sys.stdout)],format='%(levelname)s:%(message)s')

CSVFILE = '/home/users/rpetrie/cmip6/intake/ceda-cmip6.csv.gz'
INVALIDS = '/home/users/rpetrie/cmip6/intake/invalids-cmip6.txt'
OLDVERSIONS = '/home/users/rpetrie/cmip6/intake/oldVersions.txt'
BASE_DATADIR = "/badc/cmip6/data/"
#BASE_DATADIR = "/home/users/rpetrie/cmip6/intake/data/CMIP6/"
FILE_LIST_BY_MIP_DIR = "/home/users/rpetrie/cmip6/intake/CMIP6_filelist_test"

if os.path.exists(CSVFILE): os.remove(CSVFILE)
if os.path.exists(INVALIDS): os.remove(INVALIDS)
if os.path.exists(OLDVERSIONS): os.remove(OLDVERSIONS)
