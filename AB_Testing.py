import pandas as pd
import itertools
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# !pip install statsmodels
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, pearsonr, spearmanr, kendalltau, f_oneway, \
    kruskal
from statsmodels.stats.proportion import proportions_ztest

# Preparing and Analyzing the Data

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.float_format', lambda x: '%.4f' % x)


control_group = pd.read_excel("Measurement Problems/Projects/ab_testing.xlsx", sheet_name="Control Group")
control_group.head()

test_group = pd.read_excel("Measurement Problems/Projects/ab_testing.xlsx", sheet_name="Test Group")
test_group.head()

control_group.describe().T
test_group.describe().T

df = pd.concat([control_group, test_group], axis=1)
df.head()

# Defining the Hypothesis of A/B Testing

# HO: M1 = M2 (There is no significant difference between Average Bidding and Maximum Bidding in purchase averages.)
# H1: M1 != M2 (There is a significant difference between Average Bidding and Maximum Bidding in purchase averages.)

# Analyzing the purchase averages of the control and test groups

control_group["Purchase"].mean() # 550.8940587702316
test_group["Purchase"].mean() # 582.1060966484675

# Checking assumptions to decide appropriate test type (parametric/non-parametric)

# Assumption 1: Normality

# Hypothesis

# H0: The sample datasets are normally distributed. The assumption of normal distribution is PROVIDED.
# H1: The sample datasets are not normally distributed.The assumption of normal distribution is NOT PROVIDED.

test_stat, pvalue = shapiro(control_group["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

test_stat, pvalue = shapiro(test_group["Purchase"]) # 0.5891
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue)) # 0.1541

# It was failed to reject H0 hypothesis, because 0.5891 > 0.05 and 0.1541 > 0.05.
# It can be said that the sample datasets are normally distributed and assumption 1 is met.

# Assumption 2: Variance Homogeneity

# Hypothesis

# H0: Variances are Homogeneous.The assumption of Variance Homogeneity is PROVIDED.
# H1: Variances are not Homogeneous.The assumption of Variance Homogeneity is NOT PROVIDED.

test_stat, pvalue = levene(control_group["Purchase"], test_group["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# It was failed to reject H0 hypothesis, because 0.1083 > 0.05.
# It can be said that variances are Homogeneous and assumption 2 is met.

####################################################################################
# Implementing the Hypothesis Testing with Parametric Test
###################################################################################

# Both of the assumptions are provided, so independent two-sample t-test (parametric test) is used.

# Hypothesis

# HO: M1 = M2 (There is no significant difference between Average Bidding and Maximum Bidding in purchase averages.)
# H1: M1 != M2 (There is a significant difference between Average Bidding and Maximum Bidding in purchase averages.)


test_stat, pvalue = ttest_ind(control_group["Purchase"], test_group["Purchase"], equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue)) # Test Stat = -0.9416, p-value = 0.3493

# It was failed to reject H0 hypothesis, because 0.3493 > 0.05.
# It can be said that there is no significant difference between Average Bidding and Maximum Bidding in purchase
# averages.

# We can recommend our customer to withdraw their investment by being told that average bidding does not bring more
# conversions than maximum bidding and that there is no significant difference between them.