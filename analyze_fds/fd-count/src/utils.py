import numpy as np

def padarray(A, size, *, value=0):
    '''
    Pads an array `A` to `size` with `value`
    '''
    t = size - len(A)
    return np.pad(A, pad_width=(0, t), mode='constant', value=value)