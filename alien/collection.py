#! /usr/bin/python

import  os,sys
from    cStringIO       import StringIO

from numpy              import load, save, array
from numpy.lib.format   import open_memmap


#def cached(mode='normal',cacheName=None,cacheDir='./cached',compress='lz4'):
def cached(name=None, dir='./cached', compress=False, mode='cached', verbose=True, purge_empty_file=True):
    '''
    mode : in ['cached',    # read from cached file if exists
               'skip'  ,    # skip caching process
               'update'     # force to update cached file
               ] or False

    compress : in ['lz4', False]
    '''


    def wrapper(func):

        def inner(*args, **kwargs):
            mode        = wrapper.mode
            name        = wrapper.name
            dir         = wrapper.dir
            compress    = wrapper.compress
            verbose     = wrapper.verbose

            if mode in [False, 'skip']      :   return func( *args, **kwargs )

            if name == None                 :   name = func.__name__
            if not os.path.exists(dir)      :   os.makedirs(dir)

            cachePath   = os.path.join(dir, name)

            if compress                     :   import lz4


            if os.path.exists( cachePath ) and mode != 'update':

                if compress == 'lz4':
                    cached  = StringIO( lz4.loads( open(cachePath,'r').read() ) )

                else:
                    cached  = open(cachePath,'r')

                if verbose: print '\t!! Cached from %s'%cachePath

                aOut    = load( cached )

                if aOut.shape != () or purge_empty_file == False:
                    return aOut

                else:
                    os.remove( cachePath )
                    raise ValueError, 'empty cache file (erased): %s'%(cachePath)

            if os.path.exists( cachePath ) == False or mode == 'update':
                aOut    = func( *args, **kwargs )

                if compress == 'lz4':

                    cached  = StringIO()
                    save( cached, aOut )
                    open(cachePath,'w').write( lz4.dumps( cached.getvalue() ) )

                else:
                    save( open(cachePath,'w'), aOut )

                if verbose: print '\t!! Cached to %s'%cachePath
                return aOut

            raise KeyError, 'failed exception handling for %s and %s'%( cachePath, mode )

        return inner

    wrapper.name        = name
    wrapper.mode        = mode
    wrapper.dir         = dir
    wrapper.compress    = compress
    wrapper.verbose     = verbose

    return wrapper


# push_cache, pop_cache
def push_cache(aOut,varName,itrmCode,timeCode,cacheDir=None,ow=False):
    if cacheDir == None:
        baseDir = './cached/%s.%s'%(varName,itrmCode)

    else:
        baseDir = cacheDir

    if not os.path.exists(baseDir):
        os.makedirs(baseDir)

    outPath = os.path.join(baseDir,'%s.%s.%s.npy'%(varName,itrmCode,timeCode))

    if os.path.exists(outPath) and ow == False: # file size and array size compare [ToDo]
        return False

    else:
        save(outPath, aOut.astype('float32'))   # better dtype treatment [ToDo]
        return True


def pop_cache(varName,itrmCode,timeCode,func,args,cacheDir=None,cache=True,mmap=None,returnTF=False):
    if cacheDir == None:
        baseDir = './%s.%s'%(varName,itrmCode)

    else:
        baseDir = cacheDir

    srcPath = os.path.join(baseDir,'%s.%s.%s.npy'%(varName,itrmCode,timeCode))

    if os.path.exists(srcPath) and cache != 'ow':
        aSrc    = load(srcPath, mmap_mode=mmap)

    else:
        # replace None with srcPath to cache
        if func == open_memmap:
            if not os.path.exists(baseDir):
                os.makedirs(baseDir)

            aSrc= func(srcPath, *args)

        else:
            aSrc    = func(*args)

            ow      = True if cache == 'ow' else False

            if cache == True:
                push_cache(aSrc,varName,itrmCode,timeCode,cacheDir=cacheDir,ow=ow)

    if returnTF :   return aSrc,False
    else        :   return aSrc
