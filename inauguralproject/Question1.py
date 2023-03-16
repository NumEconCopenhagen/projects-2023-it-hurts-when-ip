
from types import SimpleNamespace

import numpy as np
from scipy import optimize

import pandas as pd 
import matplotlib.pyplot as plt

class HouseholdSpecializationModelClass:

    def __init__(self):
        """ setup model """

        # a. create namespaces
        par = self.par = SimpleNamespace()
        sol = self.sol = SimpleNamespace()

        # b. preferences
        par.rho = 2.0
        par.nu = 0.001
        par.epsilon = 1.0
        par.omega = 0.5 

        # c. household production
        par.alpha = 0.5
        par.sigma = 1.0

        # d. wages
        par.wM = 1.0
        par.wF = 1.0
        par.wF_vec = np.linspace(0.8,1.2,5)

        # e. targets
        par.beta0_target = 0.4
        par.beta1_target = -0.1

        # f. solution
        sol.LM_vec = np.zeros(par.wF_vec.size)
        sol.HM_vec = np.zeros(par.wF_vec.size)
        sol.LF_vec = np.zeros(par.wF_vec.size)
        sol.HF_vec = np.zeros(par.wF_vec.size)

        sol.beta0 = np.nan
        sol.beta1 = np.nan

    def calc_utility(self,LM,HM,LF,HF):
        """ calculate utility """

        par = self.par
        sol = self.sol

        # a. consumption of market goods
        C = par.wM*LM + par.wF*LF

        # b. home production
        H = HM**(1-par.alpha)*HF**par.alpha

        # c. total consumption utility
        Q = C**par.omega*H**(1-par.omega)
        utility = np.fmax(Q,1e-8)**(1-par.rho)/(1-par.rho)

        # d. disutlity of work
        epsilon_ = 1+1/par.epsilon
        TM = LM+HM
        TF = LF+HF
        disutility = par.nu*(TM**epsilon_/epsilon_+TF**epsilon_/epsilon_)
        
        return utility - disutility

    def solve_discrete(self,do_print=False):
        """ solve model discretely """
        
        par = self.par
        sol = self.sol
        opt = SimpleNamespace()
        
        #define the choice set
        x = np.linspace(0,24,49)
        LM,HM,LF,HF = np.meshgrid(x,x,x,x) # all combinations
    
        LM = LM.ravel() # vector
        HM = HM.ravel()
        LF = LF.ravel()
        HF = HF.ravel()

        #calculate utility for different parameter values
        alpha_list = [0.25, 0.50, 0.75]
        sigma_list = [0.5, 1.0, 1.5]

        fig, axs = plt.subplots(nrows=3, ncols=3, figsize=(10, 10))

        for i, alpha in enumerate(alpha_list):
            for j, sigma in enumerate(sigma_list):
                par.alpha = alpha
                par.sigma = sigma

                 #calculate utility
                u = self.calc_utility(LM,HM,LF,HF)

                 #set to minus infinity if constraint is broken
                I = (LM+HM > 24) | (LF+HF > 24) # | is "or"
                u[I] = -np.inf

                 #find maximizing argument
                k = np.argmax(u)
                opt.LM = LM[k]
                opt.HM = HM[k]
                opt.LF = LF[k]
                opt.HF = HF[k]

                 #store the results
                sol.LM_vec[j+i*3] = opt.LM
                sol.HM_vec[j+i*3] = opt.HM
                sol.LF_vec[j+i*3] = opt.LF
                sol.HF_vec[j+i*3] = opt.HF

                # plot the results
                axs[i, j].contourf(x, x, np.reshape(HF/HM, (49,49)), cmap=plt.cm.coolwarm)
                axs[i, j].set_xlabel('HF')
                axs[i, j].set_ylabel('HM')
                axs[i, j].set_title(r'$\alpha = {}, \sigma = {}$'.format(alpha, sigma))

        plt.tight_layout()
        plt.show()

         #print the results
        if do_print:
            for k,v in opt.__dict__.items():
                print(f'{k} = {v:6.4f}')

        return opt

    #def solve_wF_vec(self,discrete=False):
        """ solve model for vector of female wages """

        pass

    #def run_regression(self):
        """ run regression """

        #par = self.par
        #sol = self.sol

        #x = np.log(par.wF_vec)
        #y = np.log(sol.HF_vec/sol.HM_vec)
        #A = np.vstack([np.ones(x.size),x]).T
        #sol.beta0,sol.beta1 = np.linalg.lstsq(A,y,rcond=None)[0]
    
    #def estimate(self,alpha=None,sigma=None):
        """ estimate alpha and sigma """

        #pass

model = HouseholdSpecializationModelClass()
model.solve_discrete(do_print=False)
# define parameter combinations to loop over
#alpha_vals = [0.25, 0.5, 0.75]
#sigma_vals = [0.5, 1.0, 1.5]

# create subplots
#fig, axes = plt.subplots(nrows=len(alpha_vals), ncols=len(sigma_vals), figsize=(12, 12))

# loop over parameter combinations and plot results
#for i, alpha in enumerate(alpha_vals):
 #   for j, sigma in enumerate(sigma_vals):
  #      model = HouseholdSpecializationModelClass()
   #     model.par.alpha = alpha
    #    model.par.sigma = sigma
     #   opt = model.solve_discrete()
      #  HF_over_HM = opt.HF / opt.HM
       # axes[i, j].plot(HF_over_HM)
        #axes[i, j].set_title(f"alpha = {alpha}, sigma = {sigma}")
        #axes[i, j].set_xlabel("Index")
        #axes[i, j].set_ylabel("HF / HM")

# add a title
#fig.suptitle("Effect of alpha and sigma on HF / HM")

# adjust subplot layout and spacing
#fig.tight_layout(pad=3.0)

##############################################################################################################################

