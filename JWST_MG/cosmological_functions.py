# Import some constants that are shared between all files
# Namely H0, Omegam0, Omegar0 etc.
from JWST_MG.constants import *


class cosmological_functions:

    ########################################################################
    # Initialize a class cosmological_functions
    # float a - scale factor value (related to redshift via a = 1/(1+z))
    # string model - model of MG for the derivation of mu parameter
    # string model_H - model of MG for H(a)
    # float par1, par2 - corresponding MG parameters
    ########################################################################

    def __init__(self, a, model, model_H, par1, par2):
        self.a = a
        self.model = model
        self.model_H = model_H
        self.par1 = par1
        self.par2 = par2

    """
    Calculate the Hubble parameter for different cosmological models.

    Parameters:
        a (float): The scale factor.
        model_H (str): The cosmological model ('LCDM', 'wCDM', 'nDGP', 'kmoufl').
        par1 (float): Additional parameter depending on the model.
        par2 (float): Additional parameter depending on the model.

    Returns:
        float: The value of the Hubble parameter for the given cosmological model.
    """
    def H_f(self, a, model_H, par1, par2):
        if model_H == 'LCDM':
            return H0*np.sqrt(1-Omegam0-Omegar0+Omegam0*a**(-3)+Omegar0*a**(-4))
        elif model_H == 'wCDM':
            wL = par1
            return H0*np.sqrt((1-Omegam0-Omegar0)*a**(-3*(1+wL))+Omegam0*a**(-3)+Omegar0*a**(-4))
        elif model_H == 'nDGP':
            rc = par1/c
            Omegarc = 1/(4*H0**2*rc**2)
            OmegaLambda0 = 1 - Omegam0 - Omegar0 + 2*np.sqrt(Omegarc)
            return H0*np.sqrt(Omegam0*a**(-3)+Omegar0*a**(-4)+Omegarc + OmegaLambda0)-H0*np.sqrt(Omegarc)
        elif model_H == 'kmoufl':
            closest_beta = (np.absolute(beta_arr-par1)).argmin()
            closest_K0 = (np.absolute(K0_arr-par2)).argmin()
            return kmoufl_H[closest_K0, closest_beta](a)
        else:
            raise Exception("Incorrect model specified.")

    """
    Calculate the Hubble parameter derivative for different cosmological models.

    Parameters:
        a (float): The scale factor.
        model_H (str): The cosmological model ('LCDM', 'wCDM', 'nDGP', 'kmoufl').
        par1 (float): Additional parameter depending on the model.
        par2 (float): Additional parameter depending on the model.

    Returns:
        float: The value of the Hubble parameter derivative for the given cosmological model.
    """

    def dH_f(self, a, model_H, par1, par2):
        self.a = a
        self.model_H = model_H
        self.par1 = par1
        self.par2 = par2

        if model_H == 'LCDM':
            return -0.5*(H0*(3*a*Omegam0 + 4*Omegar0))/(a**5*np.sqrt((a*Omegam0 + Omegar0 - a**4*(-1 + Omegam0 + Omegar0))/a**4))
        elif model_H == 'wCDM':
            wL = par1
            return (a**(-5 - 3*wL)*(3*a*H0*(1 + wL)*(-1 + Omegam0 + Omegar0) - a**(3*wL)*H0*(3*a*Omegam0 + 4*Omegar0)))/(2*np.sqrt((Omegar0 + a*(Omegam0 - (-1 + Omegam0 + Omegar0)/a**(3*wL)))/a**4))
        elif model_H == 'nDGP':
            rc = par1/c
            Omegarc = 1/(4*H0**2*rc**2)
            OmegaLambda0 = 1 - Omegam0 - Omegar0 + 2*np.sqrt(Omegarc)
            return (H0*((-3*Omegam0)/a**4 - (4*Omegar0)/a**5))/(2.*np.sqrt(OmegaLambda0 + Omegam0/a**3 + Omegar0/a**4 + Omegarc))
        elif model_H == 'kmoufl':
            closest_beta = (np.absolute(beta_arr-par1)).argmin()
            closest_K0 = (np.absolute(K0_arr-par2)).argmin()
            return kmoufl_dH[closest_K0, closest_beta](a)
        else:
            raise Exception("Incorrect model specified.")

    """
    Calculate the value of effective gravitational constant based on the given parameters.

    Parameters:
        a (float): The value of a.
        model (str): The model to use for the calculation.
        model_H (str): The model to use for calculating H.
        par1 (float): The first parameter for the model.
        par2 (float): The second parameter for the model.
        type (str, optional): The type of model (only used for nDGP model).
        x (float, optional): The value of x (only used for nonlinear nDGP model).

    Returns:
        float: The calculated value of mu.

    Raises:
        Exception: If an incorrect model is specified.
    """

    def mu(self, a, model, model_H, par1, par2, type=None, x=None):
        H = self.H_f(a, model_H, par1, par2)
        dHda = self.dH_f(a, model_H, par1, par2)
        dHdt = a*H*dHda
        rhom = 3*H0**2*Omegam0*a**(-3)
        rhor = 3*H0**2*Omegar0*a**(-4)
        rhoL = 3*H**2-rhom-rhor
        OmegaL = rhoL/(3*H**2)
        OmegaM = rhom/(3*H**2)
        if model == 'LCDM':
            return 1
        elif model == 'E11':
            f1 = par1*OmegaL
            return 1 + f1
        elif model == 'gmu':
            return 1 + par1*(1-a)**1 - par1*(1-a)**2
        elif model == 'DES':
            return 1 + par1*OmegaL + par2*OmegaL**2
        elif model == 'wCDM':
            wL = par1
            gamma = par2
            return 2/3*OmegaM**(gamma-1)*(OmegaM**gamma+2-3*gamma+3*(gamma-1/2)*(OmegaM+(1+wL)*OmegaL))
        elif model == 'nDGP':
            par1 = par1/c
            beta = 1 + 2*H*par1*(1+dHdt/(3*H**2))
            if type == 'linear':
                return 1 + 1/(3*beta)
            elif type == 'nonlinear':
                return 1 + 2/(3*beta)*(np.sqrt(1+x**(-3))-1)/(x**(-3))
            else:
                raise Exception("Incorrect Geff type for nDGP!")
        elif model == 'kmoufl':
            A_kmfl = 1.0 + par1*a
            X_kmfl = 0.5 * A_kmfl**2*(H*a)**2/((1-Omegam0-Omegar0)*H0**2)
            k_prime_mfl = 1.0 + 2.0*par2*X_kmfl
            epsl1_kmfl = 2.0*par1**2/k_prime_mfl
            X_kmfl_dot = 0.5 * A_kmfl**2 / \
                ((1-Omegam0-Omegar0)*H0**2)*2.0*H*a*(H*H*a+dHdt*a)
            return 1. + epsl1_kmfl
        else:
            raise Exception("Incorrect model specified.")
