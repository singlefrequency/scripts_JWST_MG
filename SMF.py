import integration_library as IL
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

import classy
from classy import Class
from scipy.integrate import ode, odeint
import scipy.constants as SPC
import numpy as np
import matplotlib.pyplot as plt
import math
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from classy import Class
from scipy.optimize import fsolve
import math
import scipy
from tqdm import tqdm 
import sys
from numpy import diff
import matplotlib.pylab as pl
import matplotlib as mpl
from matplotlib.colors import LogNorm
from multiprocessing import Pool
import integration_library as IL
%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

import classy
from classy import Class
from scipy.integrate import ode, odeint
import scipy.constants as SPC
import numpy as np
import matplotlib.pyplot as plt
import math
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from classy import Class
from scipy.optimize import fsolve
import math
import scipy
from tqdm import tqdm 

# Defs

kvec = np.logspace(np.log10(0.00001),np.log10(1000.0),10000)
H0 = 67.66
Omegam0 = (0.02242/(H0/100)**2+0.11933/(H0/100)**2)
Omegab0 = 0.02242/(H0/100)**2
Omegar0 = 8.493e-5
c = 299792.45800000057
Tcmb = 2.72e6
h = 0.6766
c = 3.3
GN = 4.301*10**(-9)
rho = 3*H0**2*Omegam0/(8*np.pi*GN)
rhocr = 2.77536627e11
rhom = rhocr*Omegam0

K0 = [0, 0.5, 1]
beta = np.linspace(0,0.5,10)
H_arr_kmoufl = [[],[],[]]
dH_arr_kmoufl = [[],[],[]]
H_int_kmoufl = [[],[],[]]
dH_int_kmoufl = [[],[],[]]

M_kmoufl = {}


common_settings_kmoufl =  {'n_s':0.9665,
          'A_s':2.101e-9,
          'tau_reio':0.0561,
          'omega_b':0.02242,
          'omega_cdm':0.11933,
          'h':0.6766,
          'YHe':0.2425,
          'T_cmb':2.7255,
          'gauge':'newtonian', #FOR MGCLASS TO WORK, GAUGE NEEDS TO BE NEWTONIAN
          'k_pivot': 0.05,
          'mg_z_init': 10.000,
          'l_logstep': 1.025,
          'l_linstep':15,
          'P_k_max_1/Mpc':1500.0,
          'l_switch_limber':9,
          'perturb_sampling_stepsize': 0.05,
          'output':'tCl,pCl,lCl,mPk',
          'l_max_scalars': 3000,
          'lensing': 'yes',
          'z_max_pk': 99}

def Pk(a, model, par1, par2):
    common_settings = {'n_s':0.9665,
          'A_s':2.101e-9,
          'tau_reio':0.0561,
          'omega_b':0.02242,
          'omega_cdm':0.11933,
          'h':0.6766,
          'YHe':0.2425,
          'T_cmb':2.7255,
          'gauge':'newtonian', #FOR MGCLASS TO WORK, GAUGE NEEDS TO BE NEWTONIAN
          'k_pivot': 0.05,
          'mg_z_init': 10.000,
          'l_logstep': 1.025,
          'l_linstep':15,
          'P_k_max_1/Mpc':1500.0,
          'l_switch_limber':9,
          'perturb_sampling_stepsize': 0.05,
          'output':'tCl,pCl,lCl,mPk',
          'l_max_scalars': 3000,
          'lensing': 'yes',
          'z_max_pk': 99}
    common_settings['mg_ansatz'] = model
    if model == 'plk_late':
        common_settings['mg_E11'] = par1
        common_settings['mg_E22'] = par2
    elif model == 'z_flex_late':
        common_settings['mg_muz'] = par1
        common_settings['mg_gamz'] = par2
        common_settings['mg_zzn'] = par2
    elif model == 'z_xpans_late':
        common_settings['mg_T1'] = par1
        common_settings['mg_T2'] = par2
        common_settings['mg_T3'] = par1
        common_settings['mg_T4'] = par2
        common_settings['mg_zzn'] = 1
    elif model == 'GI':
        common_settings['Omega_Lambda'] = 0.0
        common_settings['w0_fld'] = par1
        common_settings['gamGI'] = par2
    elif model == 'nDGP':
        common_settings['rc'] = par1
    else:
        common_settings['beta_kmfl'] = par1
        common_settings['k0_kmfl'] = par2
        
    M = Class()
    M.set(common_settings)
    M.compute()

    Pk = []
    for k in kvec:
        Pk.append(M.pk(k,1/a-1))
    
    return Pk


def H_f(model_H,a, par1, par2):
    if model_H == 'LCDM':
        return H0*np.sqrt(1-Omegam0-Omegar0+Omegam0*a**(-3)+Omegar0*a**(-4))
    elif model_H == 'wCDM':
        par1 = wL
        return H0*np.sqrt((1-Omegam0-Omegar0)*a**(-3*(1+wL))+Omegam0*a**(-3)+Omegar0*a**(-4))
    elif model_H == 'nDGP':
        rc = par1
        Omegarc = 1/(4*H0**2*rc**2)
        OmegaLambda0 = 1 - Omegam0 - Omegar0 + 2*np.sqrt(Omegarc)
        return H0*np.sqrt(Omegam0*a**(-3)+Omegar0*a**(-4)+Omegarc + OmegaLambda0)-H0*np.sqrt(Omegarc)
    elif model_H == 'kmoufl':
        return H_int_kmoufl[i_kmoufl][j_kmoufl](a)

def dH_f(model_H,a, par1, par2):
    if model_H == 'LCDM':
        return -0.5*(H0*(3*a*Omegam0 + 4*Omegar0))/(a**5*np.sqrt((a*Omegam0 + Omegar0 - a**4*(-1 + Omegam0 + Omegar0))/a**4))
    elif model_H == 'wCDM':
        wL = par1
        return (a**(-5 - 3*wL)*(3*a*H0*(1 + wL)*(-1 + Omegam0 + Omegar0) - a**(3*wL)*H0*(3*a*Omegam0 + 4*Omegar0)))/(2*np.sqrt((Omegar0 + a*(Omegam0 - (-1 + Omegam0 + Omegar0)/a**(3*wL)))/a**4))
    elif model_H == 'nDGP':
        rc = par1
        Omegarc = 1/(4*H0**2*rc**2)
        OmegaLambda0 = 1 - Omegam0 - Omegar0 + 2*np.sqrt(Omegarc)
        return  (H0*((-3*Omegam0)/a**4 - (4*Omegar0)/a**5))/(2.*np.sqrt(OmegaLambda0 + Omegam0/a**3 + Omegar0/a**4 + Omegarc))
    elif model_H == 'kmoufl':
        return dH_int_kmoufl[i_kmoufl][j_kmoufl](a)
        
def mu(model_H, model, par1, par2, a):
    H = H_f(model_H, a, par1, par2)
    dHda = dH_f(model_H, a, par1, par2)
    dHdt = a*H*dHda
    rhom = 3*H0**2*Omegam0*a**(-3)
    rhor = 3*H0**2*Omegar0*a**(-4)
    rhoL = 3*H**2-rhom-rhor
    OmegaL = rhoL/(3*H**2)
    OmegaM = rhom/(3*H**2)
    if model == 'plk_late':
        f1 = par1*OmegaL
        return 1 + f1
    elif model =='z_flex_late':
        return 1+ par1*(1-a)**1 - par1*(1-a)**2
    elif model == 'z_xpans_late':
        return 1 + par1*OmegaL + par2*OmegaL**2
    elif model == 'GI':
        wL = par1
        gamma = par2
        return 2/3*OmegaM**(gamma-1)*(OmegaM**gamma+2-3*gamma+3*(gamma-1/2)*(OmegaM+(1+wL)*OmegaL))
    elif model == 'nDGP':
        rc = par1
        beta = 1 + 2*H/c*par1*(1+dHdt/(3*H**2))
        return 1 + 1/(3*beta)
    elif model == 'kmoufl':
        beta = par1
        K0 = par2
        A_kmfl = 1.0 + par1*a
        X_kmfl = 0.5 * A_kmfl**2*(H*a)**2/((1-Omegam0-Omegar0)*H0**2)
        k_prime_mfl = 1.0 + 2.0*par2*X_kmfl
        epsl1_kmfl = 2.0*par1**2/k_prime_mfl    
        X_kmfl_dot = 0.5 * A_kmfl**2/((1-Omegam0-Omegar0)*H0**2)*2.0*H*a*(H*H*a+dHdt*a)
        return 1.+ epsl1_kmfl

def delta_nl_ODE(a, y, model_H, model, par1, par2):
    delta,ddeltada = y
    H = H_f(model_H, a, par1, par2)
    dH = dH_f(model_H, a, par1, par2)
    dddeltada          = -(3/a+dH/H)*ddeltada + (3*Omegam0*mu(model_H, model, par1, par2, a))/(2*a**5*H**2/H0**2)*delta*(1+delta) + 4*ddeltada**2/(3*(1+delta))
    return [ddeltada, dddeltada]

def delta_l_ODE(a, y, model_H, model, par1, par2):
    delta,ddeltada = y
    H = H_f(model_H, a, par1, par2)
    dH = dH_f(model_H, a, par1, par2)
    dddeltada          = -(3/a+dH/H)*ddeltada + (3*Omegam0*mu(model_H, model, par1, par2, a))/(2*a**5*H**2/H0**2)*delta
    return [ddeltada, dddeltada]

def collapse(deltai, model_H, model, par1, par2):
    ai = 1e-5
    dt = 0.0001
    ddeltai = deltai/ai
    init = [deltai, ddeltai]
    system = ode(delta_nl_ODE)
    system.set_f_params(*[model_H, model, par1, par2])
    system.set_initial_value(init, ai)
    
    data = [0,0]
    while system.successful() and system.y[0] <= 1e7 and system.t <= 1/(1-0.5):
        data = [system.t + dt, system.integrate(system.t + dt)[0]]   
        #plt.scatter(system.t+dt, system.integrate(system.t + dt)[0], c ='tab:blue')
    data = np.array(data)
    ac = data[0]

    return ac

def interpolate_ac(ac, model_H, model, par1, par2):
    delta_i = np.logspace(-4,-1,1000)
    arr_di_ac = []
    for i in tqdm(range(len(delta_i))):
        arr_di_ac.append([delta_i[i],collapse(delta_i[i], model_H, model,par1,par2)])
    interp_di_ac = scipy.interpolate.interp1d(np.array(arr_di_ac)[:,1],np.array(arr_di_ac)[:,0],fill_value = 'extrapolate')
    return interp_di_ac(ac)

def linear(deltai_collapse, a, model_H, model, par1, par2):
    ai = 1e-5
    dt = 0.0001
    ddeltai = deltai_collapse/ai    
    init = [deltai_collapse, ddeltai]
    system = ode(delta_l_ODE)
    system.set_f_params(*[model_H, model, par1, par2])
    system.set_initial_value(init, ai)
    
    data = []
    while system.successful() and system.t <= a:
        data.append([system.t + dt, system.integrate(system.t + dt)[0]])   
    
    data = np.array(data)
    return data

def delta_c_at_ac(model_H, model, ac, par1, par2):
    return linear(interpolate_ac(ac, model_H, model, par1, par2),ac, model_H, model,par1,par2)[-1,1]


def sigma(k,Pk,R):
    yinit = np.array([0.0], dtype=np.float64)
    eps   = 1e-13  #change this for higher/lower accuracy
    h1    = 1e-12
    hmin  = 0.0
    beta_ST = 4.8
    W   = (1+(k*R)**beta_ST)**(-1)
    Pk1 = Pk*W**2*k**2/(2.0*np.pi**2)
    
    return np.sqrt(IL.odeint(yinit, k[0],k[-1], eps,
                             h1, hmin, np.log10(k), Pk1,
                             'sigma', verbose=False)[0])
def sigma_M(k,Pk,rhoM,M):
    c_ST = 3.3
    R=(3.0*M/(4.0*np.pi*rhoM*c_ST**3))**(1.0/3.0)
    return sigma(k,Pk,R)

def dSdM(k, Pk, rhoM, M):
    c_ST = 3.3
    R1=(3.0*M/(4.0*np.pi*rhoM*c_ST**3))**(1.0/3.0)
    s1=sigma(k,Pk,R1)

    M2=M*1.0001
    R2=(3.0*M2/(4.0*np.pi*rhoM*c_ST**3))**(1.0/3.0)
    s2=sigma(k,Pk,R2)

    return (s2-s1)/(M2-M)


def ST_mass_function(k, Pk, rhoM, Masses, a, model_H, model, par1, par2):
    c_ST = 3.3
    dndM = np.zeros(Masses.shape[0], dtype=np.float64)
    deltac = delta_c_at_ac(model_H, model, a, par1, par2)
    
    for i,M in enumerate(Masses):
        R   = (3.0*M/(4.0*np.pi*rhoM*c_ST**3))**(1.0/3.0)
        nu  = (deltac/sigma(k,Pk,R))**2

        dndM[i]=-(rhoM/M)*dSdM(k,Pk,rhoM,M)/sigma(k,Pk,R)
        dndM[i]*=0.3222*np.sqrt(2*nu/np.pi)*(1+1/(nu**0.3))
        dndM[i]*=np.exp(-0.5*nu)

    return dndM

def func_SFR(x,a):
    z = 1/a-1
    nu = np.exp(-4*a**2)
    alpha_SFR = -1.412+0.731*(a-1)*nu
    Delta_SFR = 3.508 + (2.608*(a-1)-0.043*z)*nu
    gamma_SFR = 0.316+(1.319*(a-1)+0.279*z)*nu
    return -np.log10(10**(alpha_SFR*x)+1)+Delta_SFR*(np.log10(1+np.exp(x)))**gamma_SFR/(1+np.exp(10**(-x)))

def epsilon(Mh, model_SFR, a):
    z = 1/a-1
    if model_SFR == 'phenomenological_regular':
        if z<10:
            epstar = 0.15 - 0.03*(z-6)
        else:
            epstar = 0.03
    elif model_SFR == 'phenomenological_extreme':
        epstar = 1
    elif model_SFR == 'Behroozi':
        nu = np.exp(-4*a**2)
        log10M1 = 11.514+(-1.793*(a-1)+(-0.251)*z)*nu
        log10eps = -1.777+(-0.006*(a-1)+(-0.000)*z)*nu-0.119*(a-1)
        log10Mstar = log10eps + log10M1 + func_SFR(np.log10(Mh)-log10M1,a)-func_SFR(0,a)
        Mstar = 10**log10Mstar
        epstar = (Mstar/Mh)/(Omegab0/Omegam0)
    elif model_SFR == 'double_power':
        Mp = 2.8*10**11
        epstarp = 0.05
        gamma_lo = 0.49
        gamma_hi = -0.61
        epstar = epstarp/((Mh/Mp)**gamma_lo+(Mh/Mp)**gamma_hi)
        epstar = epstar/(Omegab0/Omegam0)
    else:
        sys.exit("Incorrect SFR model is being used")
    return epstar

def varepsilon(Mh, model_SFR, a):
    if model_SFR == 'phenomenological_extreme' or model_SFR == 'phenomenological_regular':
        varepsilon = 1
    elif model_SFR == 'Behroozi':
        nu = np.exp(-4*a**2)
        z = 1/a-1
        log10M1 = 11.514+(-1.793*(a-1)+(-0.251)*z)*nu
        log10eps = -1.777+(-0.006*(a-1)+(-0.000)*z)*nu-0.119*(a-1)
        log10Mstar = log10eps + log10M1 + func_SFR(np.log10(Mh)-log10M1,a)-func_SFR(0,a)
        alpha_SFR = -1.412+0.731*(a-1)*nu
        Delta_SFR = 3.508 + (2.608*(a-1)-0.043*z)*nu
        gamma_SFR = 0.316+(1.319*(a-1)+0.279*z)*nu
        varepsilon = -((Mh**alpha_SFR*alpha_SFR)/(10**(log10M1*alpha_SFR) + Mh**alpha_SFR))+ (np.log(1 + Mh**(1/np.log(10))/np.e**log10M1)**(-1 + gamma_SFR)*Delta_SFR*(10**log10M1*np.exp(10**log10M1/Mh)*(np.e**log10M1 + Mh**(1/np.log(10)))*np.log(10)*np.log(1 + Mh**(1/np.log(10))/np.e**log10M1) + (1 + np.exp(10**log10M1/Mh))*Mh**(1 + 1/np.log(10))*gamma_SFR))/((1 + np.exp(10**log10M1/Mh))**2*Mh*(np.e**log10M1 + Mh**(1/np.log(10)))*np.log(10)**gamma_SFR) 
    elif model_SFR == 'double_power':
        Mp = 2.8*10**11
        epstarp = 0.05
        gamma_lo = 0.49
        gamma_hi = -0.61
        varepsilon =  -gamma_lo + ((Mh/Mp)**gamma_hi* (-gamma_hi + gamma_lo))/((Mh/Mp)**gamma_hi + (Mh/Mp)**gamma_lo)
    return varepsilon


def SMF(Mstar_var,k, Pk, rhoM, a, model_H, model,model_SFR, par1, par2):
    Mh_arr = np.logspace(6.5,17,1000)
    Mstar_arr = epsilon(Mh_arr, model_SFR, a)*Omegab0/Omegab0*Mh_arr
    SMF = varepsilon(Mh_arr*h,model_SFR,a)*ST_mass_function(k/h, np.array(Pk)*h**3, rhoM, Mh_arr*h, a, model_H, model, par1, par2)*Mh_arr*h**3
    SMF = scipy.interpolate.interp1d(Mstar_arr/h**2,SMF, fill_value="extrapolate")
    return SMF(Mstar_var)


def SMD(k, Pk, rhoM, Masses, Masses_star, a, model_H, model, par1, par2):
    eps   = 1e-13  #change this for higher/lower accuracy
    h1    = 1e-12
    hmin  = 0.0
    yinit = np.array([0.0], dtype=np.float64)
    SMD = np.zeros(Masses_star.shape[0], dtype=np.float64)

    for i in range(len(Masses_star)):
        Mass_array = np.logspace(np.log10(Masses_star[i]), 18,100)
        integrand = ST_mass_function(k, Pk, rhoM, Mass_array, a, model_H, model, par1, par2)*Mass_array
        SMD[i] = Masses_star[i]/Masses[i]*IL.odeint(yinit, Mass_array[0],Mass_array[-1], eps,
                             h1, hmin, np.log10(Mass_array), integrand,
                             'log', verbose=False)[0]
    return SMD


def Mh_EPS(z, k, Pk, rhoM, Mh0):
    q = 2.2
    func_EPS = 1/(np.sqrt(sigma_M(k,Pk,rhoM,Mh0/q)-sigma_M(k,Pk,rhoM,Mh0)))
    return Mh0*np.exp(-func_EPS*z)
   
def MAH(z, k, rhoM, Mh0, model_H, model, par1, par2):
    z_arr = np.linspace(4,20,100)
    H = H_f(model_H,1/(1+z_arr), par1, par2)
    MAH = -(1+z_arr)*H*np.gradient(Mh_EPS(z_arr, k/h, np.array(Pk(1, model, par1, par2))*h**3, rhoM, Mh0))/np.gradient(z_arr)
    MAH = scipy.interpolate.interp1d(z_arr, MAH, fill_value = 'extrapolate')
    return MAH(z)

from scipy.optimize import fsolve
model_H = 'nDGP'
model = 'nDGP'
pars1 = [100,250,500,1000,5000,10000,20000,30000,50000,100000]
pars2 = [100,250,500,1000,5000,10000,20000,30000,50000,100000]
colors = plt.cm.Blues(np.linspace(0,1,len(pars1)))
z_arr = np.linspace(0,8,10)
a_arr = 1/(1+z_arr)
#z = 9.1
#a  = 1/(1+z)
#for i in range(len(pars1)):
#    par1 = pars1[i]
#    par2 = pars2[i]
#    plt.plot(z, MAH(z, kvec, rhom, 1e13, model_H, model, par1, par2)/1e13)
    #plt.plot(z, Mh_EPS(z, kvec/h, np.array(Pk(1, model, par1, par2))*h**3, rhom, 1e9)/1e9)

par1 = 1000
par2 = 1


for i in range(len(z_arr)):
    z = z_arr[i]
    a = a_arr[i]
    model_SFR = 'phenomenological_regular'
    Masses = np.array(fsolve(lambda Mh: 1e8 - epsilon(Mh, model_SFR, a)*Omegab0/Omegab0*Mh, 1e11))
    Masses_star =  np.array([1e8])
    plt.scatter(z, h**3*SMD(kvec/h, np.array(Pk(a, model, par1, par2))*h**3, rhom, Masses, Masses_star, 1/(1+z), model_H, model, par1, par2), c = 'tab:blue')

x = [4, 5, 6, 7]
y = [10**7.36, 10**7.17, 10**6.76, 10**6.64]
zz = [10**0.06, 10**0.075, 10**0.115, 10**0.7]
plt.errorbar(x,y,yerr = zz, ls = 'None', c = 'tab:orange', marker = 's', capsize = 3)
#model_SFR = 'Behroozi'
#Masses_star = Mstar(Masses, model_SFR, a) 
#plt.scatter(Masses_star, SMD(kvec/h, np.array(Pk(a, model, par1, par2))*h**3, rhom, Masses, Masses_star, 1/(1+z), model_H, model, par1, par2), c = 'tab:blue')


#plt.plot(z, 24.1*(1e13/1e12)**1.094*(1+1.75*z)*np.sqrt(Omegam0*(1+z)**3+1-Omegam0), ls = ':', c = 'k')
#for i in range(len(pars1)):
#    par1 = pars1[i]
#    par2 = pars2[i]
#    plt.plot(Masses_star,SMF(Masses_star,kvec, Pk(a, model, par1, par2), rhom, a, model_H, model,model_SFR, par1, par2), color = colors[i])

#plt.plot(Masses, number_density(kvec/h, np.array(Pk(a, model, par1, par2))*h**3, rhom, Masses, a, model_H, model, par1, par2))

#x = np.loadtxt('Downloads/z0pt1.dat')[:,0] #https://github.com/bmoster/emerge/blob/master/data/smf.dat
#y = np.loadtxt('Downloads/z0pt1.dat')[:,1]
#zz = np.loadtxt('Downloads/z0pt1.dat')[:,2]
#plt.errorbar(10**x, 10**y, yerr = (abs(10**(y)-10**zz))*2, color = 'tab:grey', ecolor = 'tab:grey' ,ls = 'None', marker = '.')

from colossus.cosmology import cosmology
cosmology.setCosmology('planck18');
from colossus.lss import mass_function
mfunc = mass_function.massFunction(Masses, 0, mdef = 'fof', model = 'sheth99', q_out = 'dndlnM', sigma_args = {'filt': 'tophat'})
#plt.plot(Masses_star, h**3*np.gradient(np.log10(Masses_star),np.log10(Masses))*mfunc*np.log(10), c = 'tab:blue', ls = ':')
 
#plt.xscale('log')
plt.yscale('log')
#plt.xlim(10**8,10**12)
#plt.ylim(0,6)
plt.savefig('SMF.pdf', bbox_inches = 'tight')
