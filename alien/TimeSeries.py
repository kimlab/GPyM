#! /usr/bin/python
#--------------------------------------------------------------------
# PROGRAM    : bin_bytbound.py
# CREATED BY : hjkim @IIS.2015-07-13 09:05:31.202880
# MODIFED BY :
#
# USAGE      : $ ./bin_bytbound.py
#
# DESCRIPTION:
#------------------------------------------------------cf0.2@20120401


import  os,sys
from    optparse        import OptionParser
from    LOGGER          import *

import  bisect

def bin_bytbound( DTime, dtBnd, aSrc=None ):
    '''
    return Indexer if aSrc == None
                   else binned aSrc
    '''

    searchidx   = bisect.bisect_left
    Idx = (searchidx( DTime, bnd  ) for bnd in dtBnd)

    if aSrc == None:
        Idx     = list(Idx)
        return map(None, Idx[:-1], Idx[1:])

    else:
        sIdx    = Idx.next()

        aOut    = []
        for eIdx in Idx:
            if sIdx == eIdx : continue

            aOut.append( aSrc[sIdx:eIdx] )
            sIdx = eIdx
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


