import numpy as np
from fatiando.gravmag import harvester, prism
from fatiando.mesher import PrismMesh
from fatiando import gridder


def test_harvest_restrict():
    def fill(i, case):
        # Returns density of 10 for center prism and prism given by 'case'
        cdir = {'above': 4, 'below': 22, 'north': 14, 'south': 12, 'east': 16,
                'west': 10}
        if i == 13:
            return 10
        for key in cdir:
            if case == key and i == cdir.get(key):
                return 10
        return 0
    # The test cases as string list
    cases = ['above', 'below', 'north', 'south', 'east', 'west']
    # Create reference model
    bounds = (0, 3, 0, 3, 0, 3)
    shape = (3, 3, 3)
    shapegz = (10, 10)
    for testcase in cases:
        mref = PrismMesh(bounds, shape)
        mesh = mref.copy()
        mref.addprop('density', [fill(i, testcase) for i in xrange(mref.size)])
        # Calculate reference gravity field
        xp, yp, zp = gridder.regular(bounds[:4], shapegz, z=-1)
        gzref = prism.gz(xp, yp, zp, mref)
        # Initiate harvest
        hgref = [harvester.Gz(xp, yp, zp, gzref)]
        loc = [[1.5, 1.5, 1.5, {'density': 10}]]
        seeds = harvester.sow(loc, mesh)
        # est0 should be incorrect and thus fail wilst est1 should yield the
        # same geometry as mref
        est0, pred0 = harvester.harvest(hgref, seeds, mesh, compactness=0.1,
                                        threshold=0.001, restrict=[testcase])
        est1, pred1 = harvester.harvest(hgref, seeds, mesh, compactness=0.1,
                                        threshold=0.001)
        res0 = mesh.copy()
        res0.addprop('density', est0['density'])
        res1 = mesh.copy()
        res1.addprop('density', est1['density'])
        l0 = []
        l1 = []
        for i, p in enumerate(res0):
            l0.append(p.props['density'] == mref[i].props['density'])
        for i, p in enumerate(res1):
            l1.append(p.props['density'] == mref[i].props['density'])
        assert not np.all(l0)
        assert np.all(l1)


def test_harvest_test_restriction():
    def fill(i, case):
        # Returns density of 10 for center prism and prism given by 'case'
        cdir = {'above': 4, 'below': 22, 'north': 14, 'south': 12, 'east': 16,
                'west': 10}
        if i == 13:
            return 10
        for key in cdir:
            if case == key and i == cdir.get(key):
                return 10
        return 0
    # Create a reference model
    bounds = (0, 3, 0, 3, 0, 3)
    shape = (3, 3, 3)
    shapegz = (10, 10)
    mref = PrismMesh(bounds, shape)
    mesh = mref.copy()
    mref.addprop('density', [fill(i, 'above') for i in xrange(mref.size)])
    # Calculate reference gravity field
    xp, yp, zp = gridder.regular(bounds[:4], shapegz, z=-1)
    gzref = prism.gz(xp, yp, zp, mref)
    # Initiate harvester
    hgref = [harvester.Gz(xp, yp, zp, gzref)]
    loc = [[1.5, 1.5, 1.5, {'density': 10}]]
    seeds = harvester.sow(loc, mesh)
    # est0 should be correct as it uses a term that exists in the case-list of
    # the _test_restriction() function
    l0 = [True]
    l1 = [False]
    try:
        est0, pred0 = harvester.harvest(hgref, seeds, mesh, compactness=0.1,
                                        threshold=0.001, restrict=['above'])
    except ValueError:
        l0 = [False]
    try:
        est1, pred1 = harvester.harvest(hgref, seeds, mesh, compactness=0.1,
                                        threshold=0.001, restrict=['abve'])
    except ValueError:
        l1 = [True]
    assert l0
    assert l1
