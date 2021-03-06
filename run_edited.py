import pandas as pd
from pandas import Series,DataFrame
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import csv

from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split
from sklearn import metrics
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.lda import LDA

	
trainDF = pd.read_csv('cs-training.csv')

#can drop NaN values
trainDF = trainDF.dropna() 

#30-59DaysPastDueNotWorse contains values 96 and 98, which are typos
#will replace them will median of 30-59DaysPastDueNotWorse

#trainDF=trainDF.groupby('NumberOfTime30-59DaysPastDueNotWorse').transform(getmedian)
#trainDF['NumberOfTime30-59DaysPastDueNotWorse'].max()
#both don't work

#use loc, which picks out the entries in trainDF['NumberOfTime30-59DaysPastDueNotWorse] that contain 98 or 96
#set those outliers to the median value
trainDF['NumberOfTime30-59DaysPastDueNotWorse'].loc[(trainDF['NumberOfTime30-59DaysPastDueNotWorse']==98) | (trainDF['NumberOfTime30-59DaysPastDueNotWorse']==96)] = trainDF['NumberOfTime30-59DaysPastDueNotWorse'].median()


'''
#dummify the categorical variables into binary variables
dummy_age = pd.get_dummies(X['age'], prefix='age')
dummy_n3059L = pd.get_dummies(X['NumberOfTime30-59DaysPastDueNotWorse'], prefix='n3059L')
dummy_nCreditLoans = pd.get_dummies(X['NumberOfOpenCreditLinesAndLoans'], prefix='nCreditLoans')
dummy_n90L = pd.get_dummies(X['NumberOfTimes90DaysLate'], prefix='n90L')
dummy_nRE = pd.get_dummies(X['NumberRealEstateLoansOrLines'], prefix='nRE')
dummy_n6089L = pd.get_dummies(X['NumberOfTime60-89DaysPastDueNotWorse'], prefix='n6089L')
dummy_nDep = pd.get_dummies(X['NumberOfDependents'], prefix='nDep')

#keep track of the non-categorical variables
orig_cols=['SeriousDlqin2yrs', 'RevolvingUtilizationOfUnsecuredLines', 'DebtRatio', 'MonthlyIncome']

#join the binary variables with the non-categorical variables
#print "dummy_age", dummy_age.ix[:, 'age_0':].head()
newTrain = X[orig_cols].join(dummy_age.ix[:, 'age_21':]) #attach all dummy_age columns 
#except the first one, 'age_0', because that is the baseline and needs to be excluded
#to avoid MULTICOLLINEARITY, or the DUMMY VARIABLE TRAP
newTrain = newTrain.join(dummy_n3059L.ix[:, 'n3059L_1':])
newTrain = newTrain.join(dummy_nCreditLoans.ix[:, 'nCreditLoans_1':])
newTrain = newTrain.join(dummy_n90L.ix[:, 'n90L_1':])
newTrain = newTrain.join(dummy_nRE.ix[:, 'nRE_1':])
newTrain = newTrain.join(dummy_n6089L.ix[:, 'n6089L_1':])
newTrain = newTrain.join(dummy_nDep.ix[:, 'nDep_1':])
#print "newTrain", newTrain.head()


print "dummy_age", dummy_age.head()
print "dummy_n3059", dummy_n3059L.head()
print "dummy_credit", dummy_nCreditLoans.head()
print "dummy_n90L", dummy_n90L.head()
print "dummy_nRE", dummy_nRE.head()
print "dummy_n6089L", dummy_n6089L.head()
print "dummy_nDep", dummy_nDep.head()
'''

#LDA
all_cols=['SeriousDlqin2yrs', 'RevolvingUtilizationOfUnsecuredLines', 'DebtRatio', 'MonthlyIncome', 'age', 'NumberOfTime30-59DaysPastDueNotWorse', 'NumberOfOpenCreditLinesAndLoans', 'NumberOfTimes90DaysLate', 'NumberRealEstateLoansOrLines', 'NumberOfTime60-89DaysPastDueNotWorse', 'NumberOfDependents']
newTrain = trainDF[all_cols]
features = newTrain.columns[1:]

#need to use numpy array for LDA and PCA
Ymat = newTrain['SeriousDlqin2yrs'].as_matrix()
Xmat=newTrain.drop('SeriousDlqin2yrs',1).as_matrix()

print "Xmat", Xmat[0:5]
print "Ymat", Ymat[0:5]
#print "newTrain[features] is ", newTrain[features].head()
#Xf=newTrain[features]

#print "Xf", Xf.head()
#yf=newTrain.SeriousDlqin2yrs
names=['nodefault','Default']

pca = PCA(n_components=2)
X_r = pca.fit(Xmat).transform(Xmat)
print "X_r", X_r[1:5]
print len(X_r)
lda = LinearDiscriminantAnalysis(n_components=2)
X_r2 = lda.fit(Xmat, Ymat).transform(Xmat)
print "X_r2", X_r2[1:5]


print('PCA explained variance ratio (first two components): %s'
      % str(pca.explained_variance_ratio_))
#[  9.98810930e-01   8.68900912e-04]
#so the 1st Principal Component explains 99.8% of the variance

#print('LDA explained variance ratio (first two components): %s'
#      % str(lda.explained_variance_ratio_))
#doesn't work in LDA


plt.figure()
for c, i, name in zip("rgb", [0, 1], names):
    plt.scatter(X_r[Ymat == i,0], X_r[Ymat == i, 1], c=c, label=name)
plt.legend()
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.title('PCA of Credit Default')
plt.savefig('PCA.png')

plt.figure()
for c, i, name in zip("rgb", [0, 1], names):
    plt.scatter(X_r2[Ymat == i], X_r2[Ymat == i], c=c, label=name)
plt.legend()
plt.xlabel('LD1')
plt.ylabel('LD2')
plt.title('LDA of Credit Default')
plt.savefig('LDA.png')

plt.show()



