import pandas as pd
from open_file import openthefile
from treeclass import Decisiontree
import numpy as np


data = pd.read_csv('heart.csv', delimiter=',', na_values= ['no info', '.'])
msk = np.random.rand(len(data)) < 0.9  # split the dataset 90-10 for train and test randomly choosing rows
train_data = data[msk]
test_data = data[~msk]
dataset, dictrid, columnnames = openthefile(train_data)
dec = Decisiontree()
tree = dec.train_tree(dataset, 5, 0.9)
dec.print_the_tree(tree, columnnames)
dec.calculate_metrics(test_data)




