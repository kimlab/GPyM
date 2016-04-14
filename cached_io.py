#! /usr/bin/python
#--------------------------------------------------------------------
# PROGRAM    : cached_io.py
# CREATED BY : hjkim @IIS.2015-07-13 13:09:45.908298
# MODIFED BY :
#
# USAGE      : $ ./cached_io.py
#
# DESCRIPTION:
#------------------------------------------------------cf0.2@20120401


import  os,sys
from    optparse        import OptionParser
from    cf.util.LOGGER  import *

from    cf.devel.collection         import cached
from    cf2.io.read_hdf4            import read_hdf4
from    cf2.io.read_hdf5            import read_hdf5


def cached_io( srcPath, varName, mode='skip', cacheDir=None):
    if srcPath[-2:] == 'h5':
        func_read   = read_hdf5

    else:
        func_read   = read_hdf4


    cacheFName  = srcPath.split('/')[-1] + '.%s'%'.'.join(varName.split('/'))

    verbose = False
    aOut    = cached(cacheFName, cacheDir, mode=mode, verbose=verbose)(func_read)(srcPath, varName)


    if aOut.shape == ():
        os.remove( '%s/%s'%(cacheDir, cacheFName) )
        raise ValueError, 'blank cache file (erased): %s/%s'%(cacheDir, cacheFName)

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


