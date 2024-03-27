# DFTB+ infrequent metadynamics of Retinal

This project contains the code and some of the generated data for infrequent metadynamics simulations (InMetaD) for trans-cis isomerization around the C13=C14 double bond in a retinal analogue called modelPSB (also called pSb5).

For details see: [Link to the paper](https://doi.org/10.1002/jcc.27332).

## Setup

Starting structures `geo_end.gen`, velocities `velocities.npy` and charges `eq2_charges.bin` in this folder are taken from a previous equilibration run in trans state.

`runx` is a template folder which will be copied for each run. It has two subdirectories. 

- `random_equilibration` : an unbiased NVT equilibration will be carried out. Here, a random amount of equilibration steps and a small random perturbation of the starting velocities is included. This is done to randomize the starting configuration and velocities in accordance with local thermal equilibrium. The script `make_equilibration_dftb.py` is used to generate DFTB+ input files.

- `production` : the InMetaD is run using an additional `plumed.dat` input file to implement the metadynamics biasing. Starting velocities are copied from the last step of the equilibration using the `take_velocities.sh` script.  The script `make_production_dftb.py` is used to generate DFTB+ input files.

## Running infrequent metadynamics runs

Each infrequent metadynamics simulation is started by the `run.sh` script. For example, to start the first simulation, use:
```bash run.sh 1```

This creates a `run1` folder in which an unbiased NVT equilibration and subsequently a production InMetaD run is carried out.

## Data Analysis

 - Extraction and calculation of transition times is done using the `extract_times.py` script.
 - Calculation of the trans-cis isomerization rate is done using the `calculate_rate.py` script.

## Command History

A history of the commands used is given in the `history.txt` file.

## Software 

 - DFTB+ plugged with PLUMED
 - Python

## Deployment

COLVAR and xyz-trajectory files have been deleted.

