#! /usr/bin/python
#--------------------------------------------------------------------
# PROGRAM    : parse_fname.py
# CREATED BY : hjkim @IIS.2015-07-13 13:04:18.212930
# MODIFED BY :
#
# USAGE      : $ ./parse_fname.py
#
# DESCRIPTION:
#------------------------------------------------------cf0.2@20120401


import  os, sys, re
from    optparse        import OptionParser
from    cf.util.LOGGER  import *

from    datetime        import timedelta


def parse_fname_trmm(fName, ATTR):
    '''
    fName   : TRMM HDF filename
    ATTR    : list of attributes (i.e., 'sDTime' and/or 'eDTime')
    '''

    sDTime  = datetime.strptime( re.findall(r'\d{8}', fName)[0], '%Y%m%d' )

    offset  = timedelta( seconds=86400 )

    dictFunc= {'sDTime': sDTime,
               'eDTime': sDTime+offset,
               }

    return [dictFunc[attr] for attr in ATTR]



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


