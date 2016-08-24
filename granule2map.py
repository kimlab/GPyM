#! /usr/bin/python
#--------------------------------------------------------------------
# PROGRAM    : granule2map.py
# CREATED BY : hjkim @IIS.2015-07-13 11:56:07.989735
# MODIFED BY :
#
# USAGE      : $ ./granule2map.py
#
# DESCRIPTION:
#------------------------------------------------------cf0.2@20120401


import  os,sys
from    optparse        import OptionParser

from    numpy           import zeros, ma

from    alien.upscale           import upscale
from    alien.nearest_idx       import nearest_idx
from    alien.GridCoordinates   import GridCoordinates


def granule2map(lat, lon, aSrc, BBox=None, res=0.1, verbose=True):
    '''
    res     : out resolution only support n-fold of 0.01 deg
    '''

    Grid    = GridCoordinates('^001',BBox=BBox)     # default mapCode:^001

    aOut    = zeros( (Grid.lat.size,Grid.lon.size), 'float32' )-9999.9

    yIdx    = nearest_idx(Grid.lat, lat.flatten())
    xIdx    = nearest_idx(Grid.lon, lon.flatten())

    aOut[yIdx, xIdx]    = aSrc.flatten()

    nFold   = int( res/Grid.res )

    aOut    = upscale(aOut, (Grid.lat.size/nFold, Grid.lon.size/nFold), mode='m', missing=-9999.9)
    #aOut    = upscale(aOut, (Grid.lat.size/nFold, Grid.lon.size/nFold), mode='s', missing=-9999.9)

    if verbose:
        print '\t[GRANULE2MAP] Domain:%s %s -> %s'%( BBox, aSrc.shape, aOut.shape)

    return aOut


