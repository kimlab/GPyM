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


def get_dtime_gpm(srcPath, fn_read):

    if   'GMI'  in srcPath  : h5Grp = 'S1'
    elif 'DPR'  in srcPath  : h5Grp = 'NS'
    elif 'KuPR' in srcPath  : h5Grp = 'NS'
    elif 'KaPR' in srcPath  : h5Grp = 'MS'
    else:
        raise ValueError, 'unknown hdf5 group [%s] for %s'%(h5Grp, srcPath)

    Year    = fn_read( srcPath,'%s/ScanTime/Year'%h5Grp        ).astype('int')
    Month   = fn_read( srcPath,'%s/ScanTime/Month'%h5Grp       ).astype('int')
    Day     = fn_read( srcPath,'%s/ScanTime/DayOfMonth'%h5Grp  ).astype('int')
    Hour    = fn_read( srcPath,'%s/ScanTime/Hour'%h5Grp        ).astype('int')
    Minute  = fn_read( srcPath,'%s/ScanTime/Minute'%h5Grp      ).astype('int')
    Second  = fn_read( srcPath,'%s/ScanTime/Second'%h5Grp      ).astype('int')
    MicSec  = fn_read( srcPath,'%s/ScanTime/MilliSecond'%h5Grp ).astype('int')*1000

    return array( [Year, Month, Day, Hour, Minute, Second, MicSec] ).T

    '''
    DTime   = []
    for y,m,d,H,M,S,uS in map(None,Year,Month,Day,Hour,Minute,Second,MicSec):

        if uS == 1000000:
            DTime.append( datetime(y,m,d,H,M,S,0)+timedelta(seconds=1) )
            print 'Warning [NS/ScanTime/Millisecond] == 1000 : %i %i %i %i %i %i %i'%(y,m,d,H,M,S,uS/1000)

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


