import pandas as pd
from adaboost import AdaBoost
import numpy as np

# load the dataset and define the no value symbol in the dataset
# beacuse 2^k are the possible subsets to check in discrete values we take only a portion of the data
data = pd.read_csv('heart.csv', delimiter=',', na_values=['no info', '.'])[0:500]
msk = np.random.rand(len(data)) < 0.9  # split the dataset 90-10 for train and test randomly choosing rows
train_data = data[msk]
test_data = data[~msk]

print("start the training")
# create an AdaBoost object and pass the train data,the user can define the max number of trees, but the default is 10
# adabo = AdaBoost(train_data,8)
adabo = AdaBoost(train_data)
# train AdaBoost with default max tree depth=1 , the user can define this parameter
adabo.trainadaboost()
# print all the trees found
adabo.printtrees()
# print(adabo.predict_sample(test_data.iloc[0]))  #predicts the output for the first row of test data
adabo.make_output_file(test_data)
adabo.calculate_metrics(test_data)
