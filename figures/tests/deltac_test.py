

# some_file.py
import matplotlib.cm as cm
from matplotlib.lines import Line2D
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy.integrate import odeint
from scipy import integrate
from scipy.special import lambertw
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import matplotlib.pylab as pl
import matplotlib as mpl
import matplotlib
from scipy import interpolate
import scipy
import sys
sys.path.insert(0, "../../")
sys.path.insert(0,'../../observational_data/GSMF')
from JWST_MG.reionization import reionization
from JWST_MG.cosmological_functions import cosmological_functions
from JWST_MG.constants import *
from JWST_MG.HMF import HMF
from JWST_MG.SMF import SMF
from JWST_MG.UVLF import UVLF

plt.rcParams.update({"text.usetex": True})


class OOMFormatter(matplotlib.ticker.ScalarFormatter):
    def __init__(self, order=0, fformat="%1.1f", offset=True, mathText=True):
        self.oom = order
        self.fformat = fformat
        matplotlib.ticker.ScalarFormatter.__init__(
            self, useOffset=offset, useMathText=mathText)

    def _set_order_of_magnitude(self):
        self.orderOfMagnitude = self.oom

    def _set_format(self, vmin=None, vmax=None):
        self.format = self.fformat
        if self._useMathText:
            self.format = r'$\mathdefault{%s}$' % self.format


plt.cla()
plt.figure()
plt.rcParams.update({"text.usetex": True})
fig = plt.figure(figsize=(4.25*1*.95, 1*2*0.95))
"""
ax = plt.subplot(4, 1, 1)


ax.xaxis.set_ticks([0, 0.25, 0.5, 0.75, 1])
ax.yaxis.set_ticks([0, 0.5, 1, 1.5])


ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_minor_locator(AutoMinorLocator())


plt.tick_params(axis='both', which='major', direction="in",
                labelsize=14, length=5, top=True, right=True)
plt.tick_params(axis='both', which='minor', direction="in",
                labelsize=11, length=4, top=True, right=True)
plt.tick_params(axis='both', which='major',
                direction="in", labelsize=14, length=5)
plt.tick_params(axis='both', which='minor',
                direction="in", labelsize=11, length=4)


model = 'E11'
model_H = 'LCDM'
model_SFR = 'toy'

par2 = 6/11
ac = 1
a_arr = np.linspace(ai, ac, 10000)
pars1 = np.linspace(1, -1, 2)

n = len(pars1)
colors = pl.cm.Blues(np.linspace(0, 1, n))

for i in range(len(pars1)):
    par1 = pars1[i]
    deltac = delta_c(ac, model, model_H, par1, par2)
    deltai_collapse = deltac.binary_search_di(
        ac, model, model_H, par1, par2, 0, len(delta_ini), abs_err)
    delta = deltac.linear(deltai_collapse, ac,
                          model, model_H, par1, par2)
    print("a")
    # print(Deltavir)
    plt.plot(delta[:, 0], delta[:, 1], c=colors[i])


norm = plt.Normalize(pars1.min(), pars1.max())
cbar = plt.colorbar(mpl.cm.ScalarMappable(cmap=pl.cm.Blues, norm=norm), ax=ax)
cbar.set_label(r'$E_{11}$', fontsize=16)

plt.ylabel(r'$\delta_{\rm m}(a)$', size='16')

# plt.xlim(10**(-3),1)
# plt.legend(loc='best')
plt.grid(".")
ax.set_xticklabels([])

h, l = ax.get_legend_handles_labels()
kw = dict(ncol=3, loc="lower center",
          fancybox=True, fontsize=11, frameon=False)
leg1 = ax.legend(h[:], l[:], bbox_to_anchor=[0.5, 1.08], **kw)
ax.add_artist(leg1)
plt.axhline(1.675, c='tab:gray', lw=0.8)
plt.text(0.1, 1.375, r'$\delta_{\rm c}|_{G_{\rm eff}=1}$',
         fontsize=13, c='tab:grey')
ax.fill_between([-0.1, 1.1], 1.675-0.025, 1.675 +
                0.025, alpha=0.25, color='tab:gray')
plt.xlim(-0.05, 1.05)

ax = plt.subplot(4, 1, 2)


ax.xaxis.set_ticks([0, 0.25, 0.5, 0.75, 1])
ax.yaxis.set_ticks([0, 0.5, 1, 1.5])


ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_minor_locator(AutoMinorLocator())


plt.tick_params(axis='both', which='major', direction="in",
                labelsize=14, length=5, top=True, right=True)
plt.tick_params(axis='both', which='minor', direction="in",
                labelsize=11, length=4, top=True, right=True)
plt.tick_params(axis='both', which='major',
                direction="in", labelsize=14, length=5)
plt.tick_params(axis='both', which='minor',
                direction="in", labelsize=11, length=4)


model = 'gmu'
model_H = 'LCDM'
model_SFR = 'toy'

par2 = 6/11
ac = 1
a_arr = np.linspace(ai, ac, 10000)
pars1 = np.linspace(0, 1, 2)

n = len(pars1)
colors = pl.cm.Blues(np.linspace(0, 1, n))

for i in range(len(pars1)):
    par1 = pars1[i]
    deltac = delta_c(ac, model, model_H, par1, par2)
    deltai_collapse = deltac.binary_search_di(
        ac, model, model_H, par1, par2, 0, len(delta_ini), abs_err)
    delta = deltac.linear(deltai_collapse, ac,
                          model, model_H, par1, par2)
    print("a")
    # print(Deltavir)
    plt.plot(delta[:, 0], delta[:, 1], c=colors[i])


norm = plt.Normalize(pars1.min(), pars1.max())
cbar = plt.colorbar(mpl.cm.ScalarMappable(cmap=pl.cm.Blues, norm=norm), ax=ax)
cbar.set_label(r'$g_{\mu}$', fontsize=16)

plt.ylabel(r'$\delta_{\rm m}(a)$', size='16')

# plt.xlim(10**(-3),1)
# plt.legend(loc='best')
plt.grid(".")
ax.set_xticklabels([])

h, l = ax.get_legend_handles_labels()
kw = dict(ncol=3, loc="lower center",
          fancybox=True, fontsize=11, frameon=False)
leg1 = ax.legend(h[:], l[:], bbox_to_anchor=[0.5, 1.08], **kw)
ax.add_artist(leg1)
plt.axhline(1.675, c='tab:gray', lw=0.8)
plt.text(0.1, 1.375, r'$\delta_{\rm c}|_{G_{\rm eff}=1}$',
         fontsize=13, c='tab:grey')
ax.fill_between([-0.1, 1.1], 1.675-0.025, 1.675 +
                0.025, alpha=0.25, color='tab:gray')
plt.xlim(-0.05, 1.05)
"""

"""
ax = plt.subplot(4, 1, 3)


ax.xaxis.set_ticks([0, 0.25, 0.5, 0.75, 1])

ax.yaxis.set_ticks([0, 0.5, 1, 1.5])

ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_minor_locator(AutoMinorLocator())


plt.tick_params(axis='both', which='major', direction="in",
                labelsize=14, length=5, top=True, right=True)
plt.tick_params(axis='both', which='minor', direction="in",
                labelsize=11, length=4, top=True, right=True)
plt.tick_params(axis='both', which='major',
                direction="in", labelsize=14, length=5)
plt.tick_params(axis='both', which='minor',
                direction="in", labelsize=11, length=4)


model = 'DES'
model_H = 'LCDM'
model_SFR = 'toy'

pars2 = np.array([0, 5, -5])
ac = 1
a_arr = np.linspace(ai, ac, 10000)
pars1 = np.linspace(0, 1, 2)

n = len(pars1)
colors = np.array([pl.cm.Blues(np.linspace(0, 1, n)), pl.cm.Reds(
    np.linspace(0, 1, n)), pl.cm.Purples(np.linspace(0, 1, n))])

for j in range(len(pars2)):
    par2 = pars2[j]
    for i in range(len(pars1)):
        par1 = pars1[i]
        deltac = delta_c(ac, model, model_H, par1, par2)
        deltai_collapse = deltac.binary_search_di(
            ac, model, model_H, par1, par2, 0, len(delta_ini), abs_err)
        delta = deltac.linear(deltai_collapse, ac,
                              model, model_H, par1, par2)
        print("a")
        # print(Deltavir)
        plt.plot(delta[:, 0], delta[:, 1], c=colors[j][i], alpha=0.3, lw=0.75)


norm = plt.Normalize(pars1.min(), pars1.max())
cbar = plt.colorbar(mpl.cm.ScalarMappable(cmap=pl.cm.Blues, norm=norm), ax=ax)
cbar.set_label(r'$T_{1}$', fontsize=16)

plt.ylabel(r'$\delta_{\rm m}(a)$', size='16')

# plt.xlim(10**(-3),1)
# plt.legend(loc='best')
plt.grid(".")
ax.set_xticklabels([])

h, l = ax.get_legend_handles_labels()


line1 = Line2D([0], [0], label=r'$T_2=0$', color='tab:blue')
line2 = Line2D([0], [0], label=r'$T_2=5$', color='tab:red')
line3 = Line2D([0], [0], label=r'$T_2=-5$', color='tab:purple')
h.extend([line1, line2, line3])
kw = dict(ncol=1,
          fancybox=True, fontsize=10, frameon=False)
# leg1 = ax.legend(h[:], l[:], bbox_to_anchor=[0.5, 1.08], **kw)
ax.legend(handles=h, loc='lower right', **kw)

plt.axhline(1.675, c='tab:gray', lw=0.8)
plt.text(0.1, 1.375, r'$\delta_{\rm c}|_{G_{\rm eff}=1}$',
         fontsize=13, c='tab:grey')
ax.fill_between([-0.1, 1.1], 1.675-0.025, 1.675 +
                0.025, alpha=0.4, color='tab:gray')
plt.xlim(-0.05, 1.05)
"""


ax = plt.subplot(1, 1, 1)


ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_minor_locator(AutoMinorLocator())


plt.tick_params(axis='both', which='major', direction="in",
                labelsize=14, length=5, top=True, right=True)
plt.tick_params(axis='both', which='minor', direction="in",
                labelsize=11, length=4, top=True, right=True)
plt.tick_params(axis='both', which='major',
                direction="in", labelsize=14, length=5)
plt.tick_params(axis='both', which='minor',
                direction="in", labelsize=11, length=4)





#plt.errorbar(x, y, yerr=yerr, xerr=xerr, fmt='.')
from multiprocessing import Pool
#############################################
#
# extract spectra and plot them
#
#############################################
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy.integrate import odeint
from scipy import integrate
from scipy.special import lambertw
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import matplotlib.pylab as pl

plt.figure()
plt.rcParams.update({"text.usetex":True})
fig = plt.figure(figsize=(4.25*0.9*2,3*0.9*1.75))
ax_Pk = plt.subplot(221)

ax_Pk.xaxis.set_minor_locator(AutoMinorLocator())
ax_Pk.yaxis.set_minor_locator(AutoMinorLocator())


ax_Pk.tick_params(axis='both', which='major',direction="in", labelsize=14, length = 5, top=True,right=True)
ax_Pk.tick_params(axis='both', which='minor',direction="in", labelsize=12, length = 4, top=True,right=True)
ax_Pk.tick_params(axis='both', which='major',direction="in", labelsize=14, length = 5)
ax_Pk.tick_params(axis='both', which='minor',direction="in", labelsize=12, length = 4)


pool_cpu = Pool(8)

from JWST_MG.delta_c import delta_c

model = 'kmoufl'
model_H = 'kmoufl'
model_SFR = 'phenomenological_extreme'
par1 = 0.01
par2 = 0.01
f0 = 0.1
z = 0
"""deltac_library = delta_c(a_arr, model, model_H, par1, par2)
deltai_collapse = deltac_library.binary_search_di( 1, model, model_H, par1, par2, 0, len(delta_ini), abs_err)
print(deltai_collapse)
delta_nl = deltac_library.non_linear(deltai_collapse, a_arr, model, model_H, par1, par2)
"""
ac_arr = np.linspace(0.01, 1, 15)
for ac in tqdm(ac_arr):
    a_arr = np.linspace(ai, ac, 1000)
    reion_library = reionization(a_arr, model, model_H, par1, par2, model_SFR, f0)
    a_vir, Deltavir  = reion_library.Delta_vir(model, model_H, par1, par2, a_arr)

    plt.scatter(ac, Deltavir)



#print(SMF)
#Masses_star = SMF[0]
#SMF_obs = SMF[1]


"""ac_arr = np.linspace(0.01, 1, 15)
par1 = 500
par2 = 0
deltac = delta_c(ac_arr, model, model_H, par1, par2)


di = deltac.binary_search_di(1, model, model_H, par1, par2,
                             0, len(delta_ini)-1, abs_err)
print(di)
delta_nl = deltac.collapse(di, model, model_H, par1, par2)
delta = delta_nl[:, 1]
a = delta_nl[:, 0]
cosmological_library = cosmological_functions(
    a, model, model_H, par1, par2)
H = cosmological_library.H_f(a, model_H, par1, par2)
dH = cosmological_library.dH_f(a, model_H, par1, par2)


G = 1/(8*np.pi)
Hdot = a*H*dH
beta = 1 + 2*H*par1/c*(1+Hdot/(3*H**2))
epsilon = 8/(9*beta**2)*(H0*par1/c)**2*Omegam0*a**(-3)
RRV = (epsilon*delta)**(-1/3)
mu = cosmological_library.mu(
    a, model, model_H, par1, par2, type='nonlinear', x=RRV)

plt.plot(a, epsilon*delta)


par1 = 3000
par2 = 0
deltac = delta_c(ac_arr, model, model_H, par1, par2)


di = deltac.binary_search_di(1, model, model_H, par1, par2,
                             0, len(delta_ini)-1, abs_err)
print(di)
delta_nl = deltac.collapse(di, model, model_H, par1, par2)
delta = delta_nl[:, 1]
a = delta_nl[:, 0]
cosmological_library = cosmological_functions(
    a, model, model_H, par1, par2)
H = cosmological_library.H_f(a, model_H, par1, par2)
dH = cosmological_library.dH_f(a, model_H, par1, par2)


G = 1/(8*np.pi)
Hdot = a*H*dH
beta = 1 + 2*H*par1/c*(1+Hdot/(3*H**2))
epsilon = 8/(9*beta**2)*(H0*par1/c)**2*Omegam0*a**(-3)
RRV = (epsilon*delta)**(-1/3)
mu = cosmological_library.mu(
    a, model, model_H, par1, par2, type='nonlinear', x=RRV)

plt.plot(a, epsilon*delta)
plt.xlim(0.3, 1)
plt.ylim(0.05, 500)
plt.yscale('log')

"""
"""model = 'nDGP'
model_H = 'nDGP'
par1 = 3000
par2 = 0.5
a_arr = np.linspace(0.1, 1, 10)
reion = reionization(a_arr, model, model_H, par1, par2)

R_arr = reion.radius_solve(model, model_H, par1, par2, a_arr)

plt.plot(a_arr, R_arr)
plt.yscale('log')"""
# plt.plot(a, mu)
"""

model = 'kmoufl'
model_H = 'kmoufl'
par2 = 0.5
ac_arr = np.array([0.1, 0.5, 0.75, 1])
pars1 = np.linspace(0.1, 0.3, 10)

n = len(ac_arr)
colors = pl.cm.Reds(np.linspace(0, 1, 5))


for i in range(len(ac_arr)):
    Delta = []
    ac = ac_arr[i]
    a_arr = np.linspace(ai, ac, 10000)
    for par1 in pars1:
        reion = reionization(a_arr, model, model_H, par1, par2)
        a_vir, Deltavir = reion.Delta_vir(model, model_H, par1, par2, a_arr)
        print(Deltavir)
        Delta.append(Deltavir)
        # print(Deltavir)
    plt.plot(pars1, Delta, c=colors[i+1])

plt.xscale('log')

plt.axhline(18*np.pi**2, ls=':', c='tab:blue')"""
"""
par1 = 3000
par2 = 0
ac_arr = np.linspace(0.01, 1, 15)

for ac in ac_arr:
    deltac = delta_c(ac, model, model_H, par1, par2)
    dc = deltac.delta_c_at_ac(ac, model, model_H, par1, par2)
    plt.scatter(ac, dc, c='tab:blue')

plt.axhline(1.688, c='tab:blue', ls=':')


par1 = 500
par2 = 0
ac_arr = np.linspace(0.01, 1, 15)

for ac in ac_arr:
    deltac = delta_c(ac, model, model_H, par1, par2)
    dc = deltac.delta_c_at_ac(ac, model, model_H, par1, par2)
    plt.scatter(ac, dc, c='tab:orange')

plt.axhline(1.687, c='tab:orange', ls=':')
"""
"""
model = 'nDGP'
par2 = 0.5
ac_arr = np.array([0.1, 0.5, 0.75, 1])
pars1 = np.logspace(2.69897000434, 5, 10)

n = len(ac_arr)
colors = pl.cm.Reds(np.linspace(0, 1, 5))


for i in range(len(ac_arr)):
    Delta = []
    ac = ac_arr[i]
    a_arr = np.linspace(ai, ac, 10000)
    for par1 in pars1:
        reion = reionization(a_arr, model, model_H, par1, par2)
        a_vir, Deltavir = reion.Delta_vir(model, model_H, par1, par2, a_arr)
        print(Deltavir)
        Delta.append(Deltavir)
        # print(Deltavir)
    plt.plot(pars1, Delta, c=colors[i+1])

plt.xscale('log')

plt.axhline(18*np.pi**2, ls=':', c='tab:blue')"""
"""
par2 = 0.3
ac_arr = np.linspace(0.01, 1, 15)
par1 = 3000


deltac = delta_c(ac_arr, model, model_H, par1, par2)


di = deltac.binary_search_di(1, model, model_H, par1, par2,
                             0, len(delta_ini)-1, abs_err)
print(di)
delta_nl = deltac.collapse(di, model, model_H, par1, par2)
delta = delta_nl[:, 1]
a = delta_nl[:, 0]
cosmological_library = cosmological_functions(
    a, model, model_H, par1, par2)
H = cosmological_library.H_f(a, model_H, par1, par2)
dH = cosmological_library.dH_f(a, model_H, par1, par2)


G = 1/(8*np.pi)
Hdot = a*H*dH
beta = 1 + 2*H*par1/c*(1+Hdot/(3*H**2))
epsilon = 8/(9*beta**2)*(H0*par1/c)**2*Omegam0*a**(-3)
RRV = (epsilon*delta)**(-1/3)
mu = cosmological_library.mu(
    a, model, model_H, par1, par2, type='nonlinear', x=RRV)

plt.plot(a, mu, ls='-', c='tab:orange')
mu = cosmological_library.mu(
    a, model, model_H, par1, par2, type='linear', x=RRV)

plt.plot(a, mu, ls=':', c='tab:orange')


par2 = 0.3
ac_arr = np.linspace(0.01, 1, 15)
par1 = 500


deltac = delta_c(ac_arr, model, model_H, par1, par2)


di = deltac.binary_search_di(1, model, model_H, par1, par2,
                             0, len(delta_ini)-1, abs_err)
print(di)
delta_nl = deltac.collapse(di, model, model_H, par1, par2)
delta = delta_nl[:, 1]
a = delta_nl[:, 0]
cosmological_library = cosmological_functions(
    a, model, model_H, par1, par2)
H = cosmological_library.H_f(a, model_H, par1, par2)
dH = cosmological_library.dH_f(a, model_H, par1, par2)


G = 1/(8*np.pi)
Hdot = a*H*dH
beta = 1 + 2*H*par1/c*(1+Hdot/(3*H**2))
epsilon = 8/(9*beta**2)*(H0*par1/c)**2*Omegam0*a**(-3)
RRV = (epsilon*delta)**(-1/3)
mu = cosmological_library.mu(
    a, model, model_H, par1, par2, type='nonlinear', x=RRV)

plt.plot(a, mu, ls='-', c='tab:blue')
mu = cosmological_library.mu(
    a, model, model_H, par1, par2, type='linear', x=RRV)

plt.plot(a, mu, ls=':', c='tab:blue')


plt.yscale('log')
plt.xlim(0.2, 1)"""
# p
"""
plt.yscale('log')
plt.ylabel(r'$\delta_{\rm m}(a)$', size='16')
# plt.ylim(1.65, 1.7)
# plt.axhline(1.686, c='tab:gray')

# plt.axhline(1.672, c='tab:gray', ls=':')
# plt.xlim(10**(-3),1)
# plt.legend(loc='best')
plt.grid(".")
"""


plt.tight_layout()
plt.savefig('delta_c.pdf', bbox_inches='tight')
