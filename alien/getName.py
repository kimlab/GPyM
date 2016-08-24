import sys

def getFuncName():
    return sys._getframe(1).f_code.co_name

def getCallerName():
    return sys._getframe(2).f_code.co_name

