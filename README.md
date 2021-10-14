# CEDA Intake catalogues



Example intake catalog:

```
ds_id,path,size,mip_era,activity_id,institution_id,source_id,experiment_id,member_id,table_id,variable_id,grid_label,version,start_time,end_time,bbox,level
c3s-cmip6.ScenarioMIP.CAS.FGOALS-g3.ssp119.r1i1p1f1.day.sfcWind.gn.v20191202,ScenarioMIP/CAS/FGOALS-g3/ssp119/r1i1p1f1/day/sfcWind/gn/v20191202/sfcWind_day_FGOALS-g3_ssp119_r1i1p1f1_gn_20860101-20861231.nc,21053432,c3s-cmip6,ScenarioMIP,CAS,FGOALS-g3,ssp119,r1i1p1f1,day,sfcWind,gn,v20191202,2086-01-01T12:00:00,2086-12-31T12:00:00,"0.00, -90.00, 358.00, 90.00",10.00
c3s-cmip6.ScenarioMIP.EC-Earth-Consortium.EC-Earth3-Veg-LR.ssp585.r1i1p1f1.SImon.sithick.gn.v20201201,ScenarioMIP/EC-Earth-Consortium/EC-Earth3-Veg-LR/ssp585/r1i1p1f1/SImon/sithick/gn/v20201201/sithick_SImon_EC-Earth3-Veg-LR_ssp585_r1i1p1f1_gn_209101-209112.nc,1691093,c3s-cmip6,ScenarioMIP,EC-Earth-Consortium,EC-Earth3-Veg-LR,ssp585,r1i1p1f1,SImon,sithick,gn,v20201201,2091-01-16T12:00:00,2091-12-16T12:00:00,"0.05, -78.58, 359.99, 89.74",
```

Keys:
```
- ds_id:  c3s-cmip6.ScenarioMIP.CAS.FGOALS-g3.ssp119.r1i1p1f1.day.sfcWind.gn.v20191202
- path:   ScenarioMIP/CAS/FGOALS-g3/ssp119/r1i1p1f1/day/sfcWind/gn/v20191202/sfcWind_day_FGOALS-g3_ssp119_r1i1p1f1_gn_20860101-20861231.nc
- size:   21053432
- mip_era:   c3s-cmip6
- activity_id:   ScenarioMIP
- institution_id:   CAS
- source_id:   FGOALS-g3
- experiment_id:   ssp119
- member_id:   r1i1p1f1
- table_id:   day
- variable_id:   sfcWind
- grid_label:   gn
- version:   v20191202
- start_time:   2086-01-01T12:00:00
- end_time:   2086-12-31T12:00:00
- bbox:   0.00, -90.00, 358.00, 90.00
- level:   10.00
```




[![Pypi](https://img.shields.io/pypi/v/ceda_intake.svg)](https://pypi.python.org/pypi/ceda_intake)

[![Travis](https://img.shields.io/travis/cedadev/ceda_intake.svg)](https://travis-ci.org/cedadev/ceda_intake)

[![Documentation](https://readthedocs.org/projects/ceda-intake/badge/?version=latest)](https://ceda-intake.readthedocs.io/en/latest/?badge=latest)


[![Updates](https://pyup.io/repos/github/cedadev/ceda_intake/shield.svg)](https://pyup.io/repos/github/cedadev/ceda_intake/)

"""
Extract attributes of a file using information from CMIP6 DRS.
References
 1. CMIP6 DRS: http://goo.gl/v1drZl
 2. Controlled Vocabularies (CVs) for use in CMIP6:
    https://github.com/WCRP-CMIP/CMIP6_CVs
mipdir structure =
```<mip_era>/
    <activity_id>/
        <institution_id>/
            <source_id>/
                <experiment_id>/
                    <member_id>/
                        <table_id>/
                            <variable_id>/
                                <grid_label>/
                                    <version>
```
file name =
```<variable_id>_<table_id>_<source_id>_<experiment_id >_<member_id>_<grid_label>[_<time_range>].nc```
For time-invariant fields, the last segment (time_range) above is omitted.
Example when there is no sub-experiment: `tas_Amon_GFDL-CM4_historical_r1i1p1f1_gn_196001-199912.nc`
Example with a sub-experiment:   `pr_day_CNRM-CM6-1_dcppA-hindcast_s1960-r2i1p1f1_gn_198001-198412.nc`


Generate Intake ESM catalogs


* Free software: BSD - see LICENSE file in top-level package directory
* Documentation: https://ceda-intake.readthedocs.io.


## Features

* TODO

# Credits

This package was created with `Cookiecutter` and the `audreyr/cookiecutter-pypackage` project template.

 * Cookiecutter: https://github.com/audreyr/cookiecutter
 * cookiecutter-pypackage: https://github.com/audreyr/cookiecutter-pypackage

# ceda-intake
Generate posix and S3 intake catalogs
