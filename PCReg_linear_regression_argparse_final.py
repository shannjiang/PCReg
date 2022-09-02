import pandas as pd
import statistics
import numpy as np
import random
import sklearn
from sklearn.decomposition import KernelPCA
#from sklearn.decomposition import PCA
import scipy
import statsmodels.api as sm
from scipy import stats
import argparse
import warnings
warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser()
parser.add_argument("--mtx4pc_file", type=str,
                    help="matrix for dimensionality reduction")
parser.add_argument("--covars_file", type=str,
                    help="covar matrix for linear regression")
parser.add_argument("--variance_thre", type=float, default=0.8,
                    help="percent of variance to keep the PCs. default value is 0.8.")
parser.add_argument("--dr_method", type=str, default='rbf',
                    help="dimensionality reduction method. default method is radial basis function.")
parser.add_argument('--covars', nargs='+',
                    help='covariates for linear regression')
parser.add_argument('--dep_var', type=str,
                    help='dependent variable for linear regression')
args = parser.parse_args()


def DimensionReduction4Regression(mtx4pc, dr_method, variance_thre):
    pca_method = KernelPCA(kernel=dr_method)
    PCs = pca_method.fit_transform(mtx4pc.to_numpy())
    PCnums = list(range(1, PCs.shape[1]+1))
    PCnames = []
    for PCnum in PCnums:
        PCnames.append('PC' + str(PCnum))
    PCs_df = pd.DataFrame(PCs, columns=PCnames)
    PCvariances = PCs_df.apply(statistics.variance, axis=0)
    PCvariance_df = pd.DataFrame(
        {'PCname': PCnames, 'PCvariance': PCvariances})
    PCvariance_df = PCvariance_df.sort_values(
        by=['PCvariance'], ascending=False)
    cum_variance = 0
    PCcum_variances = []
    for i in range(0, len(PCvariance_df['PCvariance'])):
        cum_variance = cum_variance + PCvariance_df['PCvariance'][i]
        PCcum_variances.append(cum_variance)
    PCvariance_df['PCcum_variance'] = PCcum_variances
    retain_PCvariance_df = PCvariance_df[PCvariance_df['PCcum_variance'] < variance_thre]
    PCs_df = pd.DataFrame(PCs, columns=PCnames)
    PCs_df.index = covars.index
    retain_PCs_df = PCs_df[retain_PCvariance_df['PCname'].to_list()]
    return(retain_PCs_df)


def PC_LinearRegression(retain_PCs_df, vars_df, covar, dep_var):
    reg_df = pd.concat([retain_PCs_df, vars_df], axis=1)
    if covar == ['None']:
        X_col = retain_PCs_df.columns.to_list()
        y_col = [dep_var]
        X = reg_df[X_col]
        y = reg_df[y_col]
        full_log_res = sm.OLS(y, X).fit()
        chi_stat = full_log_res.llr
        pval = full_log_res.llr_pvalue
        res = {'chi_stat': chi_stat, 'pvalue': pval}
        return(res)
    else:
        X_col = retain_PCs_df.columns.to_list() + covar
        y_col = [dep_var]
        X = reg_df[X_col]
        y = reg_df[y_col]
        full_log_res = sm.OLS(y, X).fit()
        # covar reg
        X_col = covar
        y_col = [dep_var]
        X = reg_df[X_col]
        y = reg_df[y_col]
        covar_log_res = sm.Logit(y, X).fit(method='bfgs')
        chi_stat = 2*(full_log_res.llf-covar_log_res.llf)
        #chi_squared_stats.append(chi_stat)
        pval = 1-stats.chi2.cdf(chi_stat, 2)
        res = {'chi_stat': chi_stat, 'pvalue': pval}
        return(res)


mtx4pc = pd.read_csv(args.mtx4pc_file, header=0, index_col=0)
covars = pd.read_csv(args.covars_file, header=0, index_col=0)

retain_PCs_df = DimensionReduction4Regression(mtx4pc, args.dr_method, args.variance_thre)
res = PC_LinearRegression(retain_PCs_df, covars, args.covars, args.dep_var)

print('chi_stat is ' + str(res['chi_stat']) + ', Pvalue is ' + str(res['pvalue']))
