from os import listdir, system, makedirs
from os.path import isfile, join, exists

from sklearn.model_selection import train_test_split
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV

import scipy as sp
import numpy as np
import pickle

import parselmouth as pm
from tysums import *
from henrys import *


train_matrix, test_matrix, train_labels, test_labels = train_test_split(full_data_matrix, full_labels_array, test_size=0.2, random_state=42)

param_grid = [
    {
    'learning_rate': [0.25, 0.5, 0.75], 
    'base_estimator__criterion': ['gini', 'entropy'],
    'base_estimator__max_depth': [None, 10, 15, 20]
    }
]

ada_clf = AdaBoostClassifier(base_estimator=DecisionTreeClassifier(splitter='random'), algorithm='SAMME.R', n_estimators=200)

grid_search_clf = GridSearchCV(ada_clf, param_grid=param_grid, cv=5, scoring='roc_auc', return_train_score=True, refit=True)

grid_search_clf.fit(train_matrix, train_labels)

best_model = grid_search_clf.best_estimator_

f = open(join(PATH_TO_MTC_DATA, 'tpm-f2020-project/grid_search_clf.pkl'), "wb")
pickle.dump(grid_search_clf,f)
f.close()
    
f = open(join(PATH_TO_MTC_DATA, 'tpm-f2020-project/best_model.pkl'), "wb")
pickle.dump(best_model,f)
f.close()

