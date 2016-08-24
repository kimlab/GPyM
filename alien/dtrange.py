#from pylab import *
from datetime import datetime,timedelta


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

