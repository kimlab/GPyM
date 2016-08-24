import sys
from AnsiFormatter  import AnsiFormatter


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

