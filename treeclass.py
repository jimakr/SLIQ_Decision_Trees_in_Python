from algorithm_u import algorithm_u
from collections import Counter
from open_file import transformdatatolists


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

    def split_list(self, list_a, split):
        right = list_a[split:]
        left = list_a[0:split]
        return left, right

    def split_list_descrete(self, list_a, split):
        left = []
        right = []
        for item in list_a:
            if split[0].__contains__(item[0]):
                left.append(item)
            else:
                right.append(item)

        return left, right

    def split_atribute(self, list_a):
        last = list_a[0][0]
        index = -1
        best_gini = 2
        best_index = 0
        for item in list_a:
            index += 1
            if item[0] != last:
                last = item[0]
                left, right = self.split_list(list_a, index)
                gini = self.gini_list(left, right, self.dictrid)
                if best_gini > gini:
                    best_gini = gini
                    best_index = index

        return best_gini, list_a[best_index][0]

    def split_atribute_descrete(self, list_a):
        last = list_a[0][0]
        uniques = [last]
        best_gini = 2
        best_split = []
        for item in list_a:
            if item[0] != last:
                last = item[0]
                uniques.append(item[0])

        sets = list(algorithm_u(uniques, 2))

        for split in sets:
            a, b = self.split_list_descrete(list_a, split)
            gini = self.gini_list(a, b, self.dictrid)
            if best_gini > gini:
                best_gini = gini
                best_split = split

        return best_gini, best_split

    def choose_split(self, leafset, dataset):
        best = 2
        best_split = 0
        best_list = []
        column_index = -1
        best_column_index = 0
        for list in dataset:
            column_index += 1
            leaf_list = [item for item in list if leafset.__contains__(item[1])]  # filter list to contain only leaf items
            if isinstance(list[0][0], str):  # check if list contains discrete attributes or continuous
                temp, split = self.split_atribute_descrete(leaf_list)
            else:
                temp, split = self.split_atribute(leaf_list)

            if best > temp:
                best = temp
                best_split = split
                best_column_index = column_index
                best_list = leaf_list
            if temp == 0:
                break
            print("atr")
        left, right = self.split_leaf(best_split, best_list)

        return {'column_split': best_column_index, 'split': best_split, 'left': left, 'right': right}

    def split_leaf(self, split, leaflist):
        if isinstance(leaflist[0][0], str):  # check if list contains discrete attributes or continuous
            left, right = self.split_list_descrete(leaflist, split)
        else:
            left, right = self.split_list(leaflist, [item[0] for item in leaflist].index(split))

        leftset = set([item[1] for item in left])
        rightset = set([item[1] for item in right])
        return leftset, rightset

    def decide_class(self, leafset):
        temp = Counter([self.dictrid[id] for id in leafset])
        present = temp.most_common(1)[0][1]/len(leafset)
        return temp.most_common(1)[0][0], present

    def train_tree(self, minleafexample, similarity_stop):
        leaf = {item for item in range(0,len(self.dictrid))}
        root = self.choose_split(leaf, self.dataset)
        self.unfinished_nodes.append(root)
        while len(self.unfinished_nodes) > 0:
            node = self.unfinished_nodes.pop(0)
            for child in ['left', 'right']:
                if self.decide_class(node[child])[1] < similarity_stop and len(node[child]) > minleafexample:
                    node[child] = self.choose_split(node[child], self.dataset)
                    self.unfinished_nodes.append(node[child])
                else:
                    node[child] = self.decide_class(node[child])
                # if decide_class(node[child])[1] > 0.8:
                #     print('man')
        self.tree = root
        return root

    def make_prediction(self, node, example):
        if not isinstance(node, dict):
            return node
        value = example[node['column_split']]
        if isinstance(value, str):
            if node['split'][0].__contains__(value):
                res = self.make_prediction(node['left'], example)
            else:
                res = self.make_prediction(node['right'], example)
        else:
            if value < node['split']:
                res = self.make_prediction(node['left'], example)
            else:
                res = self.make_prediction(node['right'], example)
        return res

    def print_the_tree(self, node, prefix=''):
        print(prefix[:-2] + "--Split with: " + str(node['split']) + ' at column '+ str(self.columnnames[node['column_split']]))
        prefix = prefix + '|  '
        for child in ['left', 'right']:
            if isinstance(node[child], dict):
                self.print_the_tree(node[child], prefix)
            else:
                print(prefix[:-2] + '--' + str(node[child]))

    def calculate_metrics(self, test_data):
        correct = 0
        for index, row in test_data.iterrows():
            pred = self.make_prediction(self.tree, row)

            if pred[0] == row[-1]:
                correct = correct + 1

        print ("accuracy " + str(correct/len(test_data)))

    def load_dataset(self, dataframe):
        self.dataset, self.dictrid, self.columnnames = transformdatatolists(dataframe)
