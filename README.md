<h1 align='center'> PyExaFMM CiSE </h1>

# Outline

## 0 Abstract
- Question: Can we design a HPC code all in Python? Why this is an important question to answer ...
- Answer: No, because ...
- Utility of testing hypothesis with FMM algorithm (and what they are useful for - briefly): complex heirarchical datastructure, non-trivial to apply optimisation tools. Lots of data organisation, which is limited by the interpreter.
- What this paper presents (implementation and design description - how they are influenced by our tools, convergence testing, benchmarking on different problems)


## 1 Introduction

### 1.1 Broad Strokes

- The point of this paper, why are we making another FMM? Tie together reasoning for using Python to code a non-trivial algorithm. (Ease of deployment, interoperbility with Python universe, low barrier to entry for non-software specialists)
- Particle FMM, why it's useful, and in which contexts. Relevant references for more in depth discussion in the literature.
- Current advances in written software for it
- Python, and it's utility.
- The concept of JIT and Numba, and how they work roughly.
- Can we code a HPC library using just Python data/numerics stack? If so it would make our lives as Computational Scientists a lot easier/faster! Allowing you to go from prototype to performance without software engineering hassle introduced by C++.
- Paper organisation in terms of following sections ...

### 1.2 Designing a Performant FMM
- Basic concept behind KIFMM (relevant operations, and algorithm structure)
- Data structures required, morton representation, (linear) adaptive octree.
- Optimisations required for practical implementations, requirement to cache and store operators, quickly lookup (precomputed) operators, avoid redundant calculation (transfer vectors).
- Peculiarities of our FMM in order to achieve performance: rSVD compression of M2L, stability from ncheck_points > nequivalent_points. Why they help, and how they work - what is the impact on speed and accuracy.
- Some kind of overview of rSVD

Figures:
- FMM Tree/algorithm diagram
- Algorithm structure (table? similar to Lashuk)
- Illustration of the interaction lists in 2D
- List of definitions of interaction lists
- Maybe an illustration of rsvd?

### 1.3 Numba and CuPy
- Introduction to Numba, and how it can be useful for scientific computing - JIT compilation, interoperability with cupy/numpy data structures.
- How numba and cuda are used in this project, spell out where these technologies are actually impactful, and when they are not.
- Specifics of where they are used (AdaptOctree construction, M2L calculation/compression, P2P and P2M calculations) and benchmarks of the impact that they have over not using them.

## 2. Software Engineering

### 2.1 Software Design Principles:
- How much easier is it actually than just writing everything in C/C++?
- Was it easy to separate concerns, and enforce safety in a complex software?
- How did the library design end up looking
- How did the code end up looking? Because the utility of a full app in Python is that we can easily prototype algorithm implementations.
- Why is this important? Because these tools are only useful if they make our life easier and deployment of our ideas faster.
- How was code organised, and why. What bottlenecks did the design introduce on performance, if any (reliance on HDF5 for loading/caching operators).

### 2.2 Integration with Other Softwares (BEMPP ?)
- Using PyExaFMM to solve BEM

## 3. Performance Comparison
### 3.1 FMM Problem
- Accuracy, speed, and memory footprint as a function of experimental size. For different geometries. (See KIFMM Ying paper for some of the geometries that they try in that)
- Probably most important sections tbh...

Figures:
- Critical graph of convergence for all three experiments.
- Need to think about the best way to present this

### 3.2 BEM Problem (?)

## 4 Conclusion
- Shows that we can code non-trivial algorithms fairly effectively in Python, but come with their own difficulties - programming to an invisible framework - and learning curve.
- Time wasted on (non-trivial) software issues to cope with/get around Python interpreter, could have been spent on optimising an already performant code.
- Bottlenecks for data organisation which are done via python where JIT compilation has no effect. Difficult to avoid without degrading software quality - specific examples