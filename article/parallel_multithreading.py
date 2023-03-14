import numba
import numpy as np

@numba.njit(cache=True, parallel=True)
def multithreading(A):
    # Numpy is configured to run single
    # threaded to avoid thread 
    # oversubscription from the interaction 
    # between Numba and Numpy threads.
    for _ in numba.prange(10):
         B = A @ A