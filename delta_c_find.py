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

common_settings = {'A_s':2.101e-9,
          'n_s':0.9665,
          'tau_reio':0.0561,
          'omega_b':0.02242,
          'omega_cdm':0.11933,
          'h':0.6766,
          'YHe':0.2425,
          'T_cmb':2.7255,
          'gauge':'newtonian', #FOR MGCLASS TO WORK, GAUGE NEEDS TO BE NEWTONIAN
          'k_pivot': 0.05,
          'mg_z_init': 111111.000,
          'l_logstep': 1.025,
          'l_linstep':15,
          'P_k_max_1/Mpc':3.0,
          'l_switch_limber':9,
          'perturb_sampling_stepsize': 0.05,
          'output':'tCl,pCl,lCl,mPk',
          'l_max_scalars': 3000,
          'lensing': 'yes',
          'mg_ansatz':'kmoufl'}


H0 = 67.66
Omegam0 = (0.02242/(H0/100)**2+0.11933/(H0/100)**2)
Omegar0 = 8.493e-5
c = 299792.45800000057


K0 = [0, 0.5, 1]
beta = np.linspace(0,0.5,10)
H_arr_kmoufl = [[],[],[]]
dH_arr_kmoufl = [[],[],[]]
H_int_kmoufl = [[],[],[]]
dH_int_kmoufl = [[],[],[]]

M = {}
for i in range(len(K0)):
    for j in tqdm(range(len(beta))):
        common_settings['beta_kmfl'] = beta[j]
        common_settings['k0_kmfl'] = K0[i]

        M[j] = Class()
        M[j].set(common_settings)
        
        M[j].compute()
        a = np.logspace(-6,0,10000)
        H_arr_kmoufl[i].append([M[j].Hubble(1/ai-1)*c for ai in a])
        dH_arr_kmoufl[i].append(np.gradient(H_arr_kmoufl[i][j])/np.gradient(a))
        H_int_kmoufl[i].append(scipy.interpolate.interp1d(a, H_arr_kmoufl[i][j], fill_value = 'extrapolate'))
        dH_int_kmoufl[i].append(scipy.interpolate.interp1d(a, dH_arr_kmoufl[i][j], fill_value = 'extrapolate'))
        
def H_f(a):
    if model_H == 'LCDM':
        return H0*np.sqrt(1-Omegam0-Omegar0+Omegam0*a**(-3)+Omegar0*a**(-4))
    elif model_H == 'wCDM':
        return H0*np.sqrt((1-Omegam0-Omegar0)*a**(-3*(1+wL))+Omegam0*a**(-3)+Omegar0*a**(-4))
    elif model_H == 'nDGP':
        Omegarc = 1/(4*H0**2*rc**2)
        OmegaLambda0 = 1 - Omegam0 - Omegar0 + 2*np.sqrt(Omegarc)
        return H0*np.sqrt(Omegam0*a**(-3)+Omegar0*a**(-4)+Omegarc + OmegaLambda0)-H0*np.sqrt(Omegarc)
    elif model_H == 'kmoufl':
        return H_int_kmoufl[i_kmoufl][j_kmoufl](a)

def dH_f(a):
    if model_H == 'LCDM':
        return -0.5*(H0*(3*a*Omegam0 + 4*Omegar0))/(a**5*np.sqrt((a*Omegam0 + Omegar0 - a**4*(-1 + Omegam0 + Omegar0))/a**4))
    elif model_H == 'wCDM':
        return (a**(-5 - 3*wL)*(3*a*H0*(1 + wL)*(-1 + Omegam0 + Omegar0) - a**(3*wL)*H0*(3*a*Omegam0 + 4*Omegar0)))/(2*np.sqrt((Omegar0 + a*(Omegam0 - (-1 + Omegam0 + Omegar0)/a**(3*wL)))/a**4))
    elif model_H == 'nDGP':
        Omegarc = 1/(4*H0**2*rc**2)
        OmegaLambda0 = 1 - Omegam0 - Omegar0 + 2*np.sqrt(Omegarc)
        return  (H0*((-3*Omegam0)/a**4 - (4*Omegar0)/a**5))/(2.*np.sqrt(OmegaLambda0 + Omegam0/a**3 + Omegar0/a**4 + Omegarc))
    elif model_H == 'kmoufl':
        return dH_int_kmoufl[i_kmoufl][j_kmoufl](a)
        
def mu(par1, par2, a):
    H = H_f(a)
    dHda = dH_f(a)
    dHdt = a*H*dHda
    rhom = 3*H0**2*Omegam0*a**(-3)
    rhor = 3*H0**2*Omegar0*a**(-4)
    rhoL = 3*H**2-rhom-rhor
    OmegaL = rhoL/(3*H**2)
    OmegaM = rhom/(3*H**2)
    if model == 'E11':
        f1 = par1*OmegaL
        return 1 + f1
    elif model =='gmu':
        return 1+ par1*(1-a)**1 - par1*(1-a)**2
    elif model == 'DES':
        return 1 + par1*OmegaL + par2*OmegaL**2
    elif model == 'wCDM':
        return 2/3*OmegaM**(gamma-1)*(OmegaM**gamma+2-3*gamma+3*(gamma-1/2)*(OmegaM+(1+wL)*OmegaL))
    elif model == 'nDGP':
        beta = 1 + 2*H/c*par1*(1+dHdt/(3*H**2))
        return 1 + 1/(3*beta)
    elif model == 'kmoufl':
        A_kmfl = 1.0 + par1*a
        X_kmfl = 0.5 * A_kmfl**2*(H*a)**2/((1-Omegam0-Omegar0)*H0**2)
        k_prime_mfl = 1.0 + 2.0*par2*X_kmfl
        epsl1_kmfl = 2.0*par1**2/k_prime_mfl    
        X_kmfl_dot = 0.5 * A_kmfl**2/((1-Omegam0-Omegar0)*H0**2)*2.0*H*a*(H*H*a+dHdt*a)
        return 1.+ epsl1_kmfl

def delta_nl_ODE(a, y, par1, par2):
    delta,ddeltada = y
    H = H_f(a)
    dH = dH_f(a)
    dddeltada          = -(3/a+dH/H)*ddeltada + (3*Omegam0*mu(par1, par2, a))/(2*a**5*H**2/H0**2)*delta*(1+delta) + 4*ddeltada**2/(3*(1+delta))
    return [ddeltada, dddeltada]

def delta_l_ODE(a, y, par1, par2):
    delta,ddeltada = y
    H = H_f(a)
    dH = dH_f(a)
    dddeltada          = -(3/a+dH/H)*ddeltada + (3*Omegam0*mu(par1, par2, a))/(2*a**5*H**2/H0**2)*delta
    return [ddeltada, dddeltada]

def collapse(deltai, par1, par2):
    ai = 1e-5
    dt = 0.0001
    ddeltai = deltai/ai
    init = [deltai, ddeltai]
    system = ode(delta_nl_ODE)
    system.set_f_params(*[par1, par2])
    system.set_initial_value(init, ai)
    
    data = [0,0]
    while system.successful() and system.y[0] <= 1e7 and system.t <= 1/(1-0.5):
        data = [system.t + dt, system.integrate(system.t + dt)[0]]   
        #plt.scatter(system.t+dt, system.integrate(system.t + dt)[0], c ='tab:blue')
    data = np.array(data)
    ac = data[0]

    return ac

def interpolate_ac(ac, par1, par2):
    delta_i = np.logspace(-4,-1,1000)
    arr_di_ac = []
    for i in tqdm(range(len(delta_i))):
        arr_di_ac.append([delta_i[i],collapse(delta_i[i],pars1,pars2)])
    interp_di_ac = scipy.interpolate.interp1d(np.array(arr_di_ac)[:,1],np.array(arr_di_ac)[:,0],fill_value = 'extrapolate')
    return interp_di_ac(ac)

def linear(deltai_collapse, a, par1, par2):
    ai = 1e-5
    dt = 0.0001
    ddeltai = deltai_collapse/ai    
    init = [deltai_collapse, ddeltai]
    system = ode(delta_l_ODE)
    system.set_f_params(*[par1, par2])
    system.set_initial_value(init, ai)
    
    data = []
    while system.successful() and system.t <= a:
        data.append([system.t + dt, system.integrate(system.t + dt)[0]])   
        #plt.scatter(system.t+dt, system.integrate(system.t + dt)[0], c ='tab:orange')
    
    data = np.array(data)
    return data

def delta_c_at_ac(ac, par1, par2):
    return linear(interp_di_ac(ac),ac,par1,par2)[-1,1]
