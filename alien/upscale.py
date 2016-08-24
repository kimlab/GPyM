from numpy      import array, ma


def upscale(aSrc,newShape,mode='s',weight=None,post_weight=None,missing=None):
    '''
    aSrc[y,x] => aSrc[*newshape]

    mode = [
            's',    # aggregate
            'ws',   # weighted aggregation
            'm'     # mean
            ]
    '''

    if weight != None:
        aSrc    = aSrc.copy()* weight


    '''
    modeFunc    = {'s':sum,
                   'm':mean,
    }[mode]
    '''

    if len(aSrc.shape)==3 and aSrc.shape[0]==1:
        aSrc.shape  = aSrc.shape[1:]


    if all( array(newShape) > array(aSrc.shape) ):
        nFOLD    = newShape/array(aSrc.shape)

        aRe     = empty(newShape, dtype=aSrc.dtype)

        for i in range(nFOLD[0]):
            for j in range(nFOLD[1]):
                aRe[i::nFOLD[0], j::nFOLD[1]]   = aSrc

    else:
        nFOLD    = array(aSrc.shape)/newShape

        if missing == None:
            aRe = array([
                        aSrc[..., i::nFOLD[-2], j::nFOLD[-1]]
                            for i in range(nFOLD[-2])
                                for j in range(nFOLD[-1])
                                ])

        else:
            aSrc    = ma.masked_equal(aSrc,missing)

            aRe = array([
                        aSrc.data[..., i::nFOLD[-2], j::nFOLD[-1]]
                            for i in range(nFOLD[-2])
                                for j in range(nFOLD[-1])
                                ])

            Mask= array([
                        aSrc.mask[..., i::nFOLD[-2], j::nFOLD[-1]]
                            for i in range(nFOLD[-2])
                                for j in range(nFOLD[-1])
                                ])

            aRe = ma.array(aRe,mask=Mask)


        if   mode == 's':
            aRe = aRe.sum(0)

        elif mode == 'ws':
            weight  = len(aRe)/(len(aRe)-Mask.astype('float64').sum(0))

            aRe = aRe.sum(0)*weight

        elif mode == 'm':
            aRe = aRe.mean(0)

        else:
            raise IOError

        if missing != None:
            aRe = aRe.filled(missing)

    if post_weight != None:
        aRe *= post_weight

    return aRe

