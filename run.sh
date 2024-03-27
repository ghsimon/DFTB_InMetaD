# use: `bash run.sh 1` for running run1

# This script is used to run a DFTB+ simulation. It takes a single argument which is the run number.
# If the directory for the run already exists, it will not run the simulation.
# If the directory does not exist, it will set up and run an equilibration and production run.

# Check if the directory for the run already exists
if [ -d "run$1"  ]
then
    # If the directory exists, print a message and do not run the simulation
    echo 'Directory exists!!!'
else
    # If the directory does not exist, set up and run the simulation

    # Set the number of OpenMP threads to 1
    export OMP_NUM_THREADS=1

    # Print the run number
    echo '### RUN' $1 ' ###'

    # Set up and run the equilibration
    echo '### EQUILIBRATION ###'
    # Copy the template directory to the run directory
    cp -r runx run$1
    # Copy the charges file to the equilibration directory
    cp eq2_charges.bin run$1/random_equilibration/charges.bin
    # Change to the equilibration directory
    cd run$1/random_equilibration
    # Generate the DFTB+ input file for the equilibration
    python make_equilibration_dftb.py
    # Run the equilibration
    dftb+ dftb_in.hsd
    # Change back to the run directory
    cd ..

    # Set up and run the production
    echo '### PRODUCTION ###'
    # Change to the production directory
    cd production
    # Copy the charges file from the equilibration to the production directory
    cp ../random_equilibration/charges.bin .
    # Extract the velocities from the equilibration
    bash take_velocities.sh
    # Generate the DFTB+ input file for the production
    python make_production_dftb.py
    # Run the production
    dftb+ dftb_in.hsd
    # Change back to the run directory
    cd ..

    # Change back to the parent directory
    cd ..
fi



