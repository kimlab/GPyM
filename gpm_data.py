#! /usr/bin/python
#--------------------------------------------------------------------
# PROGRAM    : gpm_data.py
# CREATED BY : hjkim @IIS.2015-07-13 11:55:57.445607
# MODIFED BY :
#
# USAGE      : $ ./gpm_data.py
#
# DESCRIPTION:
#------------------------------------------------------cf0.2@20120401


import  os,sys
from    optparse        import OptionParser
from    cf.util.LOGGER  import *



class GPM_data(object):
    def __init__(self):
        self.srcPath    = []
        self.recLen     = []
        self.lat        = []
        self.lon        = []
        self.dtime      = []
        self.tbound     = []
        self.data       = []
        self.griddata   = []
        self.grid       = []



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


