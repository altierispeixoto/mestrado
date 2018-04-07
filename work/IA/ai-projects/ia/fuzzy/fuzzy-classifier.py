import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
import seaborn as sns

import pandas as pd
from io import StringIO

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


print(dataset.groupby('class').count())


# Cluster using correct number of clusters (3)
cntr, U, U0, d, Jm, p, fpc = fuzz.cluster.cmeans(data=dataset, c=3, m=5, error=0.005, maxiter=1000, init=None)

print("centers")
print(cntr)

# Predict fuzzy memberships, U, for all points in test_data
U, _, _, _, _, fpc = fuzz.cluster.cmeans_predict(
    dataset.drop('class', axis=1), cntr, m=4, error=0.005, maxiter=1000, seed=1234)

print("predicted")
print(U)

print("FPC = {}".format(fpc))