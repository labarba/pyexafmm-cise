<h1 align='center'> PyExaFMM CiSE </h1>

# Outline

## 0 Abstract
- Question: Can we design a HPC code all in Python? Why this is an important question to answer ...
- Answer: No, because ...
- Utility of testing hypothesis with FMM algorithm (and what they are useful for - briefly): complex heirarchical datastructure, non-trivial to apply optimisation tools. Lots of data organisation, which is limited by the interpreter.
- What this paper presents (implementation and design description - how they are influenced by our tools, convergence testing, benchmarking on different problems)

## 1 Introduction

- The point of this paper, why are we making another FMM? What is the FMM?
-  Tie together reasoning for using Python to code a non-trivial algorithm. (Ease of deployment, interoperbility with Python universe, low barrier to entry for non-software specialists)
- Particle FMM, why it's useful, and in which contexts. Relevant references for more in depth discussion in the literature. Probably easiest to just introduce it as a problem in computational electromagnetics.
- Current advances in written software for it
- Python, and it's utility.
- The concept of JIT and Numba, and how they work roughly.
- Can we code a HPC library using just Python data/numerics stack? If so it would make our lives as Computational Scientists a lot easier/faster! Allowing you to go from prototype to performance without software engineering hassle introduced by C++.
- Paper organisation in terms of following sections ...

References:
1. Numba, lam, petriou, sievert
2. FMM implementations that already exist: https://www.swmath.org/?term=FMM
3. Original Paper, Greengard + Rokhlin


## 2 KIFMM Algorithm
- Basic concept behind KIFMM (relevant operations, and algorithm structure)
- Octrees, and adaptive octree explanation as a part of this.
- Concept of balancing, and how it effects the computation of interaction lists.

Figures:
1. Illusatrate operators, and least-squares problem for M2M/L2L/M2L/P2M
2. Illustrate operators wrt to an octree (or quadtree) if it's easier to draw.
3. Illustration of interaction lists

## 3. Techniques for Achieving Performance

- Rely on effective data representations and data organisation to achieve performance. This is hard to achieve for FMM. Need to store coefficients, and custom operators for basically all nodes in memory.
Need to represent the nodes in an easily parallelisable way. Need tree operations to be fast (i.e. parent to child, finding siblings etc).

### 3.1 What is Numba?

What is it, how does it work, what is it useful for? Where is numba used in this project (AdaptOctree construction, P2M step)

### 3.2 Data Structures

- Morton representation, (linear) adaptive octree. Provide algorithms used for tree construction, balancing, and morton encoding method. Provide a benchmark of tree construction times for a few shapes, and realistic problem sizes.
- Explain how Numba is used in AdaptOctree, especially detail the difficulties faced in achieving things like: hashing, set inclusion, mutable return types (tree construction) first-class functions (effective interaction list computatoin). Explain how many Python idioms have to be set aside, and one has to think like a C programmer.
- Explain what the end result of this data representation is, and indeed has to be, for optimisation. Aligned vectors, linked by indices, that can be optimised by the compiler for fast access as well as SIMD operation. Explain how this organisation is all done as single node python code, offer benchmarks for how significant this can be.

Figures:
1. Illustration of Morton encoding

### 3.3 Precomputing Operators

- Optimisations required for practical implementations, requirement to cache and store operators, quickly lookup (precomputed) operators, avoid redundant calculation
- Concept of transfer vectors, as well as how we do this in practice. How is this complicated by Numba? How one sometimes feels limited by Numba, into programming with an invisible framework.
- Using HDF5 effectively as a cache to load required data into memory.

### 3.4 Compressing M2L

- Overview of rSVD, and how it's used here. Show how error is dominated by FMM error through experiment.

Figures:
1. rSVD illustration

### 3.5 Software Architecture

- Overview of the separation of algorithm from compute backend. Code example of the API. I envision this section to focus on a discussion about the way in which compute kernels are written for optimum performance with Numba. I.e. they have minimal lookups, and are largely just matvecs.

## 4. Performance Comparison with State of the Art
### 4.1 FMM Problem
- Accuracy, speed, and memory footprint as a function of experimental size. For different geometries. (See KIFMM Ying paper for some of the geometries that they try in that)

Figures:
- Critical graph of convergence for all three experiments.
- Need to think about the best way to present this

### 3.2 BEM Problem (?)

## 5 Conclusion
- Shows that we can code non-trivial algorithms fairly effectively in Python, but come with their own difficulties - programming to an invisible framework - and learning curve.
- Time wasted on (non-trivial) software issues to cope with/get around Python interpreter, could have been spent on optimising an already performant code.
- Bottlenecks for data organisation which are done via python where JIT compilation has no effect. Difficult to avoid without degrading software quality - specific examples