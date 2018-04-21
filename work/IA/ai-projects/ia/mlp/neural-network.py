import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV

data_types = {
    "wti_variance": "float",
    "wti_skewness": "float",
    "wti_curtosis": "float",
    "image_entropy": "float",
    "class": "int"
}

columns = ["wti_variance", "wti_skewness", "wti_curtosis", "image_entropy", "class"]
dataset = pd.read_csv("dados_autent_bancaria.txt", dtype=data_types, names=columns)

print(dataset.head())
print(dataset.shape)
print(dataset.groupby('class').count())

X = dataset.drop('class', axis=1)
y = dataset['class']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

#  solver : 'sgd' refers to stochastic gradient descent.
#  alpha  : float, optional, default 0.0001  L2 penalty (regularization term) parameter.
#  momentum: float, default 0.9
#  Momentum for gradient descent update.Should be between 0 and 1. Only used when solver = 'sgd'.
#   hidden_layer_sizes :
#  activation :  'logistic', the logistic sigmoid function, returns f(x) = 1 / (1 + exp(-x)).

param_grid = [
        {
            'activation' : ['identity', 'logistic', 'tanh', 'relu'],
            'solver' : ['lbfgs', 'sgd', 'adam'],
            'hidden_layer_sizes': [(1,),(2,),(3,),(4,),(5,),(6,)]
        }
       ]

clf = GridSearchCV(MLPClassifier(learning_rate='adaptive', learning_rate_init=1., early_stopping=True, shuffle=True,random_state=42), param_grid, cv=3, n_jobs=-1, scoring='accuracy')
clf.fit(X,y)


print("Best parameters set found on development set:")
print(clf.best_params_)
# {'activation': 'logistic', 'hidden_layer_sizes': (2,), 'solver': 'lbfgs'}

y_pred = clf.predict(X_test)
print(accuracy_score(y_test, y_pred))

print(confusion_matrix(y_test, y_pred))


print(pd.crosstab(y_test, y_pred, rownames=['True'], colnames=['Predicted'], margins=True))

import matplotlib.pyplot as plt
conf = confusion_matrix(y_test, y_pred)
plt.imshow(conf, cmap='binary', interpolation='None')
plt.show()

