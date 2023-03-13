
import numba
import numpy as np

@numba.njit(cache=True, parallel=True)
def multithreading(a):

 for i in numba.prange(10):
  a[i] *= 10

