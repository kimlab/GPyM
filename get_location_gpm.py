#! /usr/bin/python
#--------------------------------------------------------------------
# PROGRAM    : get_location.py
# CREATED BY : hjkim @IIS.2015-07-13 13:08:32.265898
# MODIFED BY :
#
# USAGE      : $ ./get_location.py
#
# DESCRIPTION:
#------------------------------------------------------cf0.2@20120401


import  os,sys
from    optparse        import OptionParser

from    numpy           import array


def get_location_gpm(srcPath, fn_read):

    if   'GMI'  in srcPath  : h5Grp = 'S1'
    elif 'DPR'  in srcPath  : h5Grp = 'NS'
    elif 'KuPR' in srcPath  : h5Grp = 'NS'
    elif 'KaPR' in srcPath  : h5Grp = 'MS'
    else:
        raise ValueError('unknown hdf5 group [%s] for %s'%(h5Grp, srcPath))

    Lat     = fn_read( srcPath, '%s/Latitude'%h5Grp  )
    Lon     = fn_read( srcPath, '%s/Longitude'%h5Grp )

    return array( [Lat, Lon] )



def main(args,opts):
    print (args)
    print (opts)

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


