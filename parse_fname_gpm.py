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


import  os,sys
from    optparse        import OptionParser
from    cf.util.LOGGER  import *


def parse_fname_gpm(fName, ATTR):
    '''
    fName   : GPM HDF path
    ATTR    : list of attributes (i.e., 'sDTime' and/or 'eDTime')
    '''

    fName   = fName.split('_')

    dictFunc= {'sDTime': datetime.strptime(fName[2], '%y%m%d%H%M'),
               'eDTime': datetime.strptime(fName[2][:6]+fName[3], '%y%m%d%H%M')
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


