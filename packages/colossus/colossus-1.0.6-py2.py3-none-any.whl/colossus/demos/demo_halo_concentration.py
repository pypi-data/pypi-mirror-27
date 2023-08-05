###################################################################################################
#
# demo_halo_concentration.py (c) Benedikt Diemer
#     				    	     benedikt.diemer@cfa.harvard.edu
#
###################################################################################################

"""
Sample code demonstrating the usage of the halo.concentration module.
"""

###################################################################################################

import numpy as np

from colossus.utils import utilities
from colossus.cosmology import cosmology
from colossus.halo import concentration
from colossus.halo import profile_nfw

###################################################################################################

def main():
	
	demoConcentration()
	#demoConcentrationTable('WMAP9')

	return

###################################################################################################

def demoConcentration():
	"""
	A small demonstration of the concentration model: output the concentrations in the virial and 
	200c mass definitions, for three halo masses, in the WMAP9 cosmology.
	"""
	
	M = np.array([1E9, 1E12, 1E15])

	print("First, set a cosmology")
	cosmo = cosmology.setCosmology('WMAP9')
	print(("cosmology is %s" % cosmo.name))
	
	utilities.printLine()
	print("Now compute concentrations for M200c:")
	c = concentration.modelDiemer15fromM(M, 0.0, statistic = 'median')
	for i in range(len(M)):
		print(("M200c = %.2e, c200c = %5.2f" % (M[i], c[i])))

	utilities.printLine()
	print("Now compute concentrations for another mass definition, Mvir:")
	c = concentration.concentration(M, 'vir', 0.0, model = 'diemer15', statistic = 'median')
	for i in range(len(M)):
		print(("Mvir = %.2e, cvir = %5.2f" % (M[i], c[i])))

	utilities.printLine()
	print("We note that the prediction for mass definitions other than c200c is not as accurate")
	print("due to differences between the real density profiles and the NFW approximation that")
	print("is used for the conversion. See Appendix C of Diemer & Kravtsov 2015 for details.")
	
	return

###################################################################################################

def demoConcentrationTable(cosmo_name):
	"""
	Create a file with a table of concentrations according to the Diemer & Kravtsov 2015 model for 
	a range of redshifts, halo masses, and mass definitions.	
	"""
	
	cosmo = cosmology.setCosmology(cosmo_name)
	mdefs = ['2500c', '500c', 'vir', '200m']
	nu_min = 0.3
	nu_max = 5.5
	n_M_bins = 100
	z = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 3.0, 4.0, 6.0, 8.0, 10.0, 15.0, 20.0, 30.0]

	# Write file header
	f = open('cM_%s.txt' % (cosmo_name), 'w')
	line = '# This file contains concentrations according to the model of Diemer & Kravtsov 2015. \
		The model natively predicts the mean and median c200c. For all other mass definitions,\n'
	f.write(line)
	line = '# the halo mass and concentrations are converted using either the mean or median c200c.\n'
	f.write(line)
	line = '#\n'
	f.write(line)
	line = '# cosmology: ' + str(cosmology.cosmologies[cosmo_name]) + '\n'
	f.write(line)
	line = '#\n'
	f.write(line)
	line = '#   z     nu     M200c  c200c  c200c'
	for k in range(len(mdefs)):
		for dummy in range(2):
			n_spaces = 9 - len(mdefs[k])
			for dummy in range(n_spaces):
				line += ' '
			line += 'M%s' % (mdefs[k])
			n_spaces = 6 - len(mdefs[k])
			for dummy in range(n_spaces):
				line += ' '
			line += 'c%s' % (mdefs[k])
	line += '\n'
	f.write(line)
	line = '#                      median   mean'
	for dummy in range(len(mdefs)):
		line += '    median median      mean   mean'
	line += '\n'
	f.write(line)
	
	# Write block for each redshift
	for i in range(len(z)):

		print('z = %.2f' % z[i])

		if z[i] > 5.0:
			nu_min = 1.0
			
		log_M_min = np.log10(cosmo.massFromPeakHeight(nu_min, z[i]))
		log_M_max = np.log10(cosmo.massFromPeakHeight(nu_max, z[i]))
		bin_width_logM = (log_M_max - log_M_min) / float(n_M_bins - 1)
		
		M200c = 10**np.arange(log_M_min, log_M_max + bin_width_logM, bin_width_logM)
		M200c = M200c[:n_M_bins]	
		nu200c = cosmo.peakHeight(M200c, z[i])
		c200c_median = concentration.modelDiemer15fromNu(nu200c, z[i], statistic = 'median')
		c200c_mean = concentration.modelDiemer15fromNu(nu200c, z[i], statistic = 'mean')
			
		for j in range(len(M200c)):
			line = '%5.2f  %5.3f  %8.2e  %5.2f  %5.2f' % (z[i], nu200c[j], M200c[j], c200c_median[j], c200c_mean[j])
			prof_median = profile_nfw.NFWProfile(M = M200c[j], c = c200c_median[j], z = z[i], mdef = '200c')
			prof_mean = profile_nfw.NFWProfile(M = M200c[j], c = c200c_mean[j], z = z[i], mdef = '200c')			
			for k in range(len(mdefs)):
				R_delta_median, M_delta_median = prof_median.RMDelta(z[i], mdefs[k])
				R_delta_mean, M_delta_mean = prof_mean.RMDelta(z[i], mdefs[k])
				c_delta_median = R_delta_median / prof_median.par['rs']
				c_delta_mean = R_delta_mean / prof_mean.par['rs']
				line += '  %8.2e  %5.2f  %8.2e  %5.2f' % (M_delta_median, c_delta_median, M_delta_mean, c_delta_mean)
			line += '\n'
			f.write(line)
			
	f.close()
	
	return

###################################################################################################

def _outputAllTables():
	
	cosmos = ['bolshoi', 'millennium', 'planck15', 'planck15-only', 'planck13', 'planck13-only',
			'WMAP9', 'WMAP9-ML', 'WMAP9-only', 'WMAP7', 'WMAP7-ML', 'WMAP7-only',
			'WMAP5', 'WMAP5-ML', 'WMAP5-only']
	for c in cosmos:
		demoConcentrationTable(c)

	return

###################################################################################################
# Trigger
###################################################################################################

if __name__ == "__main__":
	main()
