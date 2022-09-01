# PCReg

PCReg is a user-friendly one-command-line python script kit which can perform linear or non-linear dimensionality reduction and perform principle component regression based on these principle components (PCs) reduced from the linear or non-linear dimensionality reduction. PCReg includes two statistical models for the current version, linear regression and logistic regression. You need to choose the correct model depending on the data type of the response variable (linear regression if the response variable is continuous and logistic regression if the response variable is binary).

PCReg is compiled in Python 3. Please type the following command in your terminal if you have not installed one or some of these python module(s) in python 3:

**pip3 install pandas statistics numpy random sklearn scipy statsmodels argparse warnings**

You need to provide one matrix file for dimensionality reduction and one covariate matrix file for PC regression. The two matrix files have the same order of individual samples as rows. The dimensionality reduction matrix file has the variables you want to perform dimensionality reduction as the columns. The covariate matrix file has all covariates and a response variable as the columns. Both matrix files are comma-separated. The example matrix files were provided to test the scripts.

The example command to run PCReg:

**python PCReg_logistic_regression_argparse_final.py --mtx4pc_file dimensionality_reduction_matrix.csv --covars_file covariate_matrix.csv --variance_thre 0.9 --dr_method rbf --covars age sex RIN --dep_var diagnosis**

***--mtx4pc_file*** is the argument to provide the dimensionality reduction matrix file and ***--covars_file*** is the argument to provide the covariate matrix file.

***--variance_thre*** is the argument to provide the threshold for accumulative variance which can be explained by top PCs. The threshold ranges between 0 and 1. Default threshold is 0.9.


