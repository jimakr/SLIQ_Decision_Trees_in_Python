import pandas as pd
from treeclass import Decisiontree
import numpy as np


data = pd.read_csv('master.csv', delimiter=',', na_values=['no info', '.'])[0:3000]
msk = np.random.rand(len(data)) < 0.9  # split the dataset 90-10 for train and test randomly choosing rows
train_data = data[msk]
test_data = data[~msk]

dec = Decisiontree()
print("train")
dec.load_dataset(train_data)
tree = dec.train_tree(50, 0.6)
dec.print_the_tree(tree)
print("testing")
dec.calculate_metrics(test_data)
dec.make_output_file(test_data)



