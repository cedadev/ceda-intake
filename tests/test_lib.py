from ceda_intake.lib import scan_deeper


def test_scan_deeper():
    d1 = "/badc/cmip5/data/cmip5/output1/BCC/bcc-csm1-1/decadal1991/mon/land/Lmon/r3i1p1/v20121026"
    v1 = "evspsblsoi  evspsblveg  lai  mrfso  mrlsl  mrro  mrros  mrso  mrsos  prveg  tran  tsl".split()
    r1 = scan_deeper([d1], 1)
    assert sorted(r1) == sorted([f"{d1}/{v}" for v in v1])

    assert scan_deeper([d1], 0) == [d1]

    # Do a 2-level scan
    d2 = "/badc/cmip5/data/cmip5/output1/BCC/bcc-csm1-1/decadal1991/mon/land/Lmon/r3i1p1"
    r2 = scan_deeper([d2], 2)
    assert r2[0] == "/badc/cmip5/data/cmip5/output1/BCC/bcc-csm1-1/decadal1991/mon/land/Lmon/r3i1p1/files/evspsblsoi_20121026"
    assert r2[-1] == "/badc/cmip5/data/cmip5/output1/BCC/bcc-csm1-1/decadal1991/mon/land/Lmon/r3i1p1/v20121026/tsl"
    assert len(r2) == 36
    print("ALL TESTS PASSED")

