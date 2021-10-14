#!/usr/bin/env python

"""
Example use:

 script.py cmip6

Example intake:

$ cat ~/.intake/cache/4967e926fe3363d9d027fcb7ac4d20bf/raw.githubusercontent.com/cp4cds/c3s_34g_manifests/master/intake/catalogs/c3s-cmip6/r3/c3s-cmip6_v20210625.csv.gz | gunzip | head -30

ds_id,path,size,mip_era,activity_id,institution_id,source_id,experiment_id,member_id,table_id,variable_id,grid_label,version,start_time,end_time,bbox,level

c3s-cmip6.ScenarioMIP.CAS.FGOALS-g3.ssp119.r1i1p1f1.day.sfcWind.gn.v20191202,ScenarioMIP/CAS/FGOALS-g3/ssp119/r1i1p1f1/day/sfcWind/gn/v20191202/sfcWind_day_FGOALS-g3_ssp119_r1i1p1f1_gn_20860101-20861231.nc,21053432,c3s-cmip6,ScenarioMIP,CAS,FGOALS-g3,ssp119,r1i1p1f1,day,sfcWind,gn,v20191202,2086-01-01T12:00:00,2086-12-31T12:00:00,"0.00, -90.00, 358.00, 90.00",10.00

c3s-cmip6.ScenarioMIP.EC-Earth-Consortium.EC-Earth3-Veg-LR.ssp585.r1i1p1f1.SImon.sithick.gn.v20201201,ScenarioMIP/EC-Earth-Consortium/EC-Earth3-Veg-LR/ssp585/r1i1p1f1/SImon/sithick/gn/v20201201/sithick_SImon_EC-Earth3-Veg-LR_ssp585_r1i1p1f1_gn_209101-209112.nc,1691093,c3s-cmip6,ScenarioMIP,EC-Earth-Consortium,EC-Earth3-Veg-LR,ssp585,r1i1p1f1,SImon,sithick,gn,v20201201,2091-01-16T12:00:00,2091-12-16T12:00:00,"0.05, -78.58, 359.99, 89.74",

c3s-cmip6.CMIP.EC-Earth-Consortium.EC-Earth3-Veg-LR.historical.r1i1p1f1.day.huss.gr.v20200217,CMIP/EC-Earth-Consortium/EC-Earth3-Veg-LR/historical/r1i1p1f1/day/huss/gr/v20200217/huss_day_EC-Earth3-Veg-LR_historical_r1i1p1f1_gr_18550101-18551231.nc,65838336,c3s-cmip6,CMIP,EC-Earth-Consortium,EC-Earth3-Veg-LR,historical,r1i1p1f1,day,huss,gr,v20200217,1855-01-01T12:00:00,1855-12-31T12:00:00,"0.00, -89.14, 358.88, 89.14",2.00

ds_id, location, ...facets..., start_time, end_time 

"""


import subprocess as sp
import os
import sys
import shlex
import json
import requests
import pandas as pd

from ceda_intake.catalog_maker import CatalogMaker


config = {
    "cmip6": {
        "base_dir": "/badc/cmip6/data/CMIP6",
        "facets": "mip_era activity_id institution_id source_id experiment_id member_id table_id variable_id grid_label version".split(),
        "scan_depth": 5,
        "mappings": {"variable": "variable_id", "project": "mip_era"}
    },
    "cmip5": {
        "base_dir": "/badc/cmip5/data/cmip5",
        "facets": "activity product institute model experiment frequency realm mip_table ensemble_member version variable".split(),
        "scan_depth": 5, 
        "mappings": {"project": "activity"}
    },
    "cordex": {
        "base_dir": "/badc/cordex/data/cordex",
        "facets": "project product domain institute driving_model experiment ensemble rcm_name rcm_version time_frequency variable".split(),
        "scan_depth": 5,
        "mappings": {"project": "project"}
    }
}


def _get_log_file(project):
    return f"{project}.log"


def log_err(msg, project):
    with open(_get_log_file(project), "a") as w:
        w.write(msg + "\n")


def reset(project):
    log_file = _get_log_file(project)
    if os.path.isfile(log_file):
        os.remove(log_file)


def lookup_latest(dr):
    if not dr or not dr.endswith("latest"):
        return None

    try:
        dr = os.path.join(os.path.dirname(dr), os.readlink(dr)) 
        return dr
    except:
        return None


def get_version_dirs(rip_dir, project):
    query = {"query": { "bool": { "must": [ { "match_phrase_prefix": 
                 { "path": rip_dir } }, 
                 { "term": { "dir": { "value": "latest" } } } ] } } }
    url = "https://elasticsearch.ceda.ac.uk/ceda-dirs/_search?size=10000"
    headers = {'Content-Type': 'application/json'}

    try:
        records = []
        resp = requests.post(url, data=json.dumps(query), headers=headers)
    except:
        log_err(f"Cannot process rip_dir: {rip_dir}", project)
        return []

    for rec in resp.json()["hits"]["hits"]:
        err_msg = f"Suspect elasticsearch record: {rec}"

        try:
            if not rec.get("_source", {}).get("archive_path"):
                dr = lookup_latest(rec.get("path"))
            else:
                dr = rec["_source"]["archive_path"]

            if dr:
                records.append(dr)
            else:
                log_err(err_msg, project)
        except:
            log_err(err_msg, project)

            
    return records 


def write_intake_catalog(version_dirs_file, project):
#    ds_id, location, ...facets..., start_time, end_time
    facets = config[project]["facets"]
    base_dir = config[project]["base_dir"]
    records = sorted(open(version_dirs_file).read().strip().split())
    catalog_maker = CatalogMaker(project, facets, records, base_dir, "posix", "nc")
    catalog_maker.create()


def make_intake_catalog(project, remake=False):
    conf = config[project]
    reset(project)

    rip_file = f"{project}_rip_dirs.txt"
    version_dirs_file = f"{project}_version_dirs.txt"
    intake_file = f"{project}_intake.csv.gz"

    depth = conf["scan_depth"]

    if not remake and os.path.isfile(rip_file):
        print(f"[WARN] Already found: {rip_file}")

    else:
        fout = open(rip_file, "w")
        cmd = f"find -L {conf['base_dir']} -maxdepth {depth} -mindepth {depth} -type d -name 'r*'"
        print(f"[INFO] Running: {cmd}")
        sp.call(shlex.split(cmd), stdout=fout)
        fout.close()
        print(f"[INFO] Wrote: {rip_file}")

    if not remake and os.path.isfile(version_dirs_file):
        print(f"[WARN] Already found: {version_dirs_file}")

    else:
        print(f"[INFO] Looping through each ripf directory to get listings...")
        rip_dirs = open(rip_file).read().strip().split()

        with open(version_dirs_file, "w") as version_writer:

            for rip_dir in rip_dirs:
                version_dirs = get_version_dirs(rip_dir, project=project)
                print(f"[INFO] Count for {rip_dir}: {len(version_dirs)}")
                version_writer.write("\n".join(version_dirs) + "\n")

        print(f"[INFO] Wrote: {version_dirs_file}")

    if not remake and os.path.isfile(intake_file):
        print(f"[WARN] Already found: {intake_file}")

    else:
        print(f"[INFO] Writing intake file: {intake_file}")
        write_intake_catalog(version_dirs_file, project)

    print(f"[INFO] All done!")


if __name__ == "__main__":

    make_intake_catalog(sys.argv[1])
