#! /usr/bin/python
#--------------------------------------------------------------------
# PROGRAM    : write_to_nc.py
# CREATED BY : hjkim @IIS.2017-10-17 06:23:16.129216
# MODIFED BY :
#
# USAGE      : $ ./write_to_nc.py
#
# DESCRIPTION:
#------------------------------------------------------cf0.2@20120401


import  os,sys
from    optparse                import OptionParser

from    collections             import OrderedDict

from    netCDF4                 import Dataset
import  numpy  as np


class WriteNC( object ):

    def toncdf( self, outpath ):

        torigin = self.torigin

        ncfile  = self.open_ncfile( outpath )

        ncdims  = self.create_dimensions( ncfile )

        ncvars  = self.create_variables( ncfile, ncdims )

        self.set_attributes( ncvars )

        dtime   = [ (dtm-torigin).total_seconds() for dtm in self.dtime ]

        ncvars['time'][:]   = dtime[:]
        ncvars['pixel'][:]  = range( self.data.shape[1] )
        ncvars['lat'][:]    = self.lat[:]
        ncvars['lon'][:]    = self.lon[:]
        ncvars['data'][:]   = self.data[:]

        if self.griddata != []:
            ncvars[ 'gridlat'  ][:] = self.grid.lat
            ncvars[ 'gridlon'  ][:] = self.grid.lon
            ncvars[ 'griddata' ][:] = np.ma.masked_equal( self.griddata, self.missing_value )

        ncfile.close()



    def open_ncfile( self, outpath ):

        ncfile  = Dataset( outpath, 'w', format='NETCDF4' )

        return ncfile


    def create_dimensions( self, ncfile ):

        dims    = OrderedDict((
                            ('time',  None),
                            ('pixel', None),
                            ('lat',   None),
                            ('lon',   None)
        ))

        dims['time']    = ncfile.createDimension( "time",  None)
        dims['pixel']   = ncfile.createDimension( "pixel", self.data.shape[1])


        if self.griddata != []:

            dims['gridlat'] = ncfile.createDimension( "gridlat", self.grid.lat.size)
            dims['gridlon'] = ncfile.createDimension( "gridlon", self.grid.lon.size)


        return dims


    def create_variables( self, ncfile, ncdims ):

        varparams   = dict((
                            ( 'time',    ('time','f8',('time', )) ),
                            ( 'pixel',   ('pixel','i4',('pixel',)) ),
                            ( 'lat',     ('lat','f4',('time','pixel')) ),
                            ( 'lon',     ('lon','f4',('time','pixel')) ),
                            ( 'data',    ('data','f4',('time','pixel')) ),
                            ( 'gridlat', ('gridlat','f4',('gridlat', )) ),
                            ( 'gridlon', ('gridlon','f4',('gridlon', )) ),
                            ( 'griddata',('griddata','f4',('time','gridlat','gridlon')) ),
        ))

        ncvars              = OrderedDict()

        ncvars[ 'time' ]    = ncfile.createVariable( *varparams['time'] )
        ncvars[ 'pixel' ]   = ncfile.createVariable( *varparams['pixel'] )
        ncvars[ 'lat' ]     = ncfile.createVariable( *varparams['lat' ] )
        ncvars[ 'lon' ]     = ncfile.createVariable( *varparams['lon' ] )
        ncvars[ 'data' ]    = ncfile.createVariable( *varparams['data' ] )

        if self.griddata != []:
            ncvars[ 'gridlat'  ]    = ncfile.createVariable( *varparams['gridlat' ] )
            ncvars[ 'gridlon'  ]    = ncfile.createVariable( *varparams['gridlon' ] )
            ncvars[ 'griddata' ]    = ncfile.createVariable( *varparams['griddata'], zlib=True, complevel=1 )

        return ncvars


    def set_attributes( self, ncvars ):

        ncvars['time'].units    = 'seconds since %s'%self.torigin.strftime("%Y-%m-%d %H:%M:%S")


