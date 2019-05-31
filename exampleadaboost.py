import pandas as pd
from treeclass import Decisiontree
from adaboost import adaboost
import numpy as np

# load the dataset and define the no value symbol in the dataset
# beacuse 2^k are the possible subsets to check in discrete values we take only a portion of the data
data = pd.read_csv('heart.csv', delimiter=',', na_values=['no info', '.'])[0:500]
msk = np.random.rand(len(data)) < 0.9  # split the dataset 90-10 for train and test randomly choosing rows
train_data = data[msk]
test_data = data[~msk]

print("start the training")
adabo = adaboost(train_data)
dec = adabo.maketree(3)
# print(adabo.weight_dict)
adabo.trainadaboost()
adabo.printtrees()
# print(adabo.predict_sample(test_data.iloc[0]))
adabo.make_output_file(test_data)
adabo.calculate_metrics(test_data)





