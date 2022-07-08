


def get_location(name):
    '''
    Argument:
        name (str): name of the location    
    
    Returns:
        lat (float): latitude of the location
        log (float): longitude of the location
    '''

    if name=='Newman':
        lat=-23.35
        log=119.75
    elif name=='Sydney':
        lat=-33.86
        log=151.22
    elif name=='Tom Price':
        lat=-22.69
        log=117.79
    elif name=='Port Augusta':
        lat=-32.49
        log=137.77
    elif name=='Pinjarra':
        lat=-32.63
        log=115.87
    elif name=='Whyalla':
        lat=-33.04
        log=137.59
    elif name=='Gladstone':
        lat=-23.84
        log=151.25
    elif name=='Burnie':
        lat=-41.05
        log=145.91

    return lat, log    
