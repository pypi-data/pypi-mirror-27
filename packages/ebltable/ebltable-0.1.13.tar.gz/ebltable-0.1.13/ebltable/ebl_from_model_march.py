"""
Class to read EBL models 

History of changes:
Version 0.01
- Created 29th October 2012
Version 0.02
- 7th March: added inoue z = 0 EBL
Version 0.03
- 29th January 2017: EBL integration a la Biteau & Williams 2015, LIV effect for any order larger than 1
"""

__version__ = 0.03
__author__ = "M. Meyer // manuel.meyer@physik.uni-hamburg.de, J. Biteau // biteau@in2p3.fr"

# ---- IMPORTS -----------------------------------------------#
import numpy as np
import math
import logging
import os
from scipy.special import spence as dilog
from scipy.interpolate import interp1d
from scipy.interpolate import RectBivariateSpline as RBSpline
from scipy.integrate import simps,cumtrapz
import warnings
from numpy import linspace
from numpy import meshgrid 
from numpy import zeros
from numpy import transpose
from numpy import swapaxes 
from numpy.ma import masked_array
from numpy import dstack
from numpy import log,sqrt 
from constants import *
from os.path import join
import time
# ------------------------------------------------------------#

class EBL(object):
	"""
	Class to calculate EBL intensities from EBL models.
	
	Important: if using the predefined model files, the path to the model files has to be set through the 
	environment variable EBL_FILE_PATH

	Arguments
	---------
	z:		redshift, m-dim numpy array, given by model file
	logl:	log wavelength, n-dim numpy array, given by model file, in mu m
	nuInu:	nxm - dim array with EBL intensity in nW m^-2 sr^-1, given by model file
	model:	string, model name

	eblSpline:	rectilinear spline over nuInu

	steps_e 	int, steps for tau - integration in redshift
	steps_z 	int, steps for tau - integration in energy
	"""

	def __init__(self,file_name='None',model = 'gilmore', path='/'):
		"""
		Initiate EBL model class. 

		Parameters
		----------
		file_name:	string, full path to EBL model file, with first column with log(wavelength), 
				first row with redshift and nu I nu values otherwise. If none, model files are used
		model:		string, EBL model to use if file_name == None. Currently supported models are listed in Notes Section
		path:		string, if environment variable EBL_FILE_PATH is not set, this path will be used.

		Returns
		-------
		Nothing

		Notes
		-----
		Supported EBL models:
			Name:		Publication:
			franceschini	Franceschini et al. (2008)	http://www.astro.unipd.it/background/
			kneiske		Kneiske & Dole (2010)
			dominguez	Dominguez et al. (2011)
			inuoe		Inuoe et al. (2013)		http://www.slac.stanford.edu/~yinoue/Download.html
			gilmore		Gilmore et al. (2012)		(fiducial model)
			finke		Finke et al. (2012)		http://www.phy.ohiou.edu/~finke/EBL/
		"""
		self.z		= np.array([])		#redshift
		self.logl	= np.array([])		#log (wavelength / micron)
		self.nuInu	= np.array([])		#log (nu I_nu / [nW / Hz / sr])
		self.model	= model		#model

		ebl_file_path = os.path.join(os.path.split(__file__)[0],'data/')

		if model == 'kneiske':
			file_name = join(ebl_file_path , 'ebl_nuFnu_tanja.dat')
		elif model == 'franceschini':
			file_name = join(ebl_file_path , 'ebl_franceschini.dat')
		elif model == 'dominguez':
			file_name = join(ebl_file_path , 'ebl_dominguez11.out')
		elif model == 'dominguez-upper':
			file_name = join(ebl_file_path , 'ebl_upper_uncertainties_dominguez11.out')
		elif model == 'dominguez-lower':
			file_name = join(ebl_file_path , 'ebl_lower_uncertainties_dominguez11.out')
		elif model == 'inoue':
			file_name = join(ebl_file_path , 'EBL_z_0_baseline.dat')
			#file_name = join(ebl_file_path , 'EBL_proper_baseline.dat')
		elif model == 'inoue-low-pop3':
			file_name = join(ebl_file_path , 'EBL_z_0_low_pop3.dat')
			#file_name = join(ebl_file_path , 'EBL_proper_low_pop3.dat')
		elif model == 'inoue-up-pop3':
			file_name = join(ebl_file_path , 'EBL_z_0_up_pop3.dat')
			#file_name = join(ebl_file_path , 'EBL_proper_up_pop3.dat')
		elif model == 'gilmore':
			file_name = join(ebl_file_path , 'eblflux_fiducial.dat')
		elif model == 'gilmore-fixed':
			file_name = join(ebl_file_path , 'eblflux_fixed.dat')
		elif model == 'cuba':
			file_name = join(ebl_file_path , 'CUBA_UVB.dat')
		elif model == 'finke':
			file_name = join(ebl_file_path , 'ebl_modelC_Finke.txt')
		else:
			raise ValueError("Unknown EBL model chosen!")

		data = np.loadtxt(file_name)
		if model == 'inoue':
			self.z = np.array([0.])
			self.logl = np.log10(data[:,0])
			self.nuInu = np.log10(data[:,1])
			self.eblSpline = interp1d(self.logl,self.nuInu)
			return
		elif model == 'gilmore':
			self.z = data[0,1:]
			self.logl = np.log10(data[1:,0] * 1e-4)			# convert from Angstrom to micro meter
			self.nuInu = data[1:,1:]			
			self.nuInu[self.nuInu == 0.] = 1e-20 * np.ones(np.sum(self.nuInu == 0.))
			self.nuInu = (self.nuInu.T * data[1:,0]).T * 1e4 * 1e-7 * 1e9		# convert from ergs/s/cm^2/Ang/sr to nW/m^2/sr
			self.nuInu = np.log10(self.nuInu)
		elif model == 'cuba':
			self.z = data[0,1:-1]
			self.logl = np.log10(data[1:,0] * 1e-4)
			self.nuInu = data[1:,1:-1]
			# replace zeros by 1e-40
			idx = np.where(data[1:,1:-1] == 0.)
			self.nuInu[idx] = np.ones(np.sum(self.nuInu == 0.)) * 1e-20
			self.nuInu = np.log10(self.nuInu.transpose() * SI_c / (10.**self.logl * 1e-6)).transpose()	# in erg / cm^2 / s / sr
			self.nuInu += 6	# in nW / m^2 /  sr

			# check where logl is not strictly increasing
			idx = np.where(np.diff(self.logl) == 0.)
			for i in idx[0]:
				self.logl[i+1] = (self.logl[i + 2] + self.logl[i]) / 2.
		else:
			self.z = data[0,1:]
			self.logl = np.log10(data[1:,0])
			self.nuInu = np.log10(data[1:,1:])

		if model == 'finke': 
			self.logl = self.logl[::-1] - 4.
			self.nuInu = self.nuInu[::-1]
		else:
			data	= np.loadtxt(file_name)
			self.z	= data[0,1:]
			self.logl	= np.log10(data[1:,0])
			self.nuInu	= np.log10(data[1:,1:])
			self.eblSpline = RBSpline(self.logl,self.z,self.nuInu,kx=2,ky=2)	# reutrns log10(nuInu) for log10(lambda)

		self.steps_e		= 50	# steps for integration
		self.steps_z		= 50	# steps for integration

		return


	def optical_depth(self,z0,E_TeV,LIV_scale = 0., nLIV=1, h = h, OmegaM = OmegaM, OmegaL = OmegaL):
		"""
		calculates mean free path for gamma-ray energy E_TeV at redshift z

		Parameters
		----------
		z:	float, redshift
		E_TeV:	n-dim array, gamma ray energy in TeV
		LIV:	float, Lorentz invariance violation parameter (quantum gravity scale), 
			assumed for linear violation of disp. relation and only photons affected (see Jacob & Piran 2008)

		Returns
		-------
		(N dim)-np.array with corresponding mean free path values in Mpc

		Notes
		-----
		See Dwek & Krennrich 2013 and Mirizzi & Montanino 2009
		"""
		if np.isscalar(E_TeV):
			E_TeV = np.array([E_TeV])

		z_array = linspace(0.,z0,self.steps_z)
		result	= zeros((self.steps_z,E_TeV.shape[0]))

		for i,z in enumerate(z_array):
			
			result[i] = 1. / self.mean_free_path(z,E_TeV,LIV_scale,nLIV) 
			result[i] *= 1. / Mpc2cm	# this is in cm^-1
			result[i] *=1./ ( (1. + z ) * math.sqrt((1.+ z)**3. * OmegaM + OmegaL) )	# dt / dz for a flat universe
			#result[i] *=1./ ( (1. + z ) * math.sqrt((1.+ z)**3. ) )	# dt / dz for a flat universe

		result = simps(result,z_array, axis = 0)
	#	result = cumtrapz(result,z_array, axis = 0)

		print H0, 'old'
		print 1e9 * yr2sec * CGS_c /  H0, 'old'
		

		return  result * 1e9 * yr2sec * CGS_c /  H0


	def mean_free_path(self,z,E_TeV,LIV_scale = 0., nLIV=1, electrons_and_photons_LIV=True):
		"""
		calculates mean free path for gamma-ray energy E_TeV at redshift z

		Parameters
		----------
		z:	float, redshift
		E_TeV:	n-dim array, gamma ray energy in TeV
		LIV_scale:	float, quantum gravity scale normalized to the Planck energy (see Jacob & Piran 2008)
		nLIV:	int, order of the LIV effect (n=1 -> linear modification of the dispersion relation)
		electrons_and_photons_LIV: boolean, if false, only the photons are affected by LIV

		Returns
		-------
		(N dim)-np.array with corresponding mean free path values in Mpc

		Notes
		-----
		See Biteau & Williams 2015
		"""
		if np.isscalar(E_TeV):
			E_TeV = np.array([E_TeV])

		e_max		= SI_h * SI_c / 10.**np.min(self.logl) * 1e6 / SI_e	# max energy of EBL template in eV

		#defines the effective energy scale for the LIV modification
		ELIV_eV = 4.*M_E_EV * M_E_EV* (LIV_scale * E_PLANCK_EV)**nLIV
		if electrons_and_photons_LIV:
			ELIV_eV/=1.-2.**(-nLIV)
		ELIV_eV = ELIV_eV**(1./(2.+nLIV))

		result = zeros(E_TeV.shape[0])
		for i,ETeV in enumerate(E_TeV):
			EeV_at_z = ETeV*1e12 * (1. + z)
			ethr = M_E_EV * M_E_EV / EeV_at_z
			if LIV_scale:
				ethr	*= 1.+ (EeV_at_z/ELIV_eV)**(nLIV+2.)
			if(ethr<e_max):
				e_array	= 10.**np.linspace(np.log10(ethr),np.log10(e_max),self.steps_e)
				nP		= self.n_array(z,e_array)[0] * ethr * ethr * self.Pkernel(1.-ethr / e_array) / e_array 
				nP*= (1+z)*(1+z)*(1+z)#scale factor for the density tabulated in the models
				result[i] = simps(nP,np.log(e_array), axis = 0)
		return 1. / (result * Mpc2cm* CGS_tcs * 0.75)

	def Pkernel(self,bbmax_array):
		"""
		Returns Particle-physics kernel

		Parameters
		----------
		bbmax_array: beta**2 
			scalar or M-dim numpy array

		Returns
		-------
	  P kernel as an array

		Notes
		-----
		See Biteau & Williams 2015
		"""
		if np.isscalar(bbmax_array):
			bbmax_array = np.array([bbmax_array])

		bbmax_array[bbmax_array<0.] = 0.# set to zero all values below threshold
		bbmax_array[bbmax_array>=1.] = 0.# set to zero all values below threshold

		x = sqrt(bbmax_array)
		xx = bbmax_array
		xxx = bbmax_array*x
		xxxx = bbmax_array*bbmax_array

		ln1px = np.log(1.+x);
		ln1mx = np.log(1.-x);
		ln2 = np.log(2.);
	
		c_pi = math.pi

		res = np.zeros(bbmax_array.shape)
		for i, xval in enumerate(x):
			if xval>0.:
				res[i] += ln2*ln2 -c_pi*c_pi/6. + 2.*dilog(0.5+0.5*x[i]) #note: careful 2 conventions exist for dilog - the gsl one is used in Biteau & Williams 2015, here scipy.spence(z) = gsl_sf_dilog(1-z)!!!
				res[i]+= (ln1px[i]-2.*ln2)*ln1mx[i] + 0.5*(ln1mx[i]*ln1mx[i] - ln1px[i]*ln1px[i]);
				res[i]+= (0.5*(ln1px[i]-ln1mx[i])*(1.+xxxx[i])-(x[i]+xxx[i]))/(1.-xx[i]);
		return res

	def n_array(self,z,e):
		"""
		Returns EBL photon density in [1 / cm^3 / eV] for redshift z and energy e (eV) from BSpline Interpolation

		Parameters
		----------
		z: redshift
			scalar or N-dim numpy array
		e: energy in eV 
			scalar or M-dim numpy array

		Returns
		-------
		(N x M)-np.array with corresponding photon density values

		Notes
		-----
		if any z < self.z (from interpolation table), self.z[0] is used and RuntimeWarning is issued.
		"""
		if np.isscalar(e):
			e = np.array([e])
		if np.isscalar(z):
			z = np.array([z])

		# convert energy in eV to wavelength in micron
		l	=  SI_h * SI_c / e / SI_e  * 1e6	
		# convert energy in J
		e_J	= e * SI_e

		n = self.ebl_array(z,l)
		# convert nuInu to photon density in 1 / J / m^3
		n = 4.*PI / SI_c / e_J**2. * n  * 1e-9
		# convert photon density in 1 / eV / cm^3 and return
		return n * SI_e * 1e-6

	def ebl_array(self,z,l):
		"""
		Returns EBL intensity in nuInu [W / m^2 / sr] for redshift z and wavelegth l (micron) from BSpline Interpolation

		Parameters
		----------
		z: redshift
			scalar or N-dim numpy array
		l: wavelength
			scalar or M-dim numpy array

		Returns
		-------
		(N x M)-np.array with corresponding (nu I nu) values

		Notes
		-----
		if any z < self.z (from interpolation table), self.z[0] is used and RuntimeWarning is issued.

		"""
		if np.isscalar(l):
			l = np.array([l])
		if np.isscalar(z):
			z = np.array([z])

		if self.model == 'inoue':
			logging.warning("Inoue model is only provided for z = 0!")
			return np.array([10.**self.eblSpline(np.log10(l))])

		if np.any(z < self.z[0]): 
			warnings.warn("Warning: a z value is below interpolation range, zmin = {0}".format(self.z[0]), RuntimeWarning)

		result	= np.zeros((z.shape[0],l.shape[0]))
		tt	= np.zeros((z.shape[0],l.shape[0]))

		args_z = np.argsort(z)
		args_l = np.argsort(l)

		tt[args_z,:]		= self.eblSpline(np.log10(np.sort(l)),np.sort(z)).transpose()	# Spline interpolation requires sorted lists
		result[:,args_l]	= tt

		return 10.**result

	def ebl_int(self,z,lmin = 10.**-0.7,lmax=10.**3.,steps = 50):
		"""
		Returns integrated EBL intensity in I [nW / m^2 / sr] for redshift z between wavelegth lmin and lmax (micron) 

		Parameters
		----------
		z: redshift
			scalar 
		lmin: wavelength
			scalar
		lmax: wavelength
			scalar
		steps: number of steps for simps integration
			integer

		Returns
		-------
		Scalar with corresponding I values

		Notes
		-----
		if z < self.z (from interpolation table), self.z[0] is used and RuntimeWarning is issued.
		"""
		steps = 50
		logl = np.linspace(np.log10(lmin),np.log10(lmax),steps)
		lnl  = np.log(np.linspace(lmin,lmax,steps))
		ln_Il = np.log(10.) * (self.ebl_array(z,10.**logl)[0]) 	# note: nuInu = lambda I lambda
		result = simps(ln_Il,lnl)
		return result

	def clear(self):
		self.z = np.array([])
		self.logl= np.array([])
		self.nuInu= np.array([])
		self.model = 'None'
		self.eblSpline = None
