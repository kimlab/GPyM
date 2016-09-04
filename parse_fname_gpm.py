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

from    datetime        import datetime, timedelta


def parse_fname_gpm(fName, ATTR):
    '''
    fName   : GPM HDF path
    ATTR    : list of attributes (i.e., 'sDTime' and/or 'eDTime')
    '''

    fName   = fName.split('_')

    dictFunc= {'sDTime': datetime.strptime(fName[2], '%y%m%d%H%M'),
               'eDTime': datetime.strptime(fName[2][:6]+fName[3], '%y%m%d%H%M')
               }

    if dictFunc['eDTime'] < dictFunc['sDTime']:
        dictFunc['eDTime'] += timedelta( days=1 )

    return [dictFunc[attr] for attr in ATTR]

