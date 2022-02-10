import numba
import numpy as np

@numba.njit(cache=True)
def loop_fusion(a):

 for i in range(10):
  a[i] += 1

 for i in range(10):
  a[i] *= 5
