import os
from functools import wraps
from time import time

import numpy as np
import pandas as pd



json_template = os.path.join(os.path.dirname(os.path.abspath(__file__)), "etc/intake_template.json.tmpl")


def timer(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print(f"func: {f.__name__} args: [{args} {kw}] took: {(te-ts):2.4f} sec")
        return result

    return wrap


class CatalogMaker:

#json_catalog = %(base_dir)s/data/ceda-zarr-{project}.json
#csv_catalog = %(base_dir)s/data/ceda-zarr-{project}.csv
#csv_catalog_url = https://raw.githubusercontent.com/cedadev/cmip6-object-store/master/catalogs/ceda-zarr-{project}.csv

    def __init__(self, project, facets, records, base_dir, fs_type, fmt, limit=None):
        self._facets = facets
        self._records = records
        self._base_dir = base_dir
        self._project = project
        self._limit = limit
        self._description = f"CEDA intake-esm catalog for POSIX NetCDF files: {project}"
        self._cat_id = f"ceda-intake-{project}-{fs_type}-{fmt}"

        self._output_json = f"catalogs/{project}/{self._cat_id}.json"
        self._output_csv = f"catalogs/{project}/{self._cat_id}.csv.gz"
        self._catalog_url = f"https://raw.githubusercontent.com/cedadev/ceda-intake/main/{self._output_csv}"
        
    def create(self):
        self._create_json()
        self._create_csv()

    def _create_json(self):
        template_file = json_template

        with open(template_file) as reader:
            content = reader.read()

        content = (
            content.replace("__description__", self._description)
            .replace("__id__", self._cat_id)
            .replace("__cat_file__", self._catalog_url)
        )

        with open(self._output_json, "w") as writer:
            writer.write(content)

        print(f"[INFO] Wrote intake JSON catalog: {self._output_json}")

    def _create_csv(self):
        df = self._get_dataframe()
        df.to_csv(self._output_csv, index=False)
        print(f"[INFO] Wrote {len(df)} records to CSV catalog file:\n {self._output_csv}")

    @timer
    def _get_dataframe(self):
        print(f"{len(self._records)} datasets")

        headers = ["dsid", "location"] + self._facets[:] + ["start_time", "end_time"]
        rows = []

        for row, dr in enumerate(self._records):
            if not os.path.isdir(dr):
                print(f"[WARN] Directory does not exist: {dr}")
                continue

            if self._limit is not None and row == self._limit:
                break

            dataset_id = dr.replace(self._base_dir, "").strip("/").replace("/", ".")
            facet_values = dataset_id.split(".")
            start, end = self._get_temporal_range(dr)
            location = dr + "/*.nc"
            items = [dataset_id, location, self._project] + facet_values + [start, end]

            rows.append(items)

        return pd.DataFrame(rows, columns=headers)

    def _get_temporal_range(self, dr):
        if "fx/" in dr:
            return "", ""

        try:
            nc_files = sorted(os.listdir(dr))
            nc_files = [
                fn for fn in nc_files if not fn.startswith(".") and fn.endswith(".nc")
            ]

            time_ranges = [fn.split(".")[-2].split("_")[-1].split("-") for fn in nc_files]
            start = f"{min(int(tr[0]) for tr in time_ranges)}"

            if len(start) == 4:
                start += "01"

            end = f"{max(int(tr[1]) for tr in time_ranges)}"
            if len(end) == 4:
                end += "12"
                        
            time_range = start, end
#            print(f"Found {time_range} for: {dr}")

        except Exception as exc:
            print(f"FAILED TO GET TEMPORAL RANGE FOR: {dr}: {exc}")
            time_range = "", ""

        return time_range

