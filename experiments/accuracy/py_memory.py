import gc

from memory_profiler import memory_usage

from fmm import Fmm

p = 6

e = Fmm('test')
e.run()
del e
gc.collect()

k = 10
e = Fmm(f'{k}_{p}_r')
mem = max(memory_usage(e.run))
print(mem)
del e
gc.collect()

k = 100
e = Fmm(f'{k}_{p}_r')
mem = max(memory_usage(e.run))
print(mem)
del e
gc.collect()

k = 'full'
e = Fmm(f'{k}_{p}_r')
mem = max(memory_usage(e.run))
print(mem)
del e
gc.collect()

k = 10
e = Fmm(f'{k}_{p}_s')
mem = max(memory_usage(e.run))
print(mem)
del e
gc.collect()

k = 100
e = Fmm(f'{k}_{p}_s')
mem = max(memory_usage(e.run))
print(mem)
del e
gc.collect()

k = 'full'
e = Fmm(f'{k}_{p}_s')
mem = max(memory_usage(e.run))
print(mem)
del e
gc.collect()
