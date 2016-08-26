import os,sys,time
from datetime       import datetime
from TextArt        import TextArt
from getName        import getFuncName, getCallerName
from AnsiFormatter  import AnsiFormatter


def ETA(func):
    ta  = TextArt()

    def inner(*args, **kwargs):
        clr     = ta.g  # Ansi Color 'g':green

#        funcName    = func.__name__ if func != None else None
        HEADER  = (ta.Ln,
                   '| ETA |',
                   '\t+ func <%s>\tcalled by <%s>\n'%(
#                       funcName,
                       func.__name__,
                       getCallerName()
                       ),
                   ta.ln)

        print clr+''.join(HEADER)

        sTime   = datetime.now()
        retval  = func(*args,**kwargs)
        eTime   = datetime.now()

        FOOTER  = (ta.ln,
                   '\t  - args   [%s]\n'%str(args),
                   '\t  - kwargs [%s]\n'%str(kwargs),
                   '\t  - return %s %s\n'%(
                        type(retval),
                        'in LENGTH of %i'%len(retval) if hasattr(retval,'__iter__') else ''
                        ),
                   '\t  - lapse  %-53s | ETA |\n'%(eTime-sTime),
                   ta.Ln)

        print clr+'%s'*len(FOOTER)%FOOTER

        return retval

    return inner


class LOGGER(object):
    '''
    LOG = LOGGER()
    LOG.on
    LOG.off
    LOG.color (['black','red','green',...])
    '''

    def __init__(self, logPath=None, mode=None):
        ta  = TextArt()

        self.sDTime = datetime.now()

        if logPath == None:
            logFName    = 'cmdline' if sys.argv[0] == '' else '_'.join(sys.argv)
            logFExt     = 'log@'+self.sDTime.strftime('%Y%m%d')

            logFName    = '%s.%s'%(logFName,logFExt)

            logPath = os.path.join(settings.LOG_DIR,logFName)


        logDir  = os.path.dirname( logPath )
        #logDir  = '/'.join(logPath.split('/')[:-1])

        if not os.path.exists(logDir) and logDir != '':
            os.makedirs(logDir)

        if mode == None:    mode='a'

        HEADER  = ('\n',
                   ta.LN,
                   '* logfile path\t%s\t<mode: %s>\n'%(logPath,mode),
                   '* by %s\t@%s:%s\n'%(
                        os.environ['USER'],
                        os.uname()[1],          # patch by HJKIM@20130917
#                        os.environ['HOSTNAME'],
                        os.environ['PWD'],
                        ),
                   ta.Ln,
                   '* executed FILE <%s>\t'%sys.argv[0],
                       'with ARGS %s\n'%str(sys.argv[1:]),
                   '* started DTIME <%s>\n'%self.sDTime,
                   ta.LN)

        logHeader   = '%s'*len(HEADER)%HEADER

        self.status     = 'off'
        self.mode       = mode
        self.logPath    = logPath

        self.clr('y')
        self.write(logHeader)
        self.clr('reset')


    def __del__(self):
        ta  = TextArt()
        eDTime  = datetime.now()
        FOOTER  = (ta.LN,
                   '* ended   DTIME <%s>\tLapse: %s\n'%(
                                eDTime,
                                eDTime-self.sDTime
                                ),
                   ta.LN)

        logFooter   = '%s'*len(FOOTER)%FOOTER

        self.clr('y')
        self.write(logFooter)
        self.clr('reset')

        self.off


    def write(self, data, mode=None):
        self.file.write(data)
        self.stdout.write(self.color+data)


    @property
    def on(self):
        if self.status == 'off':
            # duplicate stdout -> stdout & file
            self.file = open(self.logPath, self.mode)
            self.stdout = sys.stdout
            sys.stdout = self

            self.status= 'on'


    @property
    def off(self):
        if self.status == 'on':
            sys.stdout = self.stdout
            self.file.close()

            self.status= 'off'


    def clr(self,color):
        if self.status == 'off':
            self.on

        self.color  = AnsiFormatter(color)


'''
def printvar(var):
    for k,v in locals().items():
        if v==var:  break

    print '\t@var: %s15'%k,var
'''


if __name__=='__main__':

    @ETA
    def test(text):
        print 'print in "test" func: %s'%(text*3)
        return text,text

    def main(*args):
        print 'print in "main" func: %s'%str(args)
        print test('gogogo ')


    LOG = LOGGER()

    LOG.clr('r')
    print 'test_red'
    LOG.clr('b')
    print 'test_blue'
    print 'LOG.off'
    LOG.off
    print 'test.off'
    LOG.on
    print 'LOG.on'

    LOG.clr('g')
    print 'test_green'
    LOG.clr('reset')
    print 'test @ETA'
    main(*sys.argv)


