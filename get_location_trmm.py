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


def get_location_trmm(srcPath, fn_read):

    Lat     = fn_read( srcPath, 'Latitude'  )
    Lon     = fn_read( srcPath, 'Longitude' )

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


