#! /usr/bin/python
#--------------------------------------------------------------------
# PROGRAM    : search_granules.py
# CREATED BY : hjkim @IIS.2015-07-13 12:59:51.759752
# MODIFED BY :
#
# USAGE      : $ ./search_granules.py
#
# DESCRIPTION:
#------------------------------------------------------cf0.2@20120401


import  os,sys
from    optparse        import OptionParser

from    numpy           import arange, ma

from    get_path        import get_path
from    get_gtrack_dim  import get_gtrack_dim


class SearchGranules( object ):
    def search_granules(self, srcDir, sDTime, eDTime, BBox=[[-90,-180],[90,180]], thresh=0.001):
        '''
        BBox    : [[lllat,lllon], [urlat,urlon]]    /* lat: -90 ~ 90 */
                                                    /* lon: -180 ~ 180 */
        '''

        srcPATH = get_path(srcDir, sDTime, eDTime)

        gtrkDim = [get_gtrack_dim(path, self.func_read, self.cached, self.cacheDir)
                                                                for path in srcPATH]

        DTime, Lat, Lon     = zip(*gtrkDim)

        Granule     = []
        for dtime, lat, lon, path in map(None, DTime, Lat, Lon, srcPATH):

            mskLat  = ma.masked_outside( lat, BBox[0][0], BBox[1][0] ).mask
            mskLon  = ma.masked_outside( lon, BBox[0][1], BBox[1][1] ).mask
            mskTime = ma.masked_outside( dtime, sDTime, eDTime).mask

            #mask    = (mskLat + mskLon).any(1) + mskTime
            mask    = (mskLat + mskLon).all(1) + mskTime

            if not mask.all():

                idx = ma.array( arange(dtime.size), 'int', mask=mask).compressed()
                Granule.append([path,
                                dtime[idx],
                                lat[idx],
                                lon[idx],
                                idx
                                ])

                print('* [V] ground track dimension (%s): %s'%(self.cached,path))

            else:
                print('* [_] ground track dimension (%s): %s'%(self.cached,path))

        summary = '| [{}] granules intersects domain {} out of [{}] total between ({}-{}) |\n'    \
                  .format( len(Granule), tuple(BBox), len(srcPATH), sDTime, eDTime )

        line    = '+' + '-'*len(summary[3:]) + '+\n'

        print(line + summary + line)

        return Granule




def main(args,opts):
    print (args)
    print (opts)

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


