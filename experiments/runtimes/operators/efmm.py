# ExaFMM-T
import exafmm.laplace as laplace

# PyExaFMM
from fmm import Fmm

# Load benchmark experiment
evec = [Fmm('bench1'), Fmm('bench2'), Fmm('bench3')]

# create a list of source instances
srcs = [e.sources.copy() for e in evec]
trgs = [e.targets.copy() for e in evec]
src_densities = [e.source_densities.copy() for e in evec]

sources = [laplace.init_sources(srcs[i], src_densities[i]) for i in range(3)]

# create a list of target instances
targets = [laplace.init_targets(trgs[i]) for i in range(3)]

efmmvec = [
    laplace.LaplaceFmm(
        p=e.config['order_equivalent'], 
        ncrit=e.config['max_points'], 
        filename="test_file.dat"
    )
    for e in evec
]

# Create tree
tvec = [
    laplace.setup(sources[i], targets[i], efmmvec[i])
    for i in range(3)
]

# Evaluate and time
eresultvec = [
    laplace.evaluate(tvec[i], efmmvec[i], True)
    for i in range(3)
]