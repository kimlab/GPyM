#! /usr/bin/python
#--------------------------------------------------------------------
# PROGRAM    : get_cache_dir.py
# CREATED BY : hjkim @IIS.2015-07-13 13:09:03.418307
# MODIFED BY :
#
# USAGE      : $ ./get_cache_dir.py
#
# DESCRIPTION:
#------------------------------------------------------cf0.2@20120401


import  os,sys
from    optparse        import OptionParser


def main(args,opts):
    print(args)
    print(opts)

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


