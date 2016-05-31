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





