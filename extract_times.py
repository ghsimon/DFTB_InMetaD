'''
This script performs an analysis according to the method described in https://pubs.acs.org/doi/abs/10.1021/ct500040r.

It extracts, calculates and saves the transition times from infrequent metadynamics simulation data. 

The script performs the following steps:
1. Defines the temperature and the number of metadynamics runs.
2. Initializes arrays for transition times, unscaled times, and barriers.
3. For each run, it loads the collective variable (colvar) and hills data from files.
4. Determines the first index where the dihedral angle is definitely in the cis state.
5. Finds the index of the last value on the other side of the barrier.
6. Calculates the rescaled transition times using the acceleration factor from the COLVAR file.
7. Save the unscaled and rescaled transition times to npy files

From the rescaled transition times, chemical rates can be estimated using the calculate_rate.py script
'''

import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as constants

# Define the temperature in kJ/mol and the inverse temperature
kT      = constants.k*300*constants.N_A/1000 #kJ/mol
beta    = 1/kT

# Define the amount of runs of infrequent metadynamics
runs    = 30

# Initialize arrays to store transition times, unscaled times, and barriers for each run
transition_times    = np.zeros(runs)
unscaled_times      = np.zeros(runs)
barriers            = np.zeros(runs)

# Loop over each run
for i in range(runs):
    run             = i+1
    print('### RUN %s ###/n'%run)

    # Load the collective variable (colvar) and hills data from files
    colvar          = np.loadtxt(open('run%i/production/COLVAR'%run).readlines()[:-1])
    hills           = np.loadtxt('run%i/production/HILLS'%run)

    # Plot the position of deposited Gaussians over time and save the plot
    plt.figure()
    plt.figure()
    plt.plot(hills[:,0],hills[:,1],'x')
    plt.xlabel('Time (ps)')
    plt.ylabel('Position (radians)')
    plt.title('Position of deposited Gaussians')
    plt.savefig('run%i/deposition'%run)
    plt.close()
    plt.show()

    # Find the first index where the dihedral angle is definitely in the cis state
    cis_index       = np.where((colvar[:,1]<0.2*np.pi)&(colvar[:,1]>-0.2*np.pi))[0][0]   
    print(f'cis_index = {cis_index}')

    # Find the index of the last value on the other side of the barrier
    crossing_index  = np.where((colvar[:,1][:cis_index]>0.5*np.pi) | (colvar[:,1][:cis_index]<-0.5*np.pi))[0][-1]  # index of last value on other side of barrier
    print(f'crossing_index = {crossing_index}')

    # Extract the time it took to cross the barrier from the colvar file
    crossing_time   = colvar[:,0][crossing_index-1]
    print(f'escape time = {crossing_time} ps')
    print(f'escape position = {colvar[:,1][crossing_index]}')

    # Store the unscaled transition time for this run
    unscaled_times[i]   = crossing_time

    # Store whether the dihedral crosses the barrier over positive angles (1) or negative angles (0)
    barriers[i]         = colvar[:,1][crossing_index]>0  

    # Calculate the time step
    dt              = colvar[:,0][1]-colvar[:,0][0]

    # Calculate the rescaled time in picoseconds
    rescaled_time   = dt*np.sum(np.exp(beta*colvar[:,2][:crossing_index-1])) 
    print(f'rescaled escape time = {rescaled_time} ps')
    print(f'alpha = {crossing_time/rescaled_time}')

    # Convert the rescaled time to seconds
    rescaled_time   = rescaled_time*1e-12 
    print(f'rescaled escape time = {rescaled_time:.3e} s')

    # Calculate the rate of a single transition by taking the inverse of the rescaled time
    rate            = 1/(rescaled_time) #s-1
    print(f'rate = {rate:.3e} s^-1')

    # Store the rescaled transition time for this run
    transition_times[i] = rescaled_time

# Save the unscaled transition times, rescaled transition times, and barrier crossing directions to numpy files
np.save('unscaled_times_%i_runs.npy'%runs,unscaled_times)
np.save('transition_times_%i_runs.npy'%runs,transition_times)
np.save('barriers_%i_runs.npy'%runs,barriers)

