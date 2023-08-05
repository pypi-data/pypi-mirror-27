import numpy 

def catch_length(x):
    """Return x if len(x) > 1, raise error else."""
    if len(x) < 2:
        raise ValueError("Array must contains at least two elements, got {}".format(x))
    return x

def catch_array(x):
    """Return x if x is list or array, else raise error """
    if isinstance(x,numpy.ndarray):
        return catch_length(x)
    elif isinstance(x,list):
        return numpy.array(catch_length(x))
    else:
        raise ValueError("Input must be a list or an array, got {}".format(x))
        
        