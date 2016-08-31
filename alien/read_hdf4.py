#! /usr/bin/python
#--------------------------------------------------------------------
# PROGRAM    : read_hdf4.py
# CREATED BY : hjkim @IIS.2015-07-15 15:21:18.949532
# MODIFED BY :
#
# USAGE      : $ ./read_hdf4.py
#
# DESCRIPTION:
#------------------------------------------------------cf0.2@20120401


import  os,sys
from    optparse        import OptionParser

from    pyhdf           import SD


def read_hdf4(srcPath, varName, Slice=None, verbose=True):
    h4      = SD.SD(srcPath)# 'r')

    if Slice == None:   Slice = slice(None,None,None)

    '''
    h4Var   = h4.select(varName)
    print dir(h4Var)
    print  h4Var.dimensions()

    sys.exit()
    '''

    try:
        h4Var   = h4.select(varName)
        aOut    = h4Var[:][Slice]

    except:
        print '!'*80
        print 'I/O Error'
        print 'Blank File? %s'%srcPath
        print 'Blank array will be returned [ %s ]'%varName
        print h4Var.dimensions()
        print Slice
        print '!'*80

        #raise ValueError


    if verbose  == True:
        print '\t[READ_HDF4] %s [%s] -> %s'%( srcPath, varName, aOut.shape)
       # print '\t[READ_HDF4] %s %s -> %s'%( srcPath, h4Var.dimensions(), aOut.shape)

    #h4.close()

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


