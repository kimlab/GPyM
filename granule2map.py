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
from    cf.util.LOGGER  import *

from    numpy           import zeros, ma

from    cf.util         import upscale
from    cf.util         import nearest_idx
from    cf.devel.GridCoordinates    import GridCoordinates


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



@ETA
def main(args,opts):
    print args
    print opts

    return


if __name__=='__main__':
    usage   = 'usage: %prog [options] arg'
    version = '%prog 1.0'

    parser  = OptionParser(usage=usage,version=version)

#    parser.add_option('-r','--rescan',action='store_true',dest='rescan',
#                      help='rescan all directory to find missing file')

    (options,args)  = parser.parse_args()

#    if len(args) == 0:
#        parser.print_help()
#    else:
#        main(args,options)

#    LOG     = LOGGER()
    main(args,options)


