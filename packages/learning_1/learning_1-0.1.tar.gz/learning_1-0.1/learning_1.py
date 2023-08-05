
# coding: utf-8

# In[ ]:


import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn import preprocessing
from sklearn import datasets
import numpy as np
from sklearn import metrics
from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import KNeighborsClassifier
from sklearn.grid_search import RandomizedSearchCV


# In[2]:


class supervised_classification():
    
    def __init__(self, ind_variables, dep_variable):
        self.ind_variables = ind_variables
        self.dep_variable = dep_variable    
      
    def build_logistic_regression(self):
        self.ind_variables = preprocessing.scale(self.ind_variables)
        self.dep_variable = self.dep_variable.astype('category')
        logistic_reg = LogisticRegression()
        params = {"solver": ["liblinear","newton-cg","sag","lbfgs"],"tol":np.arange(0.01,1,0.01)}
        grid = RandomizedSearchCV(logistic_reg, params)
        self.logistic_fit = grid.fit(self.ind_variables, self.dep_variable)
        return self.logistic_fit    
    
    def score_logistic_regression(self, to_score):
        self.score = self.logistic_fit.predict_proba(to_score)
        return self.score
    
    def build_knn(self):
        model = KNeighborsClassifier()
        params = {"n_neighbors": np.arange(1, 31, 2),"metric": ["euclidean", "cityblock"]}
        grid = RandomizedSearchCV(model, params)
        self.knn_fit = grid.fit(self.ind_variables, self.dep_variable)
        return self.knn_fit
    
    def score_knn(self, to_score):
        self.score = self.knn_fit.predict_proba(to_score)
        return self.score

