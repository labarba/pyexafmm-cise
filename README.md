<h1 align='center'> PyExaFMM CiSE </h1>

# Outline

- I want to introduce Numba as a tool for HPC with Python for more complex algorithms. FMM is a good benchmark, with a;
    - Recursive data structure
    - Lots of linear algebra operations (SVD, MatMul etc), which Numba optimizes for.

- I want to demonstrate that it's ok, but not great
    - software design is constrained.
    - costs associated with passing back and forth between machine code, and python interpreter born out in slow runtimes.
    - protyping for performance is not easy, and advanced knowledge is required to debug performance.

I want to explain:
- Software decisions I made:
    - Linear representation of tree. Why is this better than a custom Node class?
        - Simplest representation of a tree possible, and is compatible with Numba or CPython libraries
        - designing for separability, want to be able to use library in non-numba contexts
        - algebraically defined tree-node attributes are very fast to compute (offer benchmark) and are orders of magnitude smaller in impact than the runtime.
        - But, traversal requires a lookup table linking the key and the index in the array representation.

- Software optimizations I used:
    - Data Driven Design
        - The separation of computational loops into a backend module to allow easy Numba decoration.
        - Minimal use of Python object model.
    - Caching of repeatedly used data in a HDF5 database, loaded into RAM at runtime
    - Design of functions to use only:
        - optimized Numba implementations (linear algebra)
        - simple arithmetic/bitwise operations
            - These kind of functions are most efficiently translated by Numba.
        - Or, compositions of simpler functions that have been njit'd using the above strategy.

- Parallel strategies for Numba performance:
    - I designed data structures for cache-coherence
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
    - matmul is optimized already with BLAS.

- My points:
    - Proved by the way I had to design it:
        - Designed around simple data structures.
        - Numba constrains design to a small subset of Python, has its own learning curve
            - e.g. designing 'hashing' function that uses simple instructions.
        - It's not possible to naively drop in, a lot of careful optimizations are needed to achieve peak performance with Numba.
            - Hot loops have to be separated from business logic of app
            - Have to ensure that methods use simple instructions, manually. Going out of your way to avoid 'pythonic' (object oriented) code.
            - Debugging performance issues requires advanced knowledge - flying in the face of being 'drop-in' tool for naive use by domain specialist
                - e.g. oversubscription issues, and choice of threading layers

    - Proved by difference in operator application times:
        - There are costs to passing into nopython mode from python
            - Argument parsing cost, computation/number of calls into nopython mode has to be considered.
            - Allocating memory with numpy is handled differently in the numba runtime, than when allocating within no-python mode. Requires the creation of an additional struct to handle reference to python object. As well as routines to ensure that writing back in original buffer is threadsafe.
            - There are checks by the Numba dispatcher to
                - Find the correct function handle for argument type.
            - Compiled machine code is more complex than direct C++/Fortran code
                - instructions to handle python/NRT interface
                - error handling for incompatible operations
                    - for example the inability to convert into primitive types.
        - I need to find good theoretical justification for this.
            - I need to understand how Numba allocs (stack vs heap) and how this can matter
                - Numba allocs using NRT (Numba Run Time) - a C library using wrappers around malloc/free etc.
                - interfaces to Python, to allow conversion between python obj and NRT meminfo object via a reference.
                - Numba has to unbox/box primitives.
                - Python and Numba both alloc always on heap
            - I need to understand impact of Python's alloc/C function calls
                - I don't use python functions in Numba routines, I hand control to NRT. The NRT converts Py objects to something it can handle, and loads data via a reference to the underlying pyobject.
    - Proved by LOC
        - Relative simplicity of PyExaFMM
            - but you still need to understand Numba in detail to retain efficiency, which is against what we are attempting to show tbh.
    - Proved by Benchmarks
        - Can achieve comparable accuracy for slower runtime cost.
        - Memory usage is comparable, which is expected.
        - Numba is very useful, with a lot of functionality, but the interface it exposes to pass between compiled machine code and Python runtime, is not efficient enough for all HPC applications.

Benchmarks:
    - Tree construction
    - Operator precomputation
    - Morton operations (need to show that algebraic operations are very fast to compute)

Figures:

- Operator application times for both softwares on benchmark problem
    - bar-chart like lashuk paper
    - Shows where Python is shitty

- Table with different parameter settings including memory/accuracy information alongside runtimes.
    - Shows that it works

- Keep the KIFMM operator figures

- Re-add the loop figure
    - Cut down words introducing FMM


# Notes

Numba's initial focus is to target a Python subset that makes heavy use of ndarrays and numeric scalars in loops so that users no longer need to rewrite their Python code in a low level language for better performance (over those loops).

> The key word is 'better' not 'best'

The basic structure of arrays
    - data pointer to the base of the memory buffer
    - two integer arrays describing the dimensionality (shape), and strides between elements along each dimension.

Numba is aware of the structure of arrays, can access these fields directly for calculating the offset of an element given an index value. Can generate efficient loops that index into ndarrays with performance similar to equivalent code written in a compiled language.

> Bypasses unnecessary indirection for indexing values from Numpy arrays.

Numba lets LLVM optimize loops for vectorization.

> This can fail, for example if a loop is over an array without a contiguous layout - therefore won't be sped up with vectorization applied.

Numba does not replace the interpreter, unlike many other JIT compilers, requires the user to declare JIT'ble using a decorator.

> UI benefits: No explicit type annotation, Numba inspects arg types for creating signature when function is first called.

Polymorphism is resolved at compile time.

Numba is more opportunistic and opinionated than PyPy or Pyston (Other JIT compilers)

> Opportunistic - focus on narrow subset of Python use-cases (hot numeric loops, simple GPU and multithreading support)

> Opinionated - Promotes array oriented programming via NumPy arrays.

If Numba fails to infer types, and compiles in 'object mode' and thus relying on the Python runtime, the generated code is equivalent to 'unrolling' the interpreter loop; and thus removing the interpreter overhead.

When calling a function during CPython execution, interpreter creates a new frame for the function and executes the function bytecode. The bytecode is an instruction stream - similar to x86 assembly. Branches are encoded as absolute/relative jump instructions. Some bytecode instructions perform multiple tasks.

> JUMP_IF_TRUE_OR_POP - jumps to target address if the value on the top of stack evaluates to true, otherwise pops the TOS

> FOR_ITER - encodes the for-loop construct, asks for the next value of the iterator at the TOS. If the iterator is exhausted, it pops the stack and jumps to the end of the loop. Otherwise the next value of the iterator is pushed up the stack.

Both of these instructions change the control flow of the program, and have optional stack-effects.

Can't be mapped directly to a low-level representation used by LLVM IR.

Numba passes this Python bytecode through several layers of analysis, before translation.

> Numba converts array expressions into loops to avoid allocating temporary arrays for intermediate results.

In the lowering to LLVM stage we have type information for all values in the Numba IR. For each Python function, two functions are emitted in LLVM:

- One for the actual compiled function
- A wrapper that acts as a bridge between the interpreted Python runtime and the compiled Numba runtime. The wrapper unboxes Python objects into machine representations (handled by the NRT) for use as arguments within the compiled function - therefore we pay the arg parsing cost within this wrapper function. The returned values from the compiled function is boxed back into a PyObject from the machine representation when returned to the Python interpreter.