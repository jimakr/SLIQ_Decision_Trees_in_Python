import pandas as pd
from treeclass import Decisiontree
import numpy as np


data = pd.read_csv('heart.csv', delimiter=',', na_values=['no info', '.'])
msk = np.random.rand(len(data)) < 0.9  # split the dataset 90-10 for train and test randomly choosing rows
train_data = data[msk]
test_data = data[~msk]

dec = Decisiontree()
dec.load_dataset(train_data)
tree = dec.train_tree(5, 0.9)
dec.print_the_tree(tree)
dec.calculate_metrics(test_data)




