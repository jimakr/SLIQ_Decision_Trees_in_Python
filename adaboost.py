from treeclass import Decisiontree


class adaboost:
    dataset = []
    tree_list = []
    tree_weight_list = []
    weight_dict = {}

    def __init__(self, dataset):
        self.dataset = dataset
        length = len(self.dataset)
        self.weight_list = [1 / length for i in range(length)]

    def maketree(self):
        dec = Decisiontree()  # create the dicision tree object
        dec.load_dataset(self.dataset)  # loads the dataset into our object
        dec.load_weights(self.weight_dict)
        dec.train_tree(50, 0.9, 1)
        dec.unloaddata()
        return dec

    def update_weights(self, error, mask):
        self.weight_list[mask] *= error / (1 - error)
        weight_sum = sum(self.weight_list)
        self.weight_list = [item / weight_sum for item in self.weight_list]

    def trainadaboost(self):
        for i in range(2):
            tree = self.maketree()
            error, mask = tree.calculate_weighted_error()

            if error > 0.5:  # discard tree too high error
                continue

            self.tree_list.append(tree)  # save the model
            self.tree_weight_list.append(((1 - error) / error))  # model weight on voting
            self.update_weights(error, mask)  # updates weights for next iteration

    def predict(self, testdata):
        for tree in self.tree_list:
            tree = self.maketree()
            tree.make_prediction(tree.tree, testdata[0])


