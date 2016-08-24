#from pylab import *
import numpy as N
from datetime import datetime,timedelta,date,time
from numpy      import arange,array,array_split,mean,empty,zeros,sum
from numpy      import concatenate,ma,ndarray,log,invert
from numpy      import where,polyfit,invert,meshgrid,resize
from    numpy           import bincount, nonzero

import multiprocessing as MP
import time,re
import sys

'''
try:
    from cf                 import rgetara
except:
    print 'Warning! cannot load rgetara.so'
'''

'''
from cf.util.logging        import logging

#dep TextArt
'''
from AnsiFormatter  import AnsiFormatter

'''
from cf                     import mpFunc
'''

#from cf.rgetlen         import rgetlen
'''
import ftplib
try:
    from xml.etree import ElementTree as etree
except:
    print 'ElementTree cannot be loaded.'
'''


class TextArt(object):
    LN  = '%s\n'%('='*80)
    Ln  = '%s\n'%('-'*80)
    ln  = '%s\n'%('.'*80)

    def __init__(self):
        pass

    def __getattr__(self,name):

        if name in AnsiFormatter.FOREGROUND.keys():
            return AnsiFormatter(name)

        else:
            raise AttributeError

    def cprint(self,sOut,color):
        sys.stdout.write( AnsiFormatter(color)+sOut )
        sys.stdout.write( '\n' )


def dtrange(sDTime,eDTime,delTime):
    '''
    TODO: add dtxrange

    delTime : <timedelta> object or <str>
              <str> 'XXw : XX of unitTime, 'w' means 'week' ['y','m','w','d','h']
    '''
    if type(delTime) == str:
        tCnt, tType     = int(delTime[:-1]), delTime[-1]


        if tType in ['y','m']:
            if tType == 'y':    tCnt *=12

            DTime   = []
            nMon    = sDTime.month-1
            cDTime  = sDTime
            while cDTime < eDTime:
                DTime.append(cDTime)
                nMon += 1

                cDTime  = datetime.combine( date(sDTime.year+nMon//12,
                                                 nMon%12+1,
                                                 sDTime.day),
                                            sDTime.time() )

            return DTime[::tCnt]

        else:
            delTime     = timedelta( seconds=tCnt*{'w':86400*7, 'd':86400, 'h':3600}[tType] )

    return [sDTime+delTime*i
                for i in range(int((eDTime-sDTime).total_seconds()/delTime.total_seconds()))]


def unique_counts(aSrc):
    '''
    aSrc    : 1d-array

    ### numpy v1.9 included faster implimentation @ np.unique
    '''
    print aSrc

    bincnt          = bincount( aSrc )
    elements        = nonzero( bincnt )[0]

    return array( zip( bincnt, elements ) ).T



def deciYear2DTime(deciYear):
    year = int(deciYear)

    yearlySec = 86400*(366 if isleap(year) else 365)

    return datetime(year,1,1)+timedelta(seconds=yearlySec*(deciYear-year))


def getFuncName():
    return sys._getframe(1).f_code.co_name

def getCallerName():
    return sys._getframe(2).f_code.co_name

def getLandGrid(Mask,Lat,Lon):

    LON,LAT = meshgrid(Lon,Lat)
    lndLON  = ma.array(LON,mask=Mask).compressed()
    lndLAT  = ma.array(LAT,mask=Mask).compressed()

    I,J     = meshgrid(range(Lon.size),range(Lat.size))
    I       = ma.array(I,mask=Mask).compressed().astype('int32')
    J       = ma.array(J,mask=Mask).compressed().astype('int32')

    return lndLAT,lndLON,J,I


def get_area(res):
    Lat             = arange(-90., 90+res, res)

    meridional_area = array([
                            rgetara(0.0,res,lat1,lat2)
                                    for lat1,lat2 in zip(Lat[:-1],Lat[1:])
                            ])

    return resize( meridional_area, (360/res, 180/res) ).T


def getArea(Lat,Lon,BBox=None,mp=False):
    '''
    rolling longitude may not be supported yet.
    '''

    xres    = Lon[1]-Lon[0]
    yres    = Lat[1]-Lat[0]

    Lat1    = Lat-yres/2.       # llLat
    Lat2    = Lat+yres/2.       # urLat

    Lon1    = Lon-xres/2.       # llLon
    Lon2    = Lon+xres/2.       # urLon

    if BBox != None:
        Lat1[0] = BBox[0][0]
        Lon1[0] = BBox[0][1]

        Lat2[-1]= BBox[1][0]
        Lon2[-1]= BBox[0][1]

    LON1,LAT1   = meshgrid(Lon1,Lat1)
    LON2,LAT2   = meshgrid(Lon2,Lat2)

    return array([rgetara(x1,x2,y1,y2)
                        for x1,x2,y1,y2 in zip(
                                LON1.flat,LON2.flat,
                                LAT1.flat,LAT2.flat)]
                                ).reshape(Lat.size,Lon.size)



def mon2num2mon(mon,option=None):
    dMon    =  {1:'JAN',2:'FEB',3:'MAR',4:'APR',5:'MAY',6:'JUN',
                7:'JUL',8:'AUG',9:'SEP',10:'OCT',11:'NOV',12:'DEC'}

    dNum    =  {'JAN':1,'FEB':2,'MAR':3,'APR':4,'MAY':5,'JUN':6,
                'JUL':7,'AUG':8,'SEP':9,'OCT':10,'NOV':11,'DEC':12}

    if str(mon) in map(str,range(1,13)):
        return dMon[int(mon)]

    else:
        return dNum[mon]


def flatIdx(aMA,axis=0):
    inShp       = aMA.shape

    Mask        = aMA.mask.any(axis)
    flatIdx     = ma.array(arange(Mask.size),mask=Mask.flatten()).compressed()

    return flatIdx


def flatArray(aMA):
    '''
    only for axis = 0
    '''
    axis        = 0
    inShp       = list(aMA.shape)

    tSize       = inShp[axis]

    Mask        = aMA.mask.any(axis)

    flatIdx     = ma.array(arange(Mask.size),mask=Mask.flatten()).compressed()

    return aMA.data.reshape(tSize,-1)[:,flatIdx],[flatIdx,Mask.shape]


def inflatArray(aSrc,flatInfo,fill_value=0.):
    '''
    only for axis = 0
    '''
    axis        = 0
    tSize       = aSrc.shape[0]

    flatIdx     = flatInfo[0]
    MaskShp     = list(flatInfo[1])

    MaskShp.insert(axis,tSize)

    aOut        = zeros(MaskShp,dtype=aSrc.dtype).reshape(tSize,-1)+fill_value
    aOut[:,flatIdx] = aSrc[...]

    return aOut.reshape(MaskShp)

'''
def flatFunc(func,aMA,*args):
#
#    only for axis = 0
#
    axis        = 0
    tSize       = aMA.shape[0]

    Mask        = aMA.mask.any(axis)

    flatIdx     = ma.array(arange(Mask.size),mask=Mask.flatten()).compressed()
    aOut        = func(aMA.data.reshape(tSize,-1)[:,flatIdx],*args)
    return
'''


################################################################################
########################################################################## Const
################################################################################

class Const(object):
    class dt:
        lNDOY = [0,31,59,90,120,151,181,212,243,273,304,334,365]
        lLDOY = [0,31,60,91,121,152,182,213,244,274,305,335,366]

        lNDOM   = [31,28,31,30,31,30,31,31,30,31,30,31]
        lLDOM   = [31,29,31,30,31,30,31,31,30,31,30,31]

        # pentad of year
        lNPOY = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60,
                65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120,
                125, 130, 135, 140, 145, 150, 155, 160, 165, 170, 175, 180,
                185, 190, 195, 200, 205, 210, 215, 220, 225, 230, 235, 240,
                245, 250, 255, 260, 265, 270, 275, 280, 285, 290, 295, 300,
                305, 310, 315, 320, 325, 330, 335, 340, 345, 350, 355, 360, 365]

        lLPOY = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 61,
                66, 71, 76, 81, 86, 91, 96, 101, 106, 111, 116, 121,
                126, 131, 136, 141, 146, 151, 156, 161, 166, 171, 176, 181,
                186, 191, 196, 201, 206, 211, 216, 221, 226, 231, 236, 241,
                246, 251, 256, 261, 266, 271, 276, 281, 286, 291, 296, 301,
                306, 311, 316, 321, 326, 331, 336, 341, 346, 351, 356, 361, 366]

    class path:
        grace   = '/export/raid24/hjkim/GRACE'
        gswp2   = '/export/raid24/hjkim/GSWP'

#..............................................................................#

################################################################################
#################################################################### OrderedDict
################################################################################

class OrderedDict:
    def __init__(self, data=None, **kwdata):
        self._keys = []
        self._data = {}
        if data is not None:
            if hasattr(data, 'items'):
                items = data.items()
            else:
                items = list(data)
            for i in xrange(len(items)):
                length = len(items[i])
                if length != 2:
                    raise ValueError('dictionary update sequence element '
                        '#%d has length %d; 2 is required' % (i, length))
                self._keys.append(items[i][0])
                self._data[items[i][0]] = items[i][1]
        if kwdata:
            self._merge_keys(kwdata.iterkeys())
            self.update(kwdata)


#    def __repr__(self):
#        result = []
#        for key in self._keys:
#            result.append('%s: %s' % (repr(key), repr(self._data[key])))
#        return ''.join(['{', ', '.join(result), '}'])


    def _merge_keys(self, keys):
        self._keys.extend(keys)
        newkeys = {}
        self._keys = [newkeys.setdefault(x, x) for x in self._keys
            if x not in newkeys]


    def update(self, data):
        if data is not None:
            if hasattr(data, 'iterkeys'):
                self._merge_keys(data.iterkeys())
            else:
                self._merge_keys(data.keys())
            self._data.update(data)

    def __setitem__(self, key, value):
        if key not in self._data:
            self._keys.append(key)
        self._data[key] = value

    def __delitem__(self, key):
        del self._data[key]
        self._keys.remove(key)

    def __len__(self):
        return len(self._keys)

    def keys(self):
        return list(self._keys)

    def copy(self):
        copyDict = OrderedDict()
        copyDict._data = self._data.copy()
        copyDict._keys = self._keys[:]
        return copyDict

    def items(self):
        return [(k,self._data[k]) for k in self]

    def values(self):
                return [ self._data[k] for k in self ]

    def __iter__(self):
        for key in self._keys:
            yield key

    def __repr__(self):
        result = []
        for key in self._keys:
            result.append('(%s, %s)' % (repr(key), repr(self._data[key])))
        return ''.join(['OrderedDict', '([', ', '.join(result), '])'])

    def __getitem__(self, key):
        if isinstance(key, slice):
            result = [(k, self._data[k]) for k in self._keys[key]]
            return OrderedDict(result)
        return self._data[key]

#..............................................................................#

################################################################################
################################################################# GridCoordinate
################################################################################

class GridCoordinate(object):
    '''
    Coord   = construct_coord(mapType,BBox)

    def)mapType = mapCode or prjName ('FLOW','TRIP'..) *def: 'u'
        BBox    = [[LLlat,LLlon],[URlat,URlon]]        *def: [[-90,0],[90,360]]

    * mapCode   = ['^','v','u','n']
                    '^',    # S->N, -180->180
                    'v',    # N->S, -180->180
                    'u',    # S->N, 0->360
                    'n',    # N->S, 0->360
    '''
    dPreset = {'^'   :[[-90,-180],[90,180]],
               'v'   :[[90,-180],[-90,180]],
               'n'   :[[90,0],[-90,360]],
               'u'   :[[-90,0],[90,360]],
               'TRIP':[[90,-180],[-90,180]],
               'FLOW':[[90,-180],[-90,180]],
                }


    def __init__(self,res=1.0,mapType='u',BBox=None):

        outBnd  = self.dPreset[mapType]
        LL      = outBnd[0]
        UR      = outBnd[1]

        if BBox == None:
            BBox = outBnd if outBnd[0][0] == -90 else [[UR[0],LL[1]],[LL[0],UR[1]]]

        if LL[0] == -90:
            origin  = 'lower'
            dLat    = res
        else:
            origin  = 'upper'
            dLat    = -res

        dLon    = res

        orgLat  = arange(LL[0]+dLat/2.,
                         UR[0]+dLat/2.,dLat)
        orgLon  = arange(LL[1]+dLon/2.,
                         UR[1]+dLon/2.,dLon)

        LLlon   = BBox[0][1]+res/2.
        URlon   = BBox[1][1]-res/2.

        if origin == 'upper':
            LLlat   = BBox[1][0]-res/2.
            URlat   = BBox[0][0]+res/2.
        else:
            LLlat   = BBox[0][0]-res/2.
            URlat   = BBox[1][0]+res/2.

        LLx = nearest_idx(orgLon,LLlon)
        URx = nearest_idx(orgLon,URlon)
        LLy = nearest_idx(orgLat,LLlat)
        URy = nearest_idx(orgLat,URlat)

        Lat = orgLat[LLy:URy+1]
        Lon = orgLon[LLx:URx+1]

        LON,LAT     = meshgrid(Lon,Lat)
        LATLON      = array((LAT,LON))

        orgX        = arange(orgLon.size)
        orgY        = arange(orgLat.size)
        X           = orgX[LLx:URx+1]
        Y           = orgY[LLy:URy+1]
        XY          = array(meshgrid(X,Y))

        self.res    = res
        self.mapType= mapType
        self.origin = origin
        self.shape  = (len(Lat),len(Lon))

        self.outBnd = outBnd
        self.orgLat = orgLat
        self.orgLon = orgLon
        self.orgX   = orgX
        self.orgY   = orgY

        self.lat    = Lat
        self.lon    = Lon
        self.LAT    = Lat
        self.LON    = Lon
        self.X      = X
        self.Y      = Y

        self.LATLON = LATLON
        self.XY     = XY

        self.BBox   = BBox
        self.lllon  = BBox[0][1]
        self.lllat  = BBox[0][0]
        self.urlon  = BBox[1][1]
        self.urlat  = BBox[1][0]

        self.LLy    = LLy
        self.LLx    = LLx
        self.URy    = URy
        self.URx    = URx
        self.XYBox  = [[LLx,LLy],[URx,URy]]

    def cutmap(self,a,flipud='keep or lower or upper'):
        '''
        cut global map to current GridCoordinate
        '''
        return a[...,self.LLy:self.URy+1,
                     self.LLx:self.URx+1]


    def to_idx(self,(lat,lon),nearest=True):
        if nearest == True:
            x   = nearest_idx(self.LON,lon)
            y   = nearest_idx(self.LAT,lat)
        else:
            LON = self.LON.tolist()
            LAT = self.LAT.tolist()

            if hasattr(lat,'__iter__') and hasttr(lon,'__iter__'):
                x   = [LON.index(l) for l in lon]
                y   = [LAT.index(l) for l in lat]

            else:
                x   = LON.index(lon)
                y   = LAT.index(lat)

        return x,y


    def to_crd(self,(i,j)):
        return self.Lat[j],self.Lon[i]

#..............................................................................#



def coord2idx(*args):
        if len(args) == 1:
            lat = args[0][0]
            lon = args[0][1]
        elif len(args) == 2:
            lat = args[0]
            lon = args[1]
        else:
            raise ValueError

        LAT = N.arange(89.5, -90.5, -1).tolist()
        LON = N.arange(-179.5,180.5).tolist()

        lon = [lon-360.,lon][lon < 180.]

        return LAT.index(lat),LON.index(lon)

def idx2coord(iY,iX):
        LAT = N.arange(89.5, -90.5, -1).tolist()
        LON = N.arange(-179.5,180.5).tolist()

        return LAT[iY],LON[iX]


#nearest_idx = lambda aSrc,val: abs(aSrc-val).argmin()
def nearest_idx(aSrc,val):
    ''' return nearest index '''
    if hasattr(val,'__iter__'): return [abs(aSrc-v).argmin() for v in val]
    else: return abs(aSrc-val).argmin()

'''
def nearest_idx(aSrc,val):
    if aSrc[0] > aSrc[-1]:
        _aSrc   = sorted(aSrc)
#        aSrc.sort()
        idx = N.searchsorted(_aSrc,val)
#        print sorted(aSrc[idx-1:idx+1],reverse=True)

        if val > N.mean(_aSrc[idx-1:idx+1]):
            return len(_aSrc)-idx-1
        else:
            return len(_aSrc)-idx

    else:
        idx = N.searchsorted(aSrc,val)
#        print aSrc[idx-1:idx+1]

        if val < N.mean(aSrc[idx-1:idx+1]):
            return idx-1
        else:
            return idx
'''

def isleap(year):
    leap = lambda x: x%4 == 0 and (x%100 !=0 or  x%400 == 0)
    return leap(year)

'''
def day2year(aSrc,dtStart,filled=-999.):
    if type(dtStart) in [int,float,str]:
        dtStart = datetime(int(dtStart),1,1)

    elif type(dtStart) in [tuple,list]:
        dtStart = datetime(*dtStart)

    doy = dtStart.timetuple()[-2]-1
    year= dtStart.year

    nCnt= 0
    _lIdx= [0]
    while nCnt < len(aSrc):
        if isleap(year):
            nCnt+=366
        else:
            nCnt+=365

        year+=1
        _lIdx.append(nCnt)

    lIdx    = N.array(_lIdx)-doy
    if lIdx[-1] < len(aSrc):
        lIdx = (N.array(_lIdx[1:])-doy).tolist()+[len(aSrc)]
        year+=1
    else:
        lIdx = list(N.array(_lIdx[1:-1]+[len(aSrc)])-doy)

    lIdx.insert(0,0)

    aRe = [N.array(aSrc[lIdx[i]:lIdx[i+1],...]) for i in range(len(lIdx)-1)]

    if filled:
        if isleap(dtStart.year):
            _doy    = 366
        else:
            _doy    = 365

        _Tmp = N.zeros(_doy-len(aRe[0]))+filled
        aRe[0] = N.concatenate((_Tmp,aRe[0]),0)

        if isleap(year-1):
            _doy    = 366
        else:
            _doy    = 365

        _Tmp = N.zeros(_doy-len(aRe[-1]))+filled
        aRe[-1] = N.concatenate((aRe[-1],_Tmp),0)


    print lIdx,dtStart.year, year,len(aSrc)
    print [a.shape for a in aRe]
'''
def day2month(aSrc,sDT):
    IDX     = [0]

    while IDX[-1] < len(aSrc):
        YYYYMM  = '%i%02d' %(sDT.year,sDT.month)
        nDays   = num_days(YYYYMM)
        IDX.append(IDX[-1]+nDays)

        sDT += timedelta(days=nDays)

    if IDX[-1] != len(aSrc):
        IDX.append(len(aSrc))

    return [aSrc[idx1:idx2] for idx1,idx2 in zip(IDX[:-1],IDX[1:])]


def day2mon(aSrc,sDTime,axis=0):
    MonDays =[31,28,31,30,31,30,31,31,30,31,30,31]
    MonDaysL=[31,29,31,30,31,30,31,31,30,31,30,31]

    nDays   = aSrc.shape[axis]

    eDTime  = sDTime+timedelta(days=nDays-1)

    nDAY    = []
    for y in xrange(sDTime.year,eDTime.year+1):
        nDAY.extend(MonDays if not isleap(y) else MonDaysL)

    nDAY    = nDAY[sDTime.month-1:eDTime.month-12 if eDTime.month != 12 else None]
    nDAY[0] = nDAY[0]-sDTime.day+1
    nDAY[-1]= eDTime.day

    IDX     = [[-1]]
    for i,d in enumerate(nDAY):
        sIdx    = IDX[i][-1]+1
        IDX.append(range(sIdx,sIdx+d))

    IDX.pop(0)

    return IDX,(aSrc.take(l,axis=axis) for l in iter(IDX))


def day2month_old(aSrc,sDT):
    DT = [sDT+timedelta(days=i) for i in range(len(aSrc))]

    sYear   = sDT.year
    eYear   = DT[-1].year

    RE  = [[] for y in range(sYear,eYear+1) for m in range(12)]

    for nCnt,dt in enumerate(DT):
        idx = (dt.year-sYear)*12+dt.month-1
        RE[idx].append(aSrc[nCnt])

    return [array(l) for l in RE]


def day2year_old(aSrc,sDT):
    DT = [sDT+timedelta(days=i) for i in range(len(aSrc))]

    sYear   = sDT.year
    eYear   = DT[-1].year

    RE  = [[] for y in range(sYear,eYear+1)]

    for nCnt,dt in enumerate(DT):
        idx = dt.year-sYear
        RE[idx].append(aSrc[nCnt])

    return [array(l) for l in RE]


def day2year(aSrc,sDT):
    IDX     = [0]

    while IDX[-1] < len(aSrc):
        nDays   = [365,366][isleap(sDT.year)]
        IDX.append(IDX[-1]+nDays)

        sDT += timedelta(days=nDays)

    if IDX[-1] != len(aSrc):
        IDX.append(len(aSrc))

    return [aSrc[idx1:idx2] for idx1,idx2 in zip(IDX[:-1],IDX[1:])]


def num_days(YYYYMM):
    if len(YYYYMM) == 6:
        year    = int(YYYYMM[:4])
        month   = int(YYYYMM[4:6])

        year_   = year
        month_  = month+1

        if month_ == 13:
            month_  = 1
            year_   += 1

        return (datetime(year_,month_,1)-datetime(year,month,1)).days

    elif len(YYYYMM) == 4:
        year    = int(YYYYMM)

        return (datetime(year+1,1,1)-datetime(year,1,1)).days

    else:
        raise ValueError, 'bad YYYYMM arg: %s'%YYYYMM


def roller(aSrc,offset=None):
    '''
    numpy.roll has bug (1 pixel vertical drift after horizontal roll)
    '''
    if not offset:
        offset = aSrc.shape[-1]/2

    if not hasattr(aSrc,'mask'):
        return concatenate((aSrc[...,offset:],aSrc[...,:offset]),-1)
    else:
        return ma.array(concatenate((aSrc.data[...,offset:],aSrc.data[...,:offset]),-1),
                    mask = concatenate((aSrc.mask[...,offset:],aSrc.mask[...,:offset]),-1))

def vroller(aSrc,offset=None):
    if not offset:
        offset = aSrc.shape[-2]/2

    return concatenate((aSrc[...,offset:,:],aSrc[...,:offset,:]),-2)

#def roll_crd(lon, Lbound=[-90]):
#    res = abs(lon-int(lon)


def roll_crd(lon, Lbound):
    if int(Lbound == 0):
        return lon+360 if lon <= 0 else lon

    else:
        return lon if lon <= 180 else lon-360


def ftpFile(URL,outPath=None,auth=None):
    if auth == None:
        auth = ['anonymous','hjkim@rainbow.iis.u-tokyo.ac.jp']

    if outPath == None:
        outDir  = './'
        outFName= URL.split('/')[-1]

    site    = URL.split('/')[0]
    path    = '/'.join(URL.split('/')[1:])

    FTP     = ftplib.FTP(site,auth[0],auth[1])
    File    = file(outPath,'wb')
    Err     = FTP.retrbinary('RETR %s'%path,File.write)
    File.close()
    FTP.quit()

    return Err


def urlFile(URL,outPath=None,auth=None):
    '''
    urlFile(URL,outPath,[id,passwd])
    '''
    from urllib import urlopen, FancyURLopener

    def raise_exception(*kw):
        raise UserWarning, (kw[3],kw[4])

    FancyURLopener.http_error_404 = raise_exception

    if URL.startswith('http'):
        URL = URL[7:]

    if auth:
        URL = 'ftp://%s@%s' %(':'.join(auth),URL)

    else:
        URL = 'http://%s' %URL

    if outPath:
        try:
            file(outPath,'wb').write(urlopen(URL).read())

        except UserWarning, Err:
            return Err

    else:
        return urlopen(URL)



def regrid(aSrc,Mult,mode='m'):#,nProc=None):
    '''
    * regrid (resize) array
    * only for last 2 axes (lat, lon)

    aSrc:   n-dimensional array
    Mult:   ratio
            e.g.) when aSrc.shape == (12,180,360)
                  i) Mult == 2   for (12,360,720)
                  ii)Mult == 0.5 for (12,90,180)

    mode:   'a'  for average
            'M'  for maximun
            'm'  for minimum
            's'  for sumation
            'f'  for most frequent
            func for user defined function
    '''

    newShape    = list(aSrc.shape)
    newShape[-2]= int(newShape[-2]*Mult)
    newShape[-1]= int(newShape[-1]*Mult)

    aOut        = empty((newShape),dtype=aSrc.dtype)


    if Mult > 1:
        YX      = [(y,x) for y in xrange(aSrc.shape[-2]) for x in xrange(aSrc.shape[-1])]

        for (y,x) in YX:
            try:
                aOut[...,y*Mult:y*Mult+Mult,x*Mult:x*Mult+Mult]    = aSrc[...,y,x]
            except:
                print y,x
                print 'OUT:',aOut[...,y*Mult:y*Mult+Mult,x*Mult:x*Mult+Mult].shape
                print 'SRC:',aSrc[...,y,x].shape


    elif Mult < 1:

        Mult    = int(1/Mult)

        dictFunc    = {'m':mean,
                       's':sum,
                      }

        func        = mode if mode not in dictFunc else dictFunc[mode]

        YX      = [(y,x) for y in xrange(aOut.shape[-2]) for x in xrange(aOut.shape[-1])]

        for (y,x) in YX:
            aOut[...,y,x]   = func(aSrc[...,y*Mult:y*Mult+Mult,x*Mult:x*Mult+Mult])

    else:
        aOut    = aSrc      ### do nothing whem Mult==1

    return aOut



def mpUpscale(aSrc,newShape,mode='s',weight=None,post_weight=None,missing=None,nProc=1):
    '''
    aSrc[y,x] => aSrc[*newshape]

    mode = [
            's',    # aggregate
            'ws',   # weighted aggregation
            'm'     # mean
            ]

    *** NOTE ***
    only support 3d-array, currently

    '''

    return mpFunc(
                  upscale,
                  (aSrc, newShape, mode, weight, post_weight, missing),
                  [0],
                  axis=0,
                  outShp=(len(aSrc), newShape[0], newShape[1]),
                  chunk=1,
                  nProc=nProc
                 )




def upscale(aSrc,newShape,mode='s',weight=None,post_weight=None,missing=None):
    '''
    aSrc[y,x] => aSrc[*newshape]

    mode = [
            's',    # aggregate
            'ws',   # weighted aggregation
            'm'     # mean
            ]
    '''

    if weight != None:
        aSrc    = aSrc.copy()* weight


    '''
    modeFunc    = {'s':sum,
                   'm':mean,
    }[mode]
    '''

    if len(aSrc.shape)==3 and aSrc.shape[0]==1:
        aSrc.shape  = aSrc.shape[1:]


    if all( array(newShape) > array(aSrc.shape) ):
        nFOLD    = newShape/array(aSrc.shape)

        aRe     = empty(newShape, dtype=aSrc.dtype)

        for i in range(nFOLD[0]):
            for j in range(nFOLD[1]):
                aRe[i::nFOLD[0], j::nFOLD[1]]   = aSrc

    else:
        nFOLD    = array(aSrc.shape)/newShape

        if missing == None:
            aRe = array([
                        aSrc[..., i::nFOLD[-2], j::nFOLD[-1]]
                            for i in range(nFOLD[-2])
                                for j in range(nFOLD[-1])
                                ])

        else:
            aSrc    = ma.masked_equal(aSrc,missing)

            aRe = array([
                        aSrc.data[..., i::nFOLD[-2], j::nFOLD[-1]]
                            for i in range(nFOLD[-2])
                                for j in range(nFOLD[-1])
                                ])

            Mask= array([
                        aSrc.mask[..., i::nFOLD[-2], j::nFOLD[-1]]
                            for i in range(nFOLD[-2])
                                for j in range(nFOLD[-1])
                                ])

            aRe = ma.array(aRe,mask=Mask)


        if   mode == 's':
            aRe = aRe.sum(0)

        elif mode == 'ws':
            weight  = len(aRe)/(len(aRe)-Mask.astype('float64').sum(0))

            aRe = aRe.sum(0)*weight

        elif mode == 'm':
            aRe = aRe.mean(0)

        else:
            raise IOError

        if missing != None:
            aRe = aRe.filled(missing)

    if post_weight != None:
        aRe *= post_weight

    return aRe


def getPANTAD(year):
    TIME    = []

    if isleap(year) == True:
        PANTAD  = Const.dt.lLPOY

    else:
        PANTAD  = Const.dt.lNPOY

    return [datetime(year,1,1)+timedelta(days=p) for p in PANTAD]


def getDTIME(sDTime,eDTime,DT=timedelta(days=1)):
    _DT     = (eDTime-sDTime)
    _days   = _DT.days
    _secs   = _DT.seconds

    nStep   = (_days*86400+_secs)/(DT.days*86400+DT.seconds)+1

    DTIME   = [sDTime+i*DT for i in range(nStep)]

    return array(DTIME)


def det_spike(data1D,std_mult,obserr=20.):
    msk = [True]*len(data1D)
    for nCol, col in enumerate(data1D):
        _data   = data1D.tolist()
        _data.pop(nCol)
        _data   = filter(None,_data)

        avg     = array(_data).mean()
        std     = array(_data).std()

        if col > avg+std*std_mult or col < avg-std*std_mult:
            msk[nCol] = True
        else:
            msk[nCol] = False

    aRe = ma.array(data1D, mask=msk)

    if aRe.std() > obserr:
        aRe = ma.masked_equal([-999.]*len(data1D),-999)

    return aRe

def sorted_table(data2D,iCol,reverse=False):
    pivot   = list(zip(*data2D)[iCol])

    IDX     = [pivot.index(x) for x in sorted(pivot,reverse=reverse)]

    OUT     = [data2D[i] for i in IDX]

    if type(data2D) == ndarray:
        OUT = array(OUT)

    return OUT

def semilog(aSrc,func=log):
    aRe=where(aSrc > 0,func(aSrc),0)
    aRe-=where(aSrc<0,func(abs(aSrc)),0)
    return aRe

'''
def gen_coord(res,UL=[90,-180],LR=[-90,180],gridmesh=False):

    latStep = [res,-res][UL[0] > LR[0]]
    lonStep = [res,-res][UL[1] > LR[1]]

    LAT = arange(UL[0]+latStep/2.,LR[0]+latStep/2.,latStep)
    LON = arange(UL[1]+lonStep/2.,LR[1]+lonStep/2.,lonStep)

    if gridmesh:
        LON,LAT = meshgrid(LON,LAT)

    return LAT,LON
'''

def Regression(obs,mod,ord=1,X=None):
    '''
    Bias Correction using Regression

    obs : standard vector [1xN]
    mod : vector to compare [1xN]
    ord : regression order (if ord==1: Linear Regression)
    X   : x-values
    '''
    Coef    = polyfit(obs,mod,ord)
    POW     = arange(len(Coef))[::-1]

    if not X:
        X       = arange(len(obs))

    REG     = array([(Coef*(x**POW)).sum() for x in X])
    return Coef,REG


def crd2idx(crd,UL=[89.5,-179.5],res=1.0):
    if UL[0] >= 0:
        LAT = arange(UL[0],-90.5+res/2.,-res)
    else:
        LAT = arange(UL[0],90.5-res/2.,res)

    if UL[1] >= 0:
        LON = arange(UL[1],360.5-res/2.,res)
    else:
        LON = arange(UL[1],180.5-res/2.,res)

#    X,Y     = N.meshgrid(LON,LAT)

    I       = LAT.tolist().index(crd[0])
    J       = LON.tolist().index(crd[1])

    return I,J


def CountGenerator(start=0,end=999999999,step=1):
    '''
    >>> count = CountGenerator()
    >>> count.next()
        0

    '''
    while abs(start) < end:
        start += step
        yield start-step


def dict2xml(dic,outPath=None,rootID=None,rootTxt=None):
    if   outPath == None and rootID == None: rootID = 'Root'
    elif outPath != None: rootID = outPath.split('/')[-1]

    xml = etree.Element(rootID)

    if rootTxt != None: xml.text = rootTxt

    for k,v in dic.items():
        print k,v
        xml.append(etree.Element(k,k=str(v)))

    if    outPath == None: return xml
    else: etree.ElementTree(xml).write(outPath)


def etree_indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            etree_indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


# find the closest value/index from interative data (e.g., list, array)
closest_value   = lambda val,vec: min(vec,key=lambda l:abs(l-val))
closest_index   = lambda val,vec: list(vec).index(closest_value(val,vec))

def conv180to360(lon):
    ''' convert between -180~180 and 0~360 '''
    if hasattr(lon,'__iter__'): return where(lon >= 0,array(lon), 360.+array(lon))
    else: return lon if lon >=0 else 360+lon

def conv360to180(lon):
    ''' convert between 0~360 and -180~180 '''
    if hasattr(lon,'__iter__'): return where(lon >= 180,array(lon)-360., array(lon))
    else: return lon-360. if lon >=180 else lon

def bbox180to360(BBox):
    LL  = BBox[0]
    UR  = BBox[1]

    return [[LL[0],conv180to360(LL[1])],
            [UR[0],conv180to360(UR[1])]]

def bbox360to180(BBox):
    LL  = BBox[0]
    UR  = BBox[1]

    return [[LL[0],conv360to180(LL[1])],
            [UR[0],conv360to180(UR[1])]]




# generate LAT, LON
def gen_coord(res,UL=[90,-180],LR=[-90,180],meshgrid=False):
    '''
    |======================+====+===============|
    |UL(lat,lon)           |    |               |
    |           ul(lat,lon)|    |               |
    +----------------------+----+---------------+
    |                      |    |               |
    +----------------------+----+---------------+
    |                      |    |lr(lat1,lon1)  |
    |                      |    |               |
    |                      |    |               |
    |                      |    |               |
    |                      |    |    LR(lat,lon)|
    |======================+====+===============|

    UL: the first element of array (not the origin of figure)
    LR: the lst   element of array (not the origin of figure)
    '''

    latStep = [res,-res][UL[0] > LR[0]]
    lonStep = [res,-res][UL[1] > LR[1]]

    LAT = arange(UL[0]+latStep/2.,LR[0]+latStep/2.,latStep)
    LON = arange(UL[1]+lonStep/2.,LR[1]+lonStep/2.,lonStep)

    if meshgrid:
        LON,LAT = N.meshgrid(LON,LAT)

    return LAT,LON


def split_monthly(iterable, sDTime, dT):
    IDX = xrange(len(iterable))

    OUT = [[]]
    month   = sDTime.month
    for itr in iterable:
        if sDTime.month != month:
            OUT.append([])
            month = (month+1)%12
            if month == 0: month = 12

#            print itr

        OUT[-1].append(itr)

        sDTime += dT

#    print dT*len(IDX)

    return OUT



    return
'''
def day2month(aSrc,sDT):
    IDX     = [0]

    while IDX[-1] < len(aSrc):
        YYYYMM  = '%i%02d' %(sDT.year,sDT.month)
        nDays   = num_days(YYYYMM)
        IDX.append(IDX[-1]+nDays)

        sDT += timedelta(days=nDays)

    if IDX[-1] != len(aSrc):
        IDX.append(len(aSrc))

    return [aSrc[idx1:idx2] for idx1,idx2 in zip(IDX[:-1],IDX[1:])]
'''


def bound2poly(BOUND,outPath=None):
    POLY    = [[]]
    nPOLY   = 0
    for i,point in enumerate(BOUND):
        POLY[nPOLY].append(point)
        if point == POLY[nPOLY][0] and len(POLY[nPOLY])>1:
            POLY.append([])
            nPOLY += 1

    if POLY[-1] == []: POLY.pop()

#    for poly in POLY:print len(poly);x,y=zip(*poly);plot(x,y)
#    show()

    OUT = []
    for poly in POLY:
        poly    = [[i+1,x,y] for i,(y,x) in enumerate(poly)]

        poly.extend([[i+1,i+1,i+2] for i in range(len(poly))])
        poly[-1][-1]    = 1

        poly.insert(0,[len(poly)/2,2,0,0])
        poly.insert(len(poly)/2+1,[len(poly)/2,0])
        poly.append([0])

        OUT.append(poly)

    if outPath != None:
        SIZE    = [len(poly)/2 for poly in OUT]
        maxId   = SIZE.index(max(SIZE))     ## save only single biggest poly
        file(outPath,'w').writelines('\n'.join([' '.join(map(str,point))
                                        for point in OUT[maxId]]))
    return OUT




def mpfunc(func, CHUNK):
    nProc   = len(CHUNK)

    manager = MP.Manager()
    outQ    = manager.Queue()
    errQ    = manager.Queue()
    Lock    = manager.Lock()

###################
    def worker(func,idx,chunk,outQ,errQ,Lock):
        try:
#            Out = [func(*args) for args in mpArgs]
            outQ.put((idx,func(chunk)))
        except Exception,e:
            errQ.put(e)
            return

#        outQ.put((idx,Out))
###################

    kill    = lambda P: [p.terminate() for p in P if p.exitcode is None]

    PROC    = [MP.Process(target=worker,
                          args  = (func,idx,chunk,outQ,errQ,Lock))
                            for idx,chunk in enumerate(CHUNK)]

    try:
        ss  = time.time()
        for p in PROC: p.start()
        for p in PROC: p.join()
        print time.time()-ss,'MP'

    except Exception,e:
        kill(PROC)
        raise e

    if not errQ.empty():
        kill(PROC)
        raise errQ.get()

    ss  = time.time()
    OUT     = [None]*nProc
    while not outQ.empty():
        idx,out = outQ.get()
        OUT[idx]= out
    print time.time()-ss,'qGET'

    return OUT
#    return concatenate(OUT)    #!! too much overhead!!
    lRE     = []
    [lRE.extend(out) for out in OUT]
    return lRE


def climatology(aSrc,dt='mon'):
    if dt != 'mon':
        raise ValueError,'%s is not implemented yet'%dt

    return aSrc.reshape(-1,12,*aSrc.shape[1:]).mean(0),aSrc.reshape(-1,12,*aSrc.shape[1:]).std(0)


def interannual(aSrc,dt='mon',std=False):
    if dt != 'mon':
        raise ValueError,'%s is not implemented yet'%dt

    aClimMean, aClimStd = climatology(aSrc,dt)
    aOut    = aSrc.reshape(-1,12,*aSrc.shape[1:])-aClimMean[None,...]

    if std == True:
        aOut    = aOut/aClimStd[None,...]

    return aOut.reshape(*aSrc.shape)
#    return ((aSrc.reshape(-1,12,*aSrc.shape[1:])-aClimMean[None,...])/aClimStd[None,...]).reshape(*aSrc.shape)


def mask_outline(LatLon,bound='outer',loopshp=True,buffer_pixels=1):
### raster outline
    Lon = LatLon[1].data
    Lat = LatLon[0].data

    mask= ones(array(Lon.shape)+buffer_pixels*2,dtype='bool')
    mask[buffer_pixels:-buffer_pixels,
         buffer_pixels:-buffer_pixels] = LatLon.mask[0]

    MASK= array([vroller(mask,1),vroller(mask,-1),roller(mask,1),roller(mask,-1)])

    mask= mask[buffer_pixels:-buffer_pixels,buffer_pixels:-buffer_pixels]
    MASK= MASK[:,buffer_pixels:-buffer_pixels,buffer_pixels:-buffer_pixels]

    Mask= MASK[0]+MASK[1]+MASK[2]+MASK[3]
    Mask= invert(Mask-mask)

    X1,X2,Y1,Y2 = [],[],[],[]

### delineate coordination
    if bound == 'outer':
        dX0                 = (roller(Lon,-1)-Lon)/2.
        dX0[:,0],dX0[:,-1]  = dX0[:,1],dX0[:,-2]        ## -180, +180 treatment
        dX1                 = (roller(Lon,1)-Lon)/2.
        dX1[:,0],dX1[:,-1]  = dX1[:,1],dX1[:,-2]

        dY0                 = (vroller(Lat,-1)-Lat)/2.
        dY0[0],dY0[-1]      = dY0[1],dY0[-2]            ## -90, +90 treatment
        dY1                 = (vroller(Lat,1)-Lat)/2.
        dY1[0],dY1[-1]      = dY1[1],dY1[-2]

        LON = array([Lon+dX0,Lon+dX1])
        LAT = array([Lat+dY0,Lat+dY1])

    ### lower bnd
        msk = ma.masked_equal(ma.array(MASK[0],mask=Mask).filled(0),0).mask
        lat2= ma.array(LAT[1],mask=msk).compressed()
        lon1= ma.array(LON[0],mask=msk).compressed()
        lon2= ma.array(LON[1],mask=msk).compressed()

        X1.extend(lon1);X2.extend(lon2);Y1.extend(lat2);Y2.extend(lat2)
#        LOWER   = map(None,lon1,lat2,lon2,lat2)

    ### upper bnd
        msk = ma.masked_equal(ma.array(MASK[1],mask=Mask).filled(0),0).mask
        lat1= ma.array(LAT[0],mask=msk).compressed()
        lon1= ma.array(LON[0],mask=msk).compressed()
        lon2= ma.array(LON[1],mask=msk).compressed()

        X1.extend(lon1);X2.extend(lon2);Y1.extend(lat1);Y2.extend(lat1)
#        UPPER   = map(None,lon1,lat1,lon2,lat1)

    ### right bnd
        msk = ma.masked_equal(ma.array(MASK[2],mask=Mask).filled(0),0).mask
        lat1= ma.array(LAT[0],mask=msk).compressed()
        lat2= ma.array(LAT[1],mask=msk).compressed()
        lon2= ma.array(LON[1],mask=msk).compressed()

        X1.extend(lon2);X2.extend(lon2);Y1.extend(lat1);Y2.extend(lat2)
#        RIGHT   = map(None,lon2,lat1,lon2,lat2)

    ### left bnd
        msk = ma.masked_equal(ma.array(MASK[3],mask=Mask).filled(0),0).mask
        lat1= ma.array(LAT[0],mask=msk).compressed()
        lat2= ma.array(LAT[1],mask=msk).compressed()
        lon1= ma.array(LON[0],mask=msk).compressed()

        X1.extend(lon1);X2.extend(lon1);Y1.extend(lat1);Y2.extend(lat2)
#        LEFT    = map(None,lon1,lat1,lon1,lat2)

    elif bound == 'center':
        X1.extend(Lon)
    else:
        raise ValueError,'wrong option: %s'%bound

    OUT = map(None,X1,Y1,X2,Y2)

    if loopshp == True:
        x1,y1,x2,y2 = OUT.pop()
        RE  = [(x1,y1),(x2,y2)]

        lenOUT  = len(OUT)
        NoneIdx = 0
        while len(OUT)>0:
            for nCnt,out in enumerate(OUT):
                lastPnt = RE[-1]

                if out[2:] == lastPnt:
                    x1,y1,x2,y2 = OUT.pop(nCnt)
                    RE.append((x1,y1))

                elif out[:2] == lastPnt:
                    x1,y1,x2,y2 = OUT.pop(nCnt)
                    RE.append((x2,y2))

            dLenOUT = lenOUT-len(OUT)
            lenOUT  = len(OUT)

            ### insert (None,None) when come back to start point and nothing matches
            sPoint  = RE[0] if NoneIdx==0 else RE[NoneIdx+1]
            if RE[-1]==sPoint and dLenOUT==0:
                x1,y1,x2,y2 = OUT.pop(0)
                RE.extend([(None,None),(x1,y1),(x2,y2)])

                NoneIdx = [i for i,crd in enumerate(RE) if crd==(None,None)][-1]


        return Mask,RE

    else:
        return Mask,OUT


def getDTIME(sYYYYMMDD,eYYYYMMDD,dT=None):
    '''
    type(YYYYMMDD)  = number, str
    dT          = # of hours(YYYYMMDD), days(YYYYMM), months(YYYY) : default
                in  ['mon','day','hour'] with # of dT (e.g., '2day', '6hour')
    '''
    sYYYYMMDD   = str(sYYYYMMDD)
    eYYYYMMDD   = str(eYYYYMMDD)

    sYear   = int(sYYYYMMDD[:4])
    eYear   = int(eYYYYMMDD[:4])

    sMon    = int(sYYYYMMDD[4:6]) if len(sYYYYMMDD[4:6])!=0 else 1
    eMon    = int(eYYYYMMDD[4:6]) if len(eYYYYMMDD[4:6])!=0 else 1

    sDay    = int(sYYYYMMDD[6:8]) if len(sYYYYMMDD[6:8])!=0 else 1
    eDay    = int(eYYYYMMDD[6:8]) if len(eYYYYMMDD[6:8])!=0 else 1

    sHour   = int(sYYYYMMDD[8:10]) if len(sYYYYMMDD[8:10])!=0 else 0
    eHour   = int(eYYYYMMDD[8:10]) if len(eYYYYMMDD[8:10])!=0 else 0

    if dT == None:
        if len(sYYYYMMDD) == 4:
            dT  = 'mon'

        elif len(sYYYYMMDD) == 6:
            dT  = 'mon'

        elif len(sYYYYMMDD) == 8:
            dT  = 'day'

        elif len(sYYYYMMDD) == 10:
            dT  = 'hour'


    if dT in ['mon','day','hour']:
        dT  = '1'+dT

    nDT,dT  = re.match(r'(\d+)(\D+)',dT).groups()
    nDT     = int(nDT)

    if dT == 'mon':
        nMonth  = eYear*12+eMon-(sYear*12+sMon)+1

        DTIME   = [datetime(sYear+(sMon+m)//12 if (sMon+m)%12 !=0 else sYear+(sMon+m)//12-1,
                           (sMon+m)%12         if (sMon+m)%12 !=0 else 12,
                            sDay,sHour)
                            for m in range(0,nMonth,nDT)]

    elif dT == 'day':
        sDTime  = datetime(sYear,sMon,sDay,sHour)
        eDTime  = datetime(eYear,eMon,eDay,eHour)+timedelta(days=1)

        DTIME   = [sDTime+timedelta(days=d) for d in range(0,(eDTime-sDTime).days,nDT)]

    elif dT == 'hour':
        sDTime  = datetime(sYear,sMon,sDay,sHour)
        eDTime  = datetime(eYear,eMon,eDay,eHour)+timedelta(seconds=1)

        dTime   = eDTime-sDTime
        dSec    = dTime.days*86400+dTime.seconds+1

        DTIME   = [sDTime+timedelta(seconds=s) for s in range(0,dSec,nDT*3600)]

    else:
        raise ValueError,'%s is not valid dT argu'%dT

    return DTIME


def key2slice(KEY,shape=None):

    K   = [k for k in KEY] if hasattr(KEY,'__iter__') else [KEY]

    if shape == None:
        shape   = [None]*len(K)

    # fill default when give # of slice,indices < array.ndim
    if len(K) <= len(shape):
        [K.insert(K.index(Ellipsis),None) if Ellipsis in K else K.append(None)
                            for i in range(len(shape)-len(K))]

    else:
        raise ValueError,'given shape or indices is not allowed.'

    reducedFLAG = [True if type(k) in [int] else False for k in K]
    K           = [slice(k,k+1,1) if type(k) in [int] else k for k in K]

    SLICE   = []
    typeK   = []
    for shp,k in map(None,shape,K):
        if k in [None,Ellipsis]: k = slice(0,shp,1)

        if isinstance(k,slice):
            k   = slice(
                    k.start if k.start != None else 0,
                    k.stop  if k.stop  != None else shp,
                    k.step  if k.step  != None else 1
                    )

            print k
            if k.step  < 0 and k.step  != None or \
               k.start < 0 and k.start != None or \
               k.stop  < 0 and k.stop  != None:
                raise ValueError, 'NEGATIVE INDEX is yet supported.'
                k   = slice(k.stop,k.start,k.step)

            typeK.append(True)

        SLICE.append(k)


    return SLICE,reducedFLAG


def ConvertMapType(aSrc,mapTypeFrom, mapTypeTo, BBox=None):
    '''
    !!WARNING!! It does NOT support REGIONAL SUBSET yet. Use ONLY for GLOBAL.

    aSrc    : ndarray with lat (axis=-2) lon (axis=-1)
    mapType : ['u','v','^','n']
    '''

    verType = {'u':-90, '^':-90,
               'n':90,'v':90,}

    horType = {'u':0,   'n':0,
               'v':-180,'^':-180,}

    vFrom   = verType[mapTypeFrom]
    vTo     = verType[mapTypeTo]
    hFrom   = horType[mapTypeFrom]
    hTo     = horType[mapTypeTo]

    vSlice  = [Ellipsis,slice(None,None,-1),slice(None,None,None)] if vFrom != vTo else [Ellipsis]

    return roller(aSrc[vSlice]) if hFrom != hTo else aSrc[vSlice]


def extractMask(aSrc,mask,outIdx=False):
    '''
    [IN]
    aSrc    : n-dimensional array (n>=2)
    mask    : 2d boolean array

    [OUT]
    extracted array
    indices to extract (optional)
    '''

    nX, nY  = mask.T.shape
    X,Y     = meshgrid(xrange(nX),xrange(nY))

    X       = ma.array(X,mask=mask).compressed()
    Y       = ma.array(Y,mask=mask).compressed()

    if outIdx == True:
        return aSrc[...,Y,X], [Y,X]
    else:
        return aSrc[...,Y,X]


def fillinMask(aSrc,mask,aDes=None,fill_value=-999.):
    '''
    [IN]
    aSrc        : vector array (1d)
    mask        : 2d boolean array
    aDes        : n-dimensional target array (n>=2)
    fill_value  : float constant

    [OUT]
    aDes filled with aSrc
    '''
    nX, nY  = mask.T.shape
    X,Y     = meshgrid(xrange(nX),xrange(nY))

    X       = ma.array(X,mask=mask).compressed()
    Y       = ma.array(Y,mask=mask).compressed()

    outShp  = aSrc.shape[:-1]+(nY,nX)
    outType = aSrc.dtype

    aDes    = zeros(outShp,dtype=outType)+fill_value if aDes==None else aDes
    aDes[...,Y,X] = aSrc
    return aDes



def divide2d( aSrc, divShp, opt='oo' ):#, **kwargs ):
    '''
    * divide 2d map into small rectagular domains

    aSrc    : 2d-array
    divShp  : inner or outer domain size

    opt     : 'oo'  - divShp (outer) / order (outer)
              'oi'  - divShp (outer) / order (inner)
              'io'  - divShp (inner) / order (outer)
              'ii'  - divShp (inner) / order (inner)

    ex) divide2d( zeros(180,360), (2,2), 'oo').shape    = (2,2,90,180)
        divide2d( zeros(180,360), (2,2), 'oi').shape    = (90,180,2,2)
        divide2d( zeros(180,360), (2,2), 'io').shape    = (90,180,2,2)
        divide2d( zeros(180,360), (2,2), 'ii').shape    = (2,2,90,180)
    '''

    nY, nX  = aSrc.shape

    Shp,Ord = opt

    if   Shp  == 'o':
        outerShp    = divShp
        innerShp    = (nY/divShp[0], nX/divShp[1])

    elif Shp == 'i':
        outerShp    = (nY/divShp[0], nX/divShp[1])
        innerShp    = divShp

    else:
        raise ValueError, '%s is not correct opt.'


    if   Ord    == 'o':
        transAxis   = (0,2,1,3)

    elif Ord    == 'i':
        transAxis   = (1,3,0,2)

    else:
        raise ValueError, '%s is not correct opt.'

    return aSrc.reshape(outerShp[0],
                        innerShp[0],
                        outerShp[1],
                        innerShp[1]
                        ).transpose(*transAxis)


