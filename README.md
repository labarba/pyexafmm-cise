<h1 align='center'> PyExaFMM CiSE </h1>

# Outline

- I want to introduce Numba as a tool for HPC with Python for algorithms with complex structures.

I want to explain

- Software optimizations I used:
    - Design, specifically the separation of computational loops into a backend module
    - caching of repeatedly used data in a HDF5 database, loaded into RAM at runtime

- Parallel strategies for Numba performance
    - I needed good datastructures for cache-coherence
        - For P2M and Near Field operators
        - aligned vectors for expansions coefficients as well as target results.
    - I needed methods that Numba could translate into fast machine code to be run on each thread
        - I'm talking about the M2L calculation specifically, and the hash calculation method
        - The tree represented linearly in an array
            - Tree traversal was then bitwise operations or index lookups
    - I relied on different strategies when I couldn't apriori allocate enough memory for results
        - Specifically the W list calculations
    - The strategies themselves:
        - Pre-allocating space for rapidly passing kernel over source/target pairs and storing result
            - I did this for the P2P calulcations and the P2P (u list, and node) as well as L2T
            - Pre-allocating space requires allocating enough for entire possible interaction list, as can't apriori know how big this will be.
            - P2M does a version of this, but slightly differently in that pre-allocation doesn't need to alloc to the max size of an interaction list as we know how many sources there are in a given leaf.
        - Just running prange over leaves/keys (S2L and M2T)
            - creating surfaces as needed, no cache-optizations
                - X list too small to be worth it
                - W list too large to be worth it
            - M2L a version of this too, but no surface creation

- Maths optimizations
    - rSVD of M2L, but this is specific to the FMM
    - matmul is fast in Python. compression allows for faster matmul.

- My points:
    - Proved by the way I had to design it:
        - How Numba constrains design to a small subset of Python, has its own learning curve
        - It's not possible to naively drop in, a lot of careful optimizations are needed to achieve peak performance with Numba. This is unfortunate as compiled languages often give good performance without much tweaking.
    - Proved by difference in operator application times:
        - The insurmountable interpretation barrier is expensive when performance really counts
        - I need to find good theoretical justification for this, and re-inforce with an appropriate experiment.
    - Proved by LOC
        - Relative simplicity of PyExaFMM
            - but you still need to understand Numba in detail to retain efficiency, which is against what we are attempting to show tbh.
