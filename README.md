# MLMDPD

A Python package for automating simulations and machine learning based parametrisation in MDPD (Many-Body Dissipative Particle Dynamics) for LAMMPS.

## Features

- Automated simulation setup and execution
- Parameter generation and conversion tools
- Genetic algorithm-based parameter optimization and model selection
- Utilities for atom creation and polymer data handling

## Project Structure

```
scripts/
    run_MLMDPD.py         # Main entry point for running simulations
src/packages/
    conversion.py         # Unit and data conversion utilities
    createatoms.py        # Atom creation tools
    ga_ll_parameter_opt.py# Genetic algorithm parameter optimization
    GA_model_selection.py # Model selection using genetic algorithms
    paramgen.py           # Parameter generation
    polydata.py           # Polymer data utilities
```

## Installation

It is recommended to activate a Python virtual environment before installation:

```bash
python -m venv venv
source venv/bin/activate
```

Then install dependencies:

```bash
make install
```

## Usage

To run the main simulation script:

```bash
make run
```

After installation, you can run MLMDPD from any folder using the following command:

```bash
MLMDPD
```

Before running MLMDPD, ensure that the files `mDPDInputTable.data` and `Concentration.data` are present in your current working directory.

## Linting

Check code style with:

```bash
make lint
```

## Cleaning

Remove build artifacts and caches:

```bash
make clean
```

## Requirements

- Python 3.8+
- See `pyproject.toml` and `setup.py` for dependencies

## License

[Specify your license here]
