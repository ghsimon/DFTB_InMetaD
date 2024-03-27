'''
starting positions and velocities taken from set8 from normal metadynamics,
length of equilibration made random between min_steps and max_steps
'''
'''
This script is used for generating DFTB+ input files for equilibrating a system for DFTB (Density Functional Tight Binding) calculations. 

It starts with positions and velocities taken from normal metadynamics. The length of equilibration is randomized between a minimum and maximum number of steps (min_steps and max_steps).

The script also introduces randomness to the velocities by adding a random number, scaled by a factor (random_velocity_scaling), to the original velocities. The random velocities are then saved to a file.

The script prepares a DFTB input file with a VelocityVerlet driver and a NoseHoover thermostat set at 300 Kelvin.

Inputs:
- '../../velocities.npy': A numpy file containing the initial velocities of the atoms in the system.

Outputs:
- 'random_velocities.dat': A file containing the randomized velocities of the atoms in the system.
- DFTB input file: A file containing the input parameters for a DFTB calculation.

Note: The paths to the input and output files, as well as the min_steps, max_steps, and random_velocity_scaling parameters, are currently hard-coded and may need to be adjusted for different systems or conditions.
'''

import numpy as np
import argparse
import random

min_steps = 10000
max_steps = 100000

random_velocity_scaling = 2

velocities        = np.load('../../velocities.npy')
random_velocities = velocities + np.random.randn(velocities.shape[0],velocities.shape[1])*random_velocity_scaling
np.savetxt('random_velocities.dat',random_velocities,delimiter=' ',fmt='%.6f')

random_velocities_string = open('random_velocities.dat','r').read()


dftb_in = '''Geometry = GenFormat {
<<< ../../geo_end.gen
}

Driver = VelocityVerlet{
  # Time step for MD
  TimeStep [fs] = 1
  # Use thermostat to maintain temperature

  Thermostat = NoseHoover {
    Temperature [Kelvin] = 300
    # Approximately the highest vibrational frequency of the molecule
    CouplingStrength [THz] = 0.5
  }
  #random amount of steps times 1 fs
  Steps = %i
  MovedAtoms = 1:-1
  # save every 100 steps
  MDRestartFrequency = 100
  Velocities [angstrom/ps] = { # This is the same unit as xyz format output
 %s
 }
}

Hamiltonian = DFTB {
  Scc = Yes
  ThirdOrderFull = Yes
  MaxSCCIterations = 500
  SlaterKosterFiles = Type2FileNames {
  Prefix = "/home/sghysbrecht/DFTB+/recipes/slakos/3ob-3-1/"
  Separator = "-"
  Suffix = ".skf"
  }
  HubbardDerivs {
  N =   -0.1535
  H =   -0.1857
  C =   -0.1492
  }
  HCorrection = Damping {
  Exponent = 4.05
  }
  MaxAngularMomentum {
    N = "p"
    C = "p"
    H = "s"
  }
  Charge = 1
  ReadInitialCharges = Yes
}

Options {}

Analysis {
  WriteBandOut = No
}

ParserOptions {
  ParserVersion = 7
}

Parallel{
UseOMPthreads=Yes
}
'''%(random.randint(min_steps,max_steps),random_velocities_string)

f = open('dftb_in.hsd','w')
f.write(dftb_in)
f.close()
