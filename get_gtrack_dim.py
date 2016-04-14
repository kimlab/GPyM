#! /usr/bin/python
#--------------------------------------------------------------------
# PROGRAM    : get_gtrack_dim.py
# CREATED BY : hjkim @IIS.2015-07-13 13:08:20.075973
# MODIFED BY :
#
# USAGE      : $ ./get_gtrack_dim.py
#
# DESCRIPTION:
#------------------------------------------------------cf0.2@20120401


import  os,sys
from    optparse        import OptionParser
from    cf.util.LOGGER  import *

from    cf.devel.collection         import cached

from    get_location_gpm            import get_location_gpm
from    get_location_trmm           import get_location_trmm

from    get_dtime_gpm               import get_dtime_gpm
from    get_dtime_trmm              import get_dtime_trmm


def get_gtrack_dim(srcPath, cache=False, cache_dir=None):
    '''
    scan granules and return dimension (T,Y,X) or ground tracks

    cache  : mode of cf.devel.collection.cached
              ['cached', 'skip', 'update']
    '''

    verbose     = False

    prjName, prdLv, prdVer, yyyy, mm, srcFName  = srcPath.split('/')[-6:]

    get_dtime, get_location = {'TRMM': [get_dtime_trmm, get_location_trmm],
                               'GPM' : [get_dtime_gpm,  get_location_gpm ],
                   }[ prjName.split('.')[0] ]


    cache_dir           = os.path.join( cache_dir, yyyy, mm )

    Lat, Lon    = get_location(srcPath, cache, cache_dir)
    DTime       = cached( srcFName + '.DTime',
                          cache_dir,
                          mode=cache,
                          verbose=verbose )(get_dtime)(srcPath, cache, cache_dir)


    return DTime, Lat, Lon



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

