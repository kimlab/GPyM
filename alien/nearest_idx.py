def nearest_idx(aSrc,val):
    ''' return nearest index '''
    if hasattr(val,'__iter__'): return [abs(aSrc-v).argmin() for v in val]
    else: return abs(aSrc-val).argmin()
