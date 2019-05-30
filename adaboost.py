from treeclass import Decisiontree
import math
import operator
import csv


class adaboost:
    tree_list = []
    tree_weight_list = []

    def __init__(self, dataset, numberoftrees = 10):
        self.dataset = dataset
        length = len(self.dataset)
        self.weight_dict = {i : 1 / length for i in range(length)}
        self.numberofclassifiers = numberoftrees

    def maketree(self):
        dec = Decisiontree()  # create the dicision tree object
        dec.load_dataset(self.dataset)  # loads the dataset into our object
        dec.load_weights(self.weight_dict)
        dec.train_tree(50, 0.9, 1)
        dec.unloaddata()
        return dec

    def update_weights(self, error, mask):
        for i in range(len(mask)):
            if not mask[i]:
                self.weight_dict[i] *= error / (1 - error)

        weight_sum = sum(self.weight_dict.values())
        self.weight_dict = {key : item / weight_sum for key,item in self.weight_dict.items()}

    def trainadaboost(self, maxdiscards):
        numberofdis = 0
        while len(self.tree_list) < self.numberofclassifiers and numberofdis < maxdiscards:
            tree = self.maketree()
            error, mask = tree.calculate_weighted_error(self.dataset, self.weight_dict)

            if error > 0.5:  # discard tree too high error
                numberofdis += 1
                continue

            self.tree_list.append(tree)  # save the model
            self.tree_weight_list.append(math.log((1 - error) / error))  # model weight on voting
            self.update_weights(error, mask)  # updates weights for next iteration


    def printtrees(self):
        for tree in self.tree_list:
            # tree = Decisiontree()
            tree.print_the_tree(tree.tree)

    def predict_sample(self, sample):
        classes = dict()
        i = 0
        for tree in self.tree_list:
            pred = tree.make_prediction(tree.tree, sample)[0]

            if not classes.__contains__(pred):
                classes[pred] = 0.0

            classes[pred] += self.tree_weight_list[i]

            i += 1

        return max(classes.items(), key=operator.itemgetter(1))[0]

    def predict(self, testdata):
        for row in testdata.iterrows():
            self.predict_sample(row)

    def calculate_metrics(self, test_data):
        correct = 0
        for index, row in test_data.iterrows():
            pred = self.predict_sample(row)  # get prediction for the row

            if pred == row[-1]:
                correct = correct + 1

        print("accuracy " + str(correct / len(test_data)))

    # creates an output file to store the predictions from the given data
    def make_output_file(self, test_data):
        with open('output.csv', 'w', newline='') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            for index, row in test_data.iterrows():
                pred = self.predict_sample(row)
                wr.writerow([pred])
        myfile.close()
        return myfile


