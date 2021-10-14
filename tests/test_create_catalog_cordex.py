import os

from ceda_intake.lib import make_intake_catalog

import intake


proj = "cordex"
cat_file_base = f"catalogs/{proj}/ceda-intake-{proj}-posix-nc"
cat_file_json = f"{cat_file_base}.json"
cat_file_json_url = "https://raw.githubusercontent.com/cedadev/ceda-intake/main/catalogs/cordex/ceda-intake-cordex-posix-nc.json"
cat_file_csv = f"{cat_file_base}.csv.gz"



def test_create_cordex_catalog():
    make_intake_catalog(proj)    

    assert os.path.isfile(cat_file_json)
    assert os.path.isfile(cat_file_csv)


def test_read_cordex_catalog():
    collection = intake.open_esm_datastore(cat_file_json_url)

