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

from    datetime        import datetime, timedelta


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


