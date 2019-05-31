from treeclass import Decisiontree
import math
import operator
import csv


# the adaboost class
class AdaBoost:
    tree_list = []
    tree_weight_list = []  # voting weights of each classifier

    def __init__(self, dataset, numberoftrees=10):
        self.dataset = dataset
        length = len(self.dataset)
        self.weight_dict = {i: 1 / length for i in range(length)}
        self.numberofclassifiers = numberoftrees

    # creates a tree and trains it, takes as input max depth of the tree
    def maketree(self, depth):
        dec = Decisiontree()  # create the decision tree object
        dec.load_dataset(self.dataset)  # loads the data into our object
        dec.load_weights(self.weight_dict)  # loads the weights
        dec.train_tree(50, 0.9, depth)  # see parameters in treeclass.py
        dec.unloaddata()  # deletes the data from the object to free memory for storing the model later
        return dec

    # Function that updates specified weights
    # mask is an array of booleans where every true needs change because it was correctly predicted
    def update_weights(self, error, mask):
        for i in range(len(mask)):
            if mask[i]:
                self.weight_dict[i] *= error / (1 - error)  # for every id that is true update

        weight_sum = sum(self.weight_dict.values())  # finds sum of all weights
        self.weight_dict = {key: item / weight_sum for key, item in self.weight_dict.items()}  # normalize weights

    # train trees until we reach the desired number of classifiers, or until we can't get classifiers with
    # above 0,5 accuracy. the tree is discarded if the error is >0.5
    def trainadaboost(self, depth=1):
        while len(self.tree_list) < self.numberofclassifiers:
            tree = self.maketree(depth)  # makes the classifier
            error, mask = tree.calculate_weighted_error(self.dataset, self.weight_dict)  # test it's weighted error
            # mask is boolean array with true for correct classifications

            if error > 0.5:  # discard tree too high error
                print("Warning could not find enough models due to high error")
                print("Found : " + str(len(self.tree_list)) + " models")
                break

            self.tree_list.append(tree)  # save the model
            self.tree_weight_list.append(math.log((1 - error) / error))  # model weight on voting
            self.update_weights(error, mask)  # updates weights for next iteration

    def printtrees(self):
        for tree in self.tree_list:
            print("")
            tree.print_the_tree(tree.tree)

    # predicts the output for one row by getting the prediction from all the trees with their weights, and returning the
    # output with the most (weighted) votes
    def predict_sample(self, sample):
        classes = dict()  # stores every possible answer and its weight
        i = 0

        if len(self.tree_list) == 0:  # check for running in untrained classifier
            print("model does not contain any trees")
            return

        for tree in self.tree_list:  # every tree makes a prediction
            pred = tree.make_prediction(tree.tree, sample)[0]

            if not classes.__contains__(pred):  # if this is the first time seeing this output, add it to the dictionary
                classes[pred] = 0.0

            classes[pred] += self.tree_weight_list[i]  # we add the tree's voting weight

            i += 1

        return max(classes.items(), key=operator.itemgetter(1))[0]  # finds the answer with the maximum weight

    # calculates accuracy of the model
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
