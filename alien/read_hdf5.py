#! /usr/bin/python
#--------------------------------------------------------------------
# PROGRAM    : read_hdf5.py
# CREATED BY : hjkim @IIS.2015-07-13 11:52:15.012270
# MODIFED BY :
#
# USAGE      : $ ./read_hdf5.py
#
# DESCRIPTION:
#------------------------------------------------------cf0.2@20120401


import  os,sys
from    optparse        import OptionParser

import  h5py


def read_hdf5(srcPath, varName, Slice=None, verbose=True):
    h5      = h5py.File(srcPath, 'r')

    if Slice == None:   Slice = slice(None,None,None)

    try:
        h5Var   = h5[varName]
        aOut    = h5Var[Slice]

    except:
        print '!'*80
        print 'I/O Error'
        print 'Blank File? %s'%srcPath
        print 'Blank array will be returned [ %s ]'%varName
        print h5Var.shape
        print Slice
        print '!'*80

        raise ValueError

    if verbose  == True:
        print '\t[READ_HDF5] %s %s -> %s'%( srcPath, h5Var.shape, aOut.shape)

    h5.close()

    return aOut


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


