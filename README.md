<h1 align='center'> PyExaFMM CiSE </h1>

# Setup Environment

Install latest PyExaFMM in a Conda envirionment from source

```bash
# Clone
git clone git@github.com:exafmm/pyexafmm.git
cd pyexafmm

# Build
conda build conda.recipe

# Install
conda install --use-local pyexafmm

# Editable mode for live development
python setup.py develop
```

Appropriate environment variables for PyExaFMM's multithreading implementations can be found in the `.env` file, and activated with.

```bash
source .env
```

# Re-running experiments

All experiments are self contained, and include JSON specifications for re-generating the FMM data structures for a given experiment using PyExaFMM's CLI.

e.g. for a test parametrized with a file named `test.json`

```bash
fmm generate-test-data -c test && fmm compute-operators -c test
```

# Compile manuscript

Requires latex.

```bash
cd article && sh compile.sh
```