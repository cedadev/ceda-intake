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
        "mappings": {"project": "activity"},
        "deeper_scan": 1,
        "exclude": ("derived", "retracted")
    },
    "cordex": {
        "base_dir": "/badc/cordex/data/cordex",
        "facets": "project product domain institute driving_model experiment ensemble rcm_name rcm_version time_frequency variable version".split(),
        "scan_depth": 5,
        "mappings": {"project": "project"},
        "renamers": {"CORDEX": "cordex"}
    }
}

