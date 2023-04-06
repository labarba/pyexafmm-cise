import numpy as np
import numba
import numba.core
import numba.typed

# Initialize in Python interpreter
data = numba.typed.Dict.empty(
    key_type=numba.core.types.unicode_type,
    value_type=numba.core.types.float64[:]
)


data['initial'] = np.ones(N)

@numba.njit
def step_1(data):
    a = np.random.rand(N, N)
    data['a'] = (a @ a)[0,:]

@numba.njit
def step_2(data):
    b = np.random.rand(N, N)
    data['b'] = (b @ b)[0,:]

@numba.njit
def algorithm1(data):
    step_1(data)
    step_2(data)

@numba.njit
def algorithm2():
    data = dict()
    data['initial'] = np.ones(N)
    step_1(data)
    step_2(data)
    return data

@numba.njit
def algorithm3():
    data = dict()
    data['initial'] = np.ones(N)

    def step_1(data):
        a = np.random.rand(N, N)
        data['a'] = (a @ a)[0,:]

    def step_2(data):
        b = np.random.rand(N, N)
        data['b'] = (b @ b)[0,:]

    step_1(data)
    step_2(data)
    return data
