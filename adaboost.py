from treeclass import Decisiontree

class adaboost:
    dataset = []
    tree_list = []
    weight_list = []

    def __init__(self, dataset):
        self.dataset = dataset
        length = len(self.dataset)
        self.weight_list = [1 / length for i in range(length)]

    def maketree(self):
        dec = Decisiontree()  # create the dicision tree object
        dec.load_dataset(self.dataset)  # loads the dataset into our object
        tree = dec.train_tree(50, 0.9, 1)
        return tree

    def calculate_weights(self, error, mask):
        self.weight_list[mask] *= error / (1 - error)
        weight_sum = sum(self.weight_list)
        for item in self.weight_list:
            item = item / weight_sum

