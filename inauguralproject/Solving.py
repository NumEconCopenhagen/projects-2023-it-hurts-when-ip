def square(x):
    """ square numpy array
    
    Args:
    
        x (ndarray): input array
        
    Returns:
    
        y (ndarray): output array
    
    """
    
    y = x**2
    return y


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
        if par.sigma == 1.0:
            H = HM**(1-par.alpha)*HF**par.alpha
        elif par.sigma == 0:
            min(HM, HF)
        else:
            ((1-par.alpha)*HM**((par.sigma-1)/par.sigma) + par.alpha*HF**((par.sigma-1)/par.sigma))**(par.sigma/(par.sigma-1))
        # c. total consumption utility
        Q = C**par.omega*H**(1-par.omega)
        utility = np.fmax(Q,1e-8)**(1-par.rho)/(1-par.rho)

        # d. disutlity of work
        epsilon_ = 1+1/par.epsilon
        TM = LM+HM
        TF = LF+HF
        disutility =  par.nu*(TM**epsilon_/epsilon_+TF**epsilon_/epsilon_)
        
        return utility - disutility

    def solve_discrete(self,do_print=False):
        """ solve model discretely """
        
        par = self.par
        sol = self.sol
        opt = SimpleNamespace()
        
        # a. all possible choices
        x = np.linspace(0,24,49)
        LM,HM,LF,HF = np.meshgrid(x,x,x,x) # all combinations
    
        LM = LM.ravel() # vector
        HM = HM.ravel()
        LF = LF.ravel()
        HF = HF.ravel()

        #calculate utility for different parameter values
        alpha_list = [0.25, 0.50, 0.75]
        sigma_list = [0.5, 1.0, 1.5]

        fig = plt.figure()
        ax = fig.add_subplot(projection = '3d')

        for i, alpha in alpha_list:
            for j, sigma in sigma_list:

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
                #sol.LM_vec[i, j] = opt.LM
                #sol.HM_vec[i, j] = opt.HM
                #sol.LF_vec[i, j] = opt.LF
                #sol.HF_vec[i, j] = opt.HF

                # plot the results
                
                #axs[i, j].contourf(x, x, np.reshape(HF/HM, (49,49)), cmap=plt.cm.coolwarm)
                #axs[i, j].xlabel('HF')
                #axs[i, j].ylabel('HM')
                HF_HM_reshaped = np.reshape(HF/HM, (49, 49, 49, 49))
                HF_HM_reshaped = np.mean(HF_HM_reshaped, axis=(1,3))
                ax.contourf(x, x, np.log(HF_HM_reshaped), cmap=plt.cm.coolwarm)
                ax.set(xlabel='HF', ylabel='HM', zlabel='alpha')
    
    

        plt.tight_layout()
        plt.show()

         #print the results
        if do_print:
            for k,v in opt.__dict__.items():
                print(f'{k} = {v:6.4f}')

        return opt

    def solve(self,do_print=False):
        """ solve model continously """

        pass    

    def solve_wF_vec(self,discrete=False):
        """ solve model for vector of female wages """

        pass

    def run_regression(self):
        """ run regression """

        par = self.par
        sol = self.sol

        x = np.log(par.wF_vec)
        y = np.log(sol.HF_vec/sol.HM_vec)
        A = np.vstack([np.ones(x.size),x]).T
        sol.beta0,sol.beta1 = np.linalg.lstsq(A,y,rcond=None)[0]
    
    def estimate(self,alpha=None,sigma=None):
        """ estimate alpha and sigma """

        pass