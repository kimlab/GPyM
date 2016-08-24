import os,sys
from        numpy           import arange, linspace, meshgrid, zeros, fromfile, concatenate
from        numpy           import loadtxt, argmax

from    unique_counts       import unique_counts

def conv180to360(lon):
    ''' convert between -180~180 and 0~360 '''
    if hasattr(lon,'__iter__'): return where(lon >= 0,array(lon), 360.+array(lon))
    else: return lon if lon >=0 else 360+lon

def conv360to180(lon):
    ''' convert between 0~360 and -180~180 '''
    if hasattr(lon,'__iter__'): return where(lon >= 180,array(lon)-360., array(lon))
    else: return lon-360. if lon >=180 else lon

def nearest_idx(aSrc,val):
    ''' return nearest index '''
    if hasattr(val,'__iter__'): return [abs(aSrc-v).argmin() for v in val]
    else: return abs(aSrc-val).argmin()

def detect_map_direction(aSrc, yAxis=-2, xAxis=-1):
    '''
    aSrc :  2d-array

    # only support global yet.
    '''

    resY    = 180./aSrc.shape[yAxis]
    resX    = 360./aSrc.shape[xAxis]

    YsampleIdx      = int(resY*30)

    unique_cnt_Y0   = unique_counts(aSrc[ YsampleIdx])[0]
    unique_cnt_Y1   = unique_counts(aSrc[-YsampleIdx])[0]

    print most_frq_val_Y1, most_frq_val_Y0

    return


class GridCoordinates(object):
    def __init__(self, mapCode, hres=None, vres=None, BBox=None):
        '''
        mapCode            = presets ['trip05','cru','u','v','^','n',...]
        #BBox=[[-90,90],[0,360]], res=1.0):
        '''
        self.setup_grid(mapCode, hres, vres, BBox)

    def setup_grid(self, mapCode, hres=None, vres=None, BBox=None):
        for i,s in enumerate(mapCode):
            if s.isdigit(): break                # find location of res.

        mapType, res        = mapCode[:i],mapCode[i:]

        if i == len(mapCode)-1:                        # when res. not given
            mapType        = mapCode                # 1.0 degree assumed
            res                = '1'

        res        = float( res[0] + '.' + res[1:] )   # conv. res. to float
        hres        = res
        vres        = res

        if BBox        == None:
            left, right        = [-180.0, 180.0] if mapType in ['v','^'] else [0.0, 360.0]
            bottom, top = [90.0, -90.0] if mapType in ['v','n'] else [-90.0,90.0]

            BBox        = [[left,right], [top,bottom]]

        else:
            bottom, left    = BBox[0]
            top, right      = BBox[1]

        hoff    = hres/2.
        width        = right-left
        nJ        = width/hres

        voff    = vres/2. if bottom < top else -vres/2.
        height        = top-bottom if bottom < top else bottom-top
        nI        = height/vres


        lon = linspace(left+hoff,right-hoff, nJ)
        lat = linspace(bottom+voff, top-voff, nI)

        self.mapType        = mapType

        self.res        = res
        self.vres        = vres
        self.hres        = hres

        self.BBox        = BBox

        self.lat        = lat
        self.lon        = lon

        self.nI                = nI
        self.nJ                = nJ

        self.Lon, self.Lat  = meshgrid(lon,lat)

        self.conv180to360   = conv180to360
        self.conv360to180   = conv360to180


    def get_idx(self, Y, X ,nearest=False, shift_lon=False):
        '''
        X :        Longitude(s)        /* float or iterable */
        Y :        Latitude(s)        /* float or iterable */
        '''

        if shift_lon == True:
            fnConv   = self.conv360to180    if self.mapType in ['v','^']    else self.conv180to360
            X        = fnConv(X)

        if nearest == True:
            j   = nearest_idx(self.lon,X)
            i   = nearest_idx(self.lat,Y)

        else:
            lon = self.lon.tolist()
            lat = self.lat.tolist()

            j        = [lon.index(x) for x in X] if hasattr(X,'__iter__') else lon.index(X)
            i        = [lon.index(y) for y in Y] if hasattr(Y,'__iter__') else lat.index(Y)

        return i, j


    def get_crd(self, I, J):
        return self.lat[J], self.lon[I]


    def get_domain_idx(self, BBox, mode='nearest', shift_lon=False):
        '''
        BBox :            [ [south, west], [north, east] ]
        mode :            [ 'nearest', 'exact', 'inner' ,'outter']
                    * both 'inner' and 'outer' include bounds *
        '''

        [south, west], [north, east]        = BBox

        nearest            = False if mode == 'exact'        else True

        llcr_idx    = self.get_idx( south, west, nearest=nearest, shift_lon=shift_lon )
        urcr_idx    = self.get_idx( north, east, nearest=nearest, shift_lon=shift_lon )

        sn_idx            = [llcr_idx[0], urcr_idx[0]]
        we_idx            = [llcr_idx[1], urcr_idx[1]]

        if self.mapType in ['n', 'v']:   sn_idx = sn_idx[::-1]

        ####!!!! add treatment for 'inner' and 'outter' !!!!####
        return [ [ sn_idx[0], we_idx[0] ], [ sn_idx[1], we_idx[1]] ]


    def get_domain_data(self, aSrc, BBox, mode='nearest', shift_lon=False):

        bbox_idx    = self.get_domain_idx( BBox, mode=mode, shift_lon=shift_lon )
        print 'bbox_idx', bbox_idx

        return aSrc[...,
                    bbox_idx[0][0]:bbox_idx[1][0],
                    bbox_idx[0][1]:bbox_idx[1][1]]


    def cut_domain(self, BBox, mode='nearest', shift_lon=False):
        return GridCoordinates( BBox )


    def __repr__(self):

        sOut        = '\n'.join( [self.mapType,
                #        self.res, self.vres,
#        self.hres,
#        self.BBox,
#        self.lat, self.lon,
#        self.nI,
#        self.nJ,
#        self.Lon.shape, self.Lat.shape
] )

        return sOut



def main(*args):

    grid    = GridCoordinates('u05')
    print '+'*80
    grid    = GridCoordinates('v')

    vasc    = VASClimO('10')
    vasc(1951,2000)

    figure();imshow(vasc.data.mean(0));colorbar()
    print vasc.get_idx( 38.5, -0.5 )
    print vasc.get_idx( 38.5, 359.5, shift_lon=True )

    BBox        = [[66.5,85.5],[70.5,170.5]]
    BBox        = [[-10.5,10.5],[-60.5,-30.5]]
    aSrc        = vasc.get_domain_data(vasc.data, BBox, shift_lon=True)

    print vasc.data.shape
    print vasc.yr.shape
    print aSrc.shape

    print vasc.data.max()

    figure();plot( ma.masked_equal( aSrc,-999).mean(-1).mean(-1) )

    show()


if __name__=='__main__':
    main(sys.argv)
