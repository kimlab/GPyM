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
from    optparse            import OptionParser

from    datetime            import datetime

from    .write_to_nc         import WriteNC


class GPM_data( WriteNC ):

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

        self.torigin        = datetime( 1901,1,1)
        self.missing_value  = -9999.9


    def tofile(self, outpath, filetype='nc'):

        iofunc  = { 'nc': self.toncdf,
                   }

        if filetype not in iofunc:
            raise TypeError('%s is not supported yet.'%filetype)

        iofunc[ filetype ]( outpath )



