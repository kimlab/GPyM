#! /usr/bin/python
#--------------------------------------------------------------------
# PROGRAM    : __main__.py
# CREATED BY : hjkim @IIS.2015-07-13 15:46:30.658570
# MODIFED BY :
#
# USAGE      : $ ./__main__.py
#
# DESCRIPTION:
#------------------------------------------------------cf0.2@20120401


import  os,sys
from    optparse        import OptionParser
from    cf.util.LOGGER  import *

from    datetime        import datetime, timedelta

from    gpm             import GPM


@ETA
def main(args,opts):
    print args
    print opts


    prjName = 'GPM.KuPR'
    prdLv   = 'L2'
    prdVer  = '02'
    varName = 'NS/SLV/precipRateESurface'

    prjName = 'GPM.GMI'
    prdLv   = 'L2'
    prdVer  = '02'
    varName = 'S1/surfacePrecipitation'


    BBox    = [[20,118],[48,150]]   # Radar-AMeDAS domain
    res     = 0.1
    delT    = timedelta(seconds=60*60)

    sDTime  = datetime( 2014,4,30 )
    #eDTime  = datetime( 2014,4,2) #,0,59)
    eDTime  = datetime( 2014,5,3 )
#    eDTime  = datetime( 2014,5,15 )

    print sDTime, eDTime
    from pylab                  import *
    from mpl_toolkits.basemap   import Basemap

    M   = Basemap( resolution='c' ,llcrnrlat=BBox[0][0], llcrnrlon=BBox[0][1], urcrnrlat=BBox[1][0], urcrnrlon=BBox[1][1])


    gpm     = GPM(prjName, prdLv, prdVer)

    JP      = gpm(varName,
                  #datetime(2014,4,19),
                  datetime.datetime(2014,4,1),
                  datetime.datetime(2014,5,1),
                  BBox,
                  #[[30,125],[45,145]],
                  0.2,
                  )
    '''
                  0.1,
                  datetime.timedelta(seconds=3600*24))
    '''

    A   = ma.masked_less_equal( array( JP.griddata ), 0 )
    figure();M.imshow( A.mean(0) );colorbar()
    #figure();M.scatter(JP.lon.flatten(), JP.lat.flatten(), 10, JP.data.flatten(), edgecolor='none',vmin=0,vmax=10);colorbar()
    M.drawcoastlines()
    show()

    sys.exit()
    gpmJP   = gpm('NS/SLV/precipRateESurface', sDTime, eDTime, BBox, res, delT )

    A   = array( gpmJP.griddata )

    '''
    # for no delT
    Lon     = gpmJP.lon
    Lat     = gpmJP.lat
    Data    = gpmJP.data

    M.scatter(Lon.flatten(), Lat.flatten(), 10, Data.flatten(), edgecolor='none',vmin=0,vmax=10);colorbar()
    M.drawcoastlines()
    '''

    # for with delT
    Lon     = gpmJP.lon
    Lat     = gpmJP.lat
    Data    = gpmJP.data

    for lat, lon, data in zip(Lat, Lon, Data):
        figure()
        M.scatter(lon.flatten(), lat.flatten(), 10, data.flatten(), edgecolor='none',vmin=0,vmax=10);colorbar()
        M.drawcoastlines()

    show()

    print A.shape, A.max(), A.min()
    for a in A: print a.shape, a.max(), a.min()
    print gpmJP.data.min(), gpmJP.data.max()


    for a in gpmJP.griddata:
        print a.shape
        figure()
        M.imshow( ma.masked_equal(array(a), -9999.9),vmin=0,vmax=10);colorbar()
        M.drawcoastlines()


    figure()
    M.imshow( ma.masked_equal(A, -9999.9).sum(0),vmin=0,vmax=10);colorbar()
    M.drawcoastlines()


    show()

    '''
    Path    = gpm.get_path(sDTime, eDTime)

    for i in range(5):

        s=time.time()
        DTime, Lat, Lon     = gpm.get_gtrack(Path[i])


        print time.time()-s
    '''



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


