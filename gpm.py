#! /usr/bin/python
#--------------------------------------------------------------------
# PROGRAM    : gpm.py
# CREATED BY : hjkim @IIS.2015-01-14 11:52:17.992599
# MODIFED BY :
#
# USAGE      : $ ./gpm.py
#
# DESCRIPTION:
#------------------------------------------------------cf0.2@20120401


import  os, sys, importlib
import  time
import  cPickle         as pickle
from    optparse        import OptionParser
from    ConfigParser    import SafeConfigParser


from    numpy           import empty

from    alien.dtrange               import dtrange

from    alien.GridCoordinates       import GridCoordinates

#from    alien.read_hdf4             import read_hdf4
#from    alien.read_hdf5             import read_hdf5

from    alien.TimeSeries            import bin_bytbound

from    gpm_data                    import GPM_data
from    search_granules             import SearchGranules
from    granule2map                 import granule2map



class GPM( SearchGranules ):
    def __init__(self, prjName, prdLv, prdVer, **kwargs):
        '''
        prjName     : e.g.) 'GPM.KuPR'
        prdLv       : e.g.) 'L2'
        prdVer      : e.g.) '02'
        '''

        self.cfg        = SafeConfigParser( os.environ )
        self.cfg.read( 'config' )

        self.cfg._sections['Defaults'].update( kwargs )

        if self.cfg.get( 'Defaults','dataroot') == '':
            self.cfg.set('Defaults','dataroot', os.environ['PWD'])

        self.dataDir    = self.cfg.get('Defaults','dataroot')

        self.prjName    = prjName
        self.prdLv      = prdLv
        self.prdVer     = prdVer

        self.prdDir     = os.path.join( self.dataDir,
                                        self.prjName,
                                        self.prdLv,
                                        self.prdVer)

        self.cached     = self.cfg.get('Defaults', 'cached')
        self.cacheDir   = self.cfg.get('Defaults', 'cache_dir')

        fnPath          = {'TRMM': self.cfg.get('Defaults','hdf4_module'),
                           'GPM' : self.cfg.get('Defaults','hdf5_module')}[prjName.split('.')[0]]

        fnName          = fnPath.split('.')[-1]
        modPath         = '.'.join( fnPath.split('.')[:-1] )

        self.func_read  = getattr( importlib.import_module( modPath ), fnName )

        print self.func_read
        print type(self.func_read)

        '''
        self.cacheDir   = os.path.join( self.dataDir,
                                        'cache.dim',
                                         self.prjName,
                                         self.prdLv,
                                         self.prdVer)

        self.prdDir     = '%s/%s/%s/%s'%(self.dataDir,
                                         self.prjName,
                                         self.prdLv,
                                         self.prdVer)

        self.cacheDir   = '%s/cache.dim/%s/%s/%s'%(self.dataDir,
                                         self.prjName,
                                         self.prdLv,
                                         self.prdVer)

        self.func_read  = {'TRMM': read_hdf4,
                           'GPM' : read_hdf5}[ prjName.split('.')[0] ]
        '''

        '''
        dictGrp = {'GPM.GMI':'S1',
                   'GPM.DPR':'NS',      # HS, MS, NS
                   'GPM.KaPR':'MS',     # HS, MS
                   'GPM.KuPR':'NS',}

        grpCode = dictGrp[ self.prjName ]
        '''



    def __call__(self, varName, sDTime, eDTime, BBox=None, res=None, delT=None):
        '''
        res     : spa. res. of 2d-array
        sDTime  : DTime bound left
        eDTime  : DTime bound right
        '''

        mapCode     = '^' + ''.join( str(res).split('.') )


        gpmData     = GPM_data()

        srcDir      = os.path.join( self.dataDir, self.prdDir )

        assert os.path.exists( srcDir ), '{} is not exists.'.format( srcDir )
        Granule     = self.search_granules( srcDir, sDTime, eDTime, BBox )

        outSize     = sum( [ len(gra[2]) for gra in Granule ] ), Granule[0][2].shape[1]
        Lat         = empty( outSize, 'float32')
        Lon         = empty( outSize, 'float32')
        aOut        = empty( outSize, 'float32' )
        DTime       = []


        prvI        = 0
        for granule in Granule:

            srcPath, dtime, lat, lon, idx   = granule

            gpmData.srcPath.append(srcPath)
            gpmData.recLen.append( len(dtime) )     # number of data record for each file

            nxtI            = prvI + len(dtime)

            aOut[prvI:nxtI] = self.func_read( srcPath, varName, idx.tolist() )
            Lat[prvI:nxtI]  = lat
            Lon[prvI:nxtI]  = lon
            DTime.extend(dtime)


            if res != None and delT == None:
                gpmData.griddata.append( granule2map( lat, lon, aOut[prvI:nxtI], BBox, res ) )
                gpmData.grid    = GridCoordinates(mapCode, BBox=BBox)

            prvI    = nxtI


        if delT != None:
            dtBnd   = dtrange(sDTime, eDTime, delT)

            gpmData.tbound  = map( None, dtBnd[:-1], dtBnd[1:] )
            gpmData.dtime   = bin_bytbound( DTime, dtBnd, DTime )
            gpmData.lat     = bin_bytbound( DTime, dtBnd, Lat )
            gpmData.lon     = bin_bytbound( DTime, dtBnd, Lon )
            gpmData.data    = bin_bytbound( DTime, dtBnd, aOut )


            if res != None:
                gpmData.griddata    = [ granule2map(lat, lon, a, BBox, res)
                                                     for lat, lon, a in map(None, gpmData.lat, gpmData.lon, gpmData.data) ]
                gpmData.grid    = GridCoordinates(mapCode, BBox=BBox)

        else:
            gpmData.dtime   = DTime
            gpmData.lat     = Lat
            gpmData.lon     = Lon
            gpmData.data    = aOut


        return gpmData


