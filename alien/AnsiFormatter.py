class AnsiFormatter( object ):
    """
    c = AnsiFormatter( 'cyan' )
    r = AnsiFormatter( 'red'  )
    y = AnsiFormatter( 'yellow'  )
    m = AnsiFormatter( 'magenta'  )
    c + 'hello ?'
    prints 'hello ?' with cyan color

    contribution by H.T. Kim @ 20120610
    """

    FOREGROUND = dict(
        black   = 30, k = 30,
        red     = 31, r = 31,
        green   = 32, g = 32,
        yellow  = 33, y = 33,
        blue    = 34, b = 34,
        magenta = 35, m = 35,
        cyan    = 36, c = 36,
        white   = 37, w = 37,
        reset   = 39, 
    )

    BACKGROUND = dict(
        black   = 40,
        red     = 41,
        green   = 42,
        yellow  = 43,
        blue    = 44,
        magenta = 45,
        cyan    = 46,
        white   = 47,
        reset   = 49,
    )

    def __init__( self, foreground ):
        self.fore = self.FOREGROUND.get( foreground )
        self.back = self.BACKGROUND.get( foreground )
        if not self.fore: raise Exception( "Couldn't understand the name", foreground )

    def __add__( self, other ):
        return '\033[%sm%s\033[0m' % ( self.fore, other )
