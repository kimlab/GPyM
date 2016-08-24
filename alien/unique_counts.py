from    numpy           import bincount, nonzero


def unique_counts(aSrc):
    '''
    aSrc    : 1d-array

    ### numpy v1.9 included faster implimentation @ np.unique
    '''
    print aSrc

    bincnt          = bincount( aSrc )
    elements        = nonzero( bincnt )[0]

    return array( zip( bincnt, elements ) ).T
