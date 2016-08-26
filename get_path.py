#! /usr/bin/python
#--------------------------------------------------------------------
# PROGRAM    : get_path.py
# CREATED BY : hjkim @IIS.2015-07-13 13:02:05.942756
# MODIFED BY :
#
# USAGE      : $ ./get_path.py
#
# DESCRIPTION:
#------------------------------------------------------cf0.2@20120401


import  os,sys
from    optparse        import OptionParser

from    parse_fname_trmm    import parse_fname_trmm
from    parse_fname_gpm     import parse_fname_gpm


def get_path(srcDir, sDTime, eDTime):
    '''
    select GPM(hdf5) and TRMM(hdf4) files and return their paths)
    '''

    prjName, prdLv, prdVer  = srcDir.split(os.path.sep)[-3:]

    parse_fname     = {'TRMM': parse_fname_trmm,
                       'GPM' : parse_fname_gpm}[ prjName.split('.')[0] ]


    if sDTime == eDTime:
        raise ValueError, '%s == %s'%(sDTime, eDTime)



    # do not know the reason of implementation ++++++++++++++++++++++
    # consider to use trange
    #srcDIR  = [os.path.join(srcDir, '%i/%02d'%(y,m))
    srcDIR  = [os.path.join(srcDir, str(y), '%02d'%m)
                            for y in range(sDTime.year,eDTime.year+1)
                                for m in range(1,13)]

    srcDIR  = srcDIR[sDTime.month-1 : eDTime.month-12 if eDTime.month != 12 else 12]
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    srcPATH = []

    for srcDir in srcDIR:
        if not os.path.exists(srcDir):
            print 'Warning [%s] directory does not exists!'%srcDir
            continue

        for srcFName in sorted( os.listdir(srcDir) ):

            sdt_gtrk, edt_gtrk  = parse_fname( srcFName, ['sDTime','eDTime'] )

            if sDTime <= edt_gtrk and eDTime >= sdt_gtrk:
                srcPATH.append( os.path.join(srcDir, srcFName) )
            else:
                continue

    return srcPATH



def main(args,opts):
    print args
    print opts

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


