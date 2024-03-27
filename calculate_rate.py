'''
This script performs an analysis according to the method described in https://pubs.acs.org/doi/abs/10.1021/ct500040r.

It calculates the rate of a chemical reaction using infrequent metadynamics simulation data. 

The script performs the following steps:
1. Defines the temperature and the number of metadynamics runs.
2. Loads the unscaled and scaled transition times for all runs from numpy files created by extract_times.py.
3. Calculates the mean, standard deviation, and median of the transition times.
4. Determines the empirical cumulative distribution function (ECDF) of the transition times.
5. Fits the ECDF with the theoretical cumulative distribution function (TCDF).
6. Prints the ratio of mean to standard deviation, the ratio of median to the product of mean and natural logarithm of 2, and the mean in scientific notation.
7. Perform Kolmogorov-Smirnov test and print corresponding p-value
'''

import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as constants

kT                  = constants.k*300*constants.N_A/1000 #kJ/mol
beta                = 1/kT

# Define the amount of runs of infrequent metadynamics
runs                = 30 # Amount of runs of infrequent metadynamics

# Load transition times
unscaled_times      = np.load('unscaled_times_%i_runs.npy'%runs)
transition_times    = np.load('transition_times_%i_runs.npy'%runs)

# Calculate mu, sigma and tm (Salvalaglio2014)
mu                  = np.mean(transition_times)
sigma               = np.std(transition_times)
median              = np.median(transition_times)

# Determine the empirical cumulative distribution function 
times_sorted        = np.sort(transition_times) # sort the data:
ECDF                = 1. * np.arange(len(times_sorted)) / (len(times_sorted) - 1) # calculate the proportional values of samples

# Fit with the theoretical cumulative distribution function
def func(t, tau):
    """
    Model the theoretical cumulative distribution function according to a first-order Poisson distribution.

    Parameters:
    t (float): The transition time value.
    tau (float): The average transtion time.

    Returns:
    float: The calculated probability value according to the theoretical cumulative distribution function.
    """
    return 1 - np.exp(-t / tau)

from scipy.optimize import curve_fit
tau, pcov = curve_fit(func, times_sorted, ECDF, p0=mu)
tau = tau[0]

print(f'mu/sigma = {mu/sigma}')
print(f'tm/(muln2) = {median/(mu*np.log(2))}')
print(f'mu = {mu:.3e} s')
print(f'tau = {tau:.3e} s')
print(f'k_escape = {1/tau:.3e} s-1')

# Sample new variables from theoretical probability distribution, see https://en.wikipedia.org/wiki/Inverse_transform_sampling 
y                   = np.random.rand(int(1e6))
theoretical_samples = -tau*np.log(1-y) #inverse function of TCDF

# rebuild TCDF from newly sampled variables
theoretical_sorted  = np.sort(theoretical_samples)
TCDF                = 1. * np.arange(len(theoretical_sorted)) / (len(theoretical_sorted) - 1)

# plot distributions against eachother 
plt.plot(theoretical_sorted,func(theoretical_sorted,tau),label='TCDF fit')
#plt.plot(theoretical_sorted[::10000],TCDF[::10000],'o',label='TCDF sampled')
plt.plot(times_sorted,ECDF,'x',label='ECDF')
plt.xscale('log')
plt.ylabel('p')
plt.xlabel('time')
plt.title(f'mu = {mu:.3e} and tau = {tau:.3e} and k = {1/tau:.3e}')
plt.legend()
plt.savefig('cdf_%i_runs'%runs)
plt.close()

# Do Kolmogorov-Smirnov test 
from scipy.stats import kstest
statistic, pvalue = kstest(transition_times,theoretical_samples)
print(f'pvalue = {pvalue}')
