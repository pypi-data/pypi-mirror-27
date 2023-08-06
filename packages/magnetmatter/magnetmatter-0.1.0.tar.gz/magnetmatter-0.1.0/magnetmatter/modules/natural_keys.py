import re
def natural_keys(text):
    """ returns a list of chars and digits

    HOW  TO USE:
        alist.sort(key=natural_keys)
            OR:
        alist = sorted(alist, key = natural_keys)
    """
    atoi = lambda c: int(c) if c.isdigit() else c
    return [ atoi(c) for c in re.split('(\d+)', text) ]
