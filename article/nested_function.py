import numpy as np
import numba
import numba.core
import numba.typed

# Initialize in Python interpreter
data = numba.typed.Dict.empty(
    key_type=numba.core.types.unicode_type,
    value_type=numba.core.types.float64[:]
)

data['initial'] = np.ones(100)

# Subroutine 1
@numba.njit
def step_1(data):
    # An example allocation & calculation
    a = np.random.rand(100, 100)
    a @ a
    data['step_1'] = data['initial']

# Subroutine 2
@numba.njit
def step_2(data):
    # An example allocation & calculation
    a = np.random.rand(100, 100)
    a @ a
    data['step_2'] =  data['step_1']

@numba.njit
def algorithm1(data):
    # Pays the un(boxing) cost to exchange
    # data with interpreter
    step_1(data)
    step_2(data)

@numba.njit
def algorithm2():
    # only pays the boxing cost to return a
    # Python type.
    data = dict()
    data['initial'] = np.ones(100)
    step_1(data)
    step_2(data)
    return data

@numba.njit
def algorithm3():
    # Numba interprets subroutines as a
    # part of a **single** function body.

    data = dict()
    data['initial'] = np.ones(100)

    def step_1(data):
        a = np.random.rand(100, 100)
        a @ a
        data['step_1'] = data['initial']

    def step_2(data):
        a = np.random.rand(100, 100)
        a @ a
        data['step_2'] =  data['step_1']

    step_1(data)
    step_2(data)
    return data