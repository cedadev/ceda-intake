"""
test_ceda_client.py
===================

Tests for the client functions to talk to the CEDA directory and file APIs.
"""


from ceda_intake.ceda_client import get_dir_list, get_file_list
    

def test_get_dir_list():
    dr = "/badc/cmip5/data/cmip5/output1"
    results = get_dir_list(dr)

    assert results["result_count"]["value"] == 27

    expected_record = {
"archive_path": "/badc/cmip5/data/",
"depth": 6,
"link": False, 
"path": "/badc/cmip5/data/cmip5/output1/BCC",
"type": "dir",
"dir": "BCC"
}
    assert expected_record in results["results"]


def test_get_file_list():
    dr = "/badc/cru/data/cru_ts/cru_ts_4.05/data/wet"
    results = get_file_list(dr)

    assert results["result_count"]["value"] == 26

    expected_record = {
"info": {
"name_auto": "cru_ts4.05.1901.1910.wet.dat.gz",
"size": "16573159",
"name": "cru_ts4.05.1901.1910.wet.dat.gz",
"location": "on_disk",
"type": ".gz",
"directory": "/badc/cru/data/cru_ts/cru_ts_4.05/data/wet"
 }
}

    assert expected_record in results["results"]

