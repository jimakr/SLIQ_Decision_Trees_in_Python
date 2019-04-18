import pandas as pd
from treeclass import Decisiontree
import numpy as np

# load the dataset and define the no value symbol in the dataset
# beacuse 2^k are the possible subsets to check in k discrete values we take only a portion of the data
data = pd.read_csv('master.csv', delimiter=',', na_values=['no info', '.'])[0:3000]
msk = np.random.rand(len(data)) < 0.9  # split the dataset 90-10 for train and test randomly choosing rows
train_data = data[msk]
test_data = data[~msk]

dec = Decisiontree() # create the dicision tree object
print("training")
dec.load_dataset(train_data) # loads the dataset into our object
# train and define minimum number of children and the similarity in each leaf in order to split
tree = dec.train_tree(50, 0.9)
dec.print_the_tree(tree)
print("testing")
dec.calculate_metrics(test_data) # calculate accuracy




