"""
This script is used to prepare an input file for a DFTB (Density Functional Tight Binding) input file for production runs.

It reads in velocities from a file created by the take_velocities.sh script, and sets up a VelocityVerlet driver with a NoseHoover thermostat for molecular dynamics simulations. 
The thermostat is set at 300 Kelvin, and the highest vibrational frequency of the molecule is set to 0.5 THz.

The script uses a predefined number of steps for the VelocityVerlet driver (100000000 steps), and saves the state of the simulation every 100 steps.

Inputs:
- 'velocities.dat': A file containing the initial velocities of the atoms in the system, taken from the end of the equilibration run by the take_velocities.sh file.

Outputs:
- DFTB input file: A file containing the input parameters for a DFTB calculation.

Note: The paths to the input and output files, as well as the number of steps, are currently hard-coded and may need to be adjusted for different systems or conditions.
"""

import numpy as np
import argparse

steps = 100000000

velocities = open('velocities.dat','r').read()

dftb_in = '''Geometry = GenFormat {
<<< ../random_equilibration/geo_end.gen
}

Driver = VelocityVerlet{
  # Time step for MD
  TimeStep [fs] = 1
  # Use thermostat to maintain temperature

  Plumed = Yes

  Thermostat = NoseHoover {
    Temperature [Kelvin] = 300
    # Approximately the highest vibrational frequency of the molecule
    CouplingStrength [THz] = 0.5
  }
  #%i times 1 fs or a total of %.1f ps
  Steps = %i
  MovedAtoms = 1:-1
  # save every 100 steps
  MDRestartFrequency = 100
  Velocities [angstrom/ps] = { # This is the same unit as xyz format output
  %s}
}

Hamiltonian = DFTB {
  Scc = Yes
  ThirdOrderFull = Yes
  MaxSCCIterations = 5000
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
UseOMPthreads=Yes}
'''%(steps,steps/1000,steps,velocities)

f = open('dftb_in.hsd','w')
f.write(dftb_in)
f.close()
