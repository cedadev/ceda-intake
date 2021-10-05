"""
ceda_client.py
==============

Client functions to talk to the CEDA directory and file APIs.
"""


import requests
import asyncio


DIR_API = "https://data.ceda.ac.uk/api/directory{dr}"
FILE_API = "https://data.ceda.ac.uk/api/file{dr}"


def get_dir_list(dr):
    results = requests.get(DIR_API.format(dr=dr))
    return results.json()

    
def get_file_list(dr):
    results = requests.get(FILE_API.format(dr=dr))
    return results.json()

