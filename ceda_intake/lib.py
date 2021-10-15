#!/usr/bin/env python

"""
Example use:

 scprimaryt.py cmip6

Example intake:

$ cat ~/.intake/cache/4967e926fe3363d9d027fcb7ac4d20bf/raw.githubusercontent.com/cp4cds/c3s_34g_manifests/master/intake/catalogs/c3s-cmip6/r3/c3s-cmip6_v20210625.csv.gz | gunzip | head -30

ds_id,path,size,mip_era,activity_id,institution_id,source_id,experiment_id,member_id,table_id,variable_id,grid_label,version,start_time,end_time,bbox,level
c3s-cmip6.ScenarioMIP.EC-Earth-Consortium.EC-Earth3-Veg-LR.ssp585.r1i1p1f1.SImon.sithick.gn.v20201201,ScenarioMIP/EC-Earth-Consortium/EC-Earth3-Veg-LR/ssp585/r1i1p1f1/SImon/sithick/gn/v20201201/sithick_SImon_EC-Earth3-Veg-LR_ssp585_r1i1p1f1_gn_209101-209112.nc,1691093,c3s-cmip6,ScenarioMIP,EC-Earth-Consortium,EC-Earth3-Veg-LR,ssp585,r1i1p1f1,SImon,sithick,gn,v20201201,2091-01-16T12:00:00,2091-12-16T12:00:00,"0.05, -78.58, 359.99, 89.74",
c3s-cmip6.CMIP.EC-Earth-Consortium.EC-Earth3-Veg-LR.historical.r1i1p1f1.day.huss.gr.v20200217,CMIP/EC-Earth-Consortium/EC-Earth3-Veg-LR/historical/r1i1p1f1/day/huss/gr/v20200217/huss_day_EC-Earth3-Veg-LR_historical_r1i1p1f1_gr_18550101-18551231.nc,65838336,c3s-cmip6,CMIP,EC-Earth-Consortium,EC-Earth3-Veg-LR,historical,r1i1p1f1,day,huss,gr,v20200217,1855-01-01T12:00:00,1855-12-31T12:00:00,"0.00, -89.14, 358.88, 89.14",2.00

ds_id, location, ...facets..., start_time, end_time 

"""


import subprocess as sp
import os
import sys
import shlex
import glob
import json
import requests
import pandas as pd

from ceda_intake.catalog_maker import CatalogMaker
from ceda_intake.config import config



def _get_log_file(project):
    return f"{project}.log"


def log_err(msg, project):
    with open(_get_log_file(project), "a") as w:
        w.write(msg + "\n")


def reset(project):
    log_file = _get_log_file(project)
    if os.path.isfile(log_file):
        os.remove(log_file)

    cat_dir = f"catalogs/{project}"
    if not os.path.isdir(cat_dir):
        os.makedirs(cat_dir)


def lookup_latest(dr):
    if not dr or not dr.endswith("latest"):
        return None

    try:
        dr = os.path.join(os.path.dirname(dr), os.readlink(dr)) 
        return dr
    except:
        return None


def rename(dr, project):
    for rename_key, rename_value in config[project].get("renamers", {}).items():
        dr = dr.replace(rename_key, rename_value)

    return dr


def get_dataset_dirs(primary_dir, project):
    """
    This uses "latest" directories to find the directories.
    In the case of CMIP5, extra post-processing will be required.
    """
    query = {"query": { "bool": { "must": [ { "match_phrase_prefix": 
                 { "path": primary_dir } }, 
                 { "term": { "dir": { "value": "latest" } } } ] } } }
    url = "https://elasticsearch.ceda.ac.uk/ceda-dirs/_search?size=10000"
    headers = {'Content-Type': 'application/json'}

    try:
        records = []
        resp = requests.post(url, data=json.dumps(query), headers=headers)
    except:
        log_err(f"Cannot process primary_dir: {primary_dir}", project)
        return []

    for rec in resp.json()["hits"]["hits"]:
        err_msg = f"Suspect elasticsearch record: {rec}"

        try:
            if not rec.get("_source", {}).get("archive_path"):
                dr = lookup_latest(rec.get("path"))
            else:
                dr = rec["_source"]["archive_path"]

            if dr:
                dr = rename(dr, project)
                records.append(dr)
            else:
                log_err(err_msg, project)
        except:
            log_err(err_msg, project)

            
    return records 


def scan_dir(dr):
    return glob.glob(f"{dr}/[a-zA-Z0-9]*")


def scan_deeper(dataset_dirs, scan_level=0):
    dirs = dataset_dirs

    for i in range(scan_level):
        these_dirs = []
        for dr in dirs:
            these_dirs.extend(scan_dir(dr))

        dirs = these_dirs
 
    return dirs


def write_intake_catalog(datasets_file, project):
    facets = config[project]["facets"]
    base_dir = config[project]["base_dir"]
    records = sorted(open(datasets_file).read().strip().split())
    catalog_maker = CatalogMaker(project, facets, records, base_dir, "posix", "nc")
    catalog_maker.create()


def make_intake_catalog(project, remake=True, test_mode=False):
    conf = config[project]

    reset(project)

    primary_dirs_file = f"catalogs/{project}/{project}_primary_dirs.txt"
    datasets_file = f"catalogs/{project}/{project}_dataset_dirs.txt"

    depth = conf["scan_depth"]

    if not remake and os.path.isfile(primary_dirs_file):
        print(f"[WARN] Already found: {primary_dirs_file}")

    else:
        fout = open(primary_dirs_file, "w")
        cmd = f"find -L {conf['base_dir']} -maxdepth {depth} -mindepth {depth} -type d -name '[a-zA-Z0-9]*'"
        print(f"[INFO] Running: {cmd}")
        sp.call(shlex.split(cmd), stdout=fout)
        fout.close()
        print(f"[INFO] Wrote: {primary_dirs_file}")

    if not remake and os.path.isfile(datasets_file):
        print(f"[WARN] Already found: {datasets_file}")

    else:
        print(f"[INFO] Looping through each primary directory to get listings...")
        primary_dirs = open(primary_dirs_file).read().strip().split()

        with open(datasets_file, "w") as dataset_writer:

            for count, primary_dir in enumerate(primary_dirs):
                if [exclude for exclude in conf.get("exclude", []) if exclude in primary_dir]:
                    print(f"[WARN] Ignoring excluded path: {primary_dir}")
                    continue

                dataset_dirs = get_dataset_dirs(primary_dir, project=project)

                if len(dataset_dirs) == 0:
                    log_err(f"./add_latest_links.sh {primary_dir}", project)

                print(f"[INFO] Count for {primary_dir}: {len(dataset_dirs)}")

                dataset_dirs = scan_deeper(dataset_dirs, conf.get("deeper_scan", 0))
                #if dataset_dirs: print(dataset_dirs)
                dataset_writer.write("\n".join(dataset_dirs) + "\n")

                if test_mode and count > 9:
                    print(f"[WARN] Restricting to 10 primary dirs in test mode.")
                    break

        print(f"[INFO] Wrote: {datasets_file}")

    print(f"[INFO] Writing intake file...")
    write_intake_catalog(datasets_file, project)

    print(f"[INFO] All done!")

