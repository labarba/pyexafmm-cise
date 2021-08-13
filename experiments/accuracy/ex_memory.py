import gc

import exafmm.laplace as laplace
from fmm import Fmm
from memory_profiler import memory_usage

p = 6
k = 10

e = Fmm(f'{k}_{p}_r')

sources = laplace.init_sources(e.sources, e.source_densities)
targets = laplace.init_targets(e.targets)
p = e.config['order_equivalent']
k = e.config['target_rank']
fmm = laplace.LaplaceFmm(p=p, ncrit=e.config['max_points'], filename=f'{p}_{k}.dat')

del e
gc.collect()

tree = laplace.setup(sources, targets, fmm)

def f(): laplace.evaluate(tree, fmm)

mem = max(memory_usage(f))
print(mem)


