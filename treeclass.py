from algorithm_u import algorithm_u
from collections import Counter
from open_file import transformdatatolists
import csv


# the main tree class contains all the values needed and the data to train it
# It implements sth SLIQ decision tree algorithm
class Decisiontree:
    unfinished_nodes = [] # list with nodes that need splitting
    tree = {} # our tree model
    dataset = [] # the transformed data
    dictrid = {} # a dictionary
    columnnames = []

    def gini_list(self, leaflist_left, leaflist_right, classlist):
        n_left = len(leaflist_left)
        n_right = len(leaflist_right)

        if n_left == 0 or n_right == 0:  # check for empty lists
            return 2

        n = n_left + n_right
        positive_left = 0.0
        positive_right = 0.0

        for item in leaflist_left:
            if classlist[item[1]] == 1:
                positive_left += 1

        for item in leaflist_right:
            if classlist[item[1]] == 1:
                positive_right += 1

        neg_a = n_left - positive_left
        neg_b = n_right - positive_right
        gini_a = 1 - float((positive_left * positive_left + neg_a * neg_a) / (n_left * n_left))
        gini_b = 1 - float((positive_right * positive_right + neg_b * neg_b) / (n_right * n_right))
        return (n_left / n) * gini_a + (n_right / n) * gini_b

    # splits the leaflist for an index value
    def split_list(self, leaflist, split):
        right = leaflist[split:]
        left = leaflist[0:split]
        return left, right # returns 2 lists

    # splits the leaflist for two sets of discrete values
    def split_list_descrete(self, leaflist, split):
        left = []
        right = []
        for item in leaflist: #checks every item in list
            if split[0].__contains__(item[0]):  # if it is contained in the left child set
                left.append(item)
            else:
                right.append(item)

        return left, right #returns 2 lists

    # checks the best split for a spesific continuous attribute
    def split_atribute(self, leaflist):
        last = leaflist[0][0]
        index = -1
        best_gini = 2
        best_index = 0
        for value in leaflist: # for every unique value
            index += 1
            if value[0] != last:
                last = value[0]
                left, right = self.split_list(leaflist, index) # splits the list at that value
                gini = self.gini_list(left, right, self.dictrid) # calculates gini index
                if best_gini > gini:  # keeps best gini
                    best_gini = gini
                    best_index = index

        return best_gini, leaflist[best_index][0]

    # check the best split for a specific discrete attribute
    def split_atribute_descrete(self, leaflist):
        last = leaflist[0][0]
        uniques = [last]
        best_gini = 2
        best_split = []
        for item in leaflist: # finds every unique element in list
            if item[0] != last:
                last = item[0]
                uniques.append(item[0])

        #calculate every possible subset and keep it in pairs of lists in a list.
        sets = list(algorithm_u(uniques, 2))

        for split in sets:# for every possible split
            a, b = self.split_list_descrete(leaflist, split) # splits list
            gini = self.gini_list(a, b, self.dictrid) #calculates gini
            if best_gini > gini: #keeps best gini
                best_gini = gini
                best_split = split

        return best_gini, best_split

    #checks best splits in every attribute and keeps the best
    def choose_split(self, leafset, dataset):
        best = 2
        best_split = 0
        best_list = []
        column_index = -1
        best_column_index = 0
        for list in dataset: # for every attribute
            column_index += 1
            # filter list to contain only this leaf items
            leaf_list = [item for item in list if leafset.__contains__(item[1])]

            if isinstance(list[0][0], str):  # check if list contains discrete attributes or continuous
                temp, split = self.split_atribute_descrete(leaf_list)
            else:
                temp, split = self.split_atribute(leaf_list)

            if best > temp: # keeps the best split
                best = temp
                best_split = split
                best_column_index = column_index
                best_list = leaf_list
            if temp == 0: # gini lowest value is 0 so we don't have to check any more
                break
        left, right = self.split_leaf(best_split, best_list) # splits the node

        # makes it from a set of ids to a new node
        return {'column_split': best_column_index, 'split': best_split, 'left': left, 'right': right}

    def split_leaf(self, split, leaflist):
        if isinstance(leaflist[0][0], str):  # check if list contains discrete attributes or continuous
            left, right = self.split_list_descrete(leaflist, split)
        else:
            left, right = self.split_list(leaflist, [item[0] for item in leaflist].index(split))

        leftset = set([item[1] for item in left])
        rightset = set([item[1] for item in right])
        return leftset, rightset

    # gets the set of data and finds the most common class , returns the class and its frequency
    def decide_class(self, leafset):
        temp = Counter([self.dictrid[id] for id in leafset])
        present = temp.most_common(1)[0][1]/len(leafset)
        return temp.most_common(1)[0][0], present

    # trains the tree and takes as input minimum number of childer and similariry of class in leaf in order to split it
    def train_tree(self, minleafexample, similarity_stop):
        leaf = {item for item in range(0,len(self.dictrid))} # creates the first set containing every item id
        root = self.choose_split(leaf, self.dataset) #makes first split
        self.unfinished_nodes.append(root) # inserts it into list
        while len(self.unfinished_nodes) > 0:
            node = self.unfinished_nodes.pop(0)
            for child in ['left', 'right']: # for it's child lists
                if self.decide_class(node[child])[1] < similarity_stop and len(node[child]) > minleafexample: #checks condition
                    node[child] = self.choose_split(node[child], self.dataset) #splits the child
                    self.unfinished_nodes.append(node[child])
                else:
                    node[child] = self.decide_class(node[child])
        self.tree = root
        return root

    # takes a row of data and predicts the label using the decision tree
    def make_prediction(self, node, example):
        if not isinstance(node, dict):  # if we have reached a decision for the label return it
            return node
        value = example[node['column_split']]  # column_split has the attribute used to split at that point
        if isinstance(value, str):    # checks if the attribute contains strings- discrete values
            if node['split'][0].__contains__(value):  # check if the attribute value belongs the set of the left child
                res = self.make_prediction(node['left'], example)
            else:
                res = self.make_prediction(node['right'], example)
        else:                         #checks for numeric values
            if value < node['split']:
                res = self.make_prediction(node['left'], example)
            else:
                res = self.make_prediction(node['right'], example)
        return res

    # prints the decision tree
    def print_the_tree(self, node, prefix=''):
        print(prefix[:-2] + "--Split with: " + str(node['split']) + ' at column '+ str(self.columnnames[node['column_split']]))
        prefix = prefix + '|  '
        for child in ['left', 'right']:
            if isinstance(node[child], dict): #
                self.print_the_tree(node[child], prefix)
            else:
                print(prefix[:-2] + '--' + str(node[child]))

    # gets the predictions for the dataset given and calculates the accuracy
    def calculate_metrics(self, test_data):
        correct = 0
        for index, row in test_data.iterrows():
            pred = self.make_prediction(self.tree, row) # get prediction for the row

            if pred[0] == row[-1]:
                correct = correct + 1

        print ("accuracy " + str(correct/len(test_data)))

    # saves the data we need to train the tree
    def load_dataset(self, dataframe):
        self.dataset, self.dictrid, self.columnnames = transformdatatolists(dataframe)

    # creates an output file to store the predictions from the given data
    def make_output_file(self, test_data):
        with open('output.csv', 'w', newline='') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            for index, row in test_data.iterrows():
                pred = self.make_prediction(self.tree, row)
                wr.writerow([pred[0]])
        myfile.close()
        return myfile
