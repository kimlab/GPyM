#! /usr/bin/python
#--------------------------------------------------------------------
# PROGRAM    : get_dtime.py
# CREATED BY : hjkim @IIS.2015-07-13 13:08:39.020805
# MODIFED BY :
#
# USAGE      : $ ./get_dtime.py
#
# DESCRIPTION:
#------------------------------------------------------cf0.2@20120401


import  os,sys
from    optparse        import OptionParser

from    numpy           import array
#from    datetime        import datetime, timedelta


def get_dtime_trmm(srcPath, func_read):

    Year    = func_read( srcPath, 'Year'        ).astype('int')
    Month   = func_read( srcPath, 'Month'       ).astype('int')
    Day     = func_read( srcPath, 'DayOfMonth'  ).astype('int')
    Hour    = func_read( srcPath, 'Hour'        ).astype('int')
    Minute  = func_read( srcPath, 'Minute'      ).astype('int')
    Second  = func_read( srcPath, 'Second'      ).astype('int')
    MicSec  = func_read( srcPath, 'MilliSecond' ).astype('int')*1000

    return array( [Year, Month, Day, Hour, Minute, Second, MicSec] ).T

    '''
    DTime   = []
    for y,m,d,H,M,S,uS in map(None,Year,Month,Day,Hour,Minute,Second,MicSec):

        if uS == 1000000:
            DTime.append( datetime(y,m,d,H,M,S,0)+timedelta(seconds=1) )
            print 'Warning [Millisecond] == 1000 : %i %i %i %i %i %i %i'%(y,m,d,H,M,S,uS/1000)

        else:
            DTime.append( datetime(y,m,d,H,M,S,uS) )

    return array( DTime )
    '''



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


