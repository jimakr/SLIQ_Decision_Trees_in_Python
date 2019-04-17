from algorithm_u import algorithm_u
from collections import Counter
from open_file import openthefile

listed_data = [[20, 1],
               [20, 3],
               [20, 10],
               [25, 6],
               [25, 8],
               [30, 2],
               [30, 4],
               [30, 7],
               [40, 5],
               [40, 9]]

family_data = [['eggamos', 3],
               ['eggamos', 6],
               ['agamos', 4],
               ['agamos', 5],
               ['agamos', 10],
               ['diazeumenos', 1],
               ['diazeumenos', 2],
               ['diazeumenos', 7],
               ['diazeumenos', 8],
               ['diazeumenos', 9]]

dictrid = {1: 1,
           2: 1,
           3: 0,
           4: 1,
           5: 1,
           6: 0,
           7: 1,
           8: 1,
           9: 1,
           10: 0, }

unfinished_nodes = []

ex = []

def gini_list(list_a, list_b, classlist):
    n1 = len(list_a)
    n2 = len(list_b)

    if n1 == 0 or n2 == 0:
        return 2

    n = n1 + n2
    pos_a = 0.0
    pos_b = 0.0

    for item in list_a:
        if classlist[item[1]] == 1:
            pos_a += 1

    for item in list_b:
        if classlist[item[1]] == 1:
            pos_b += 1

    neg_a = n1 - pos_a
    neg_b = n2 - pos_b
    gini_a = 1 - float((pos_a * pos_a + neg_a * neg_a) / (n1 * n1))
    gini_b = 1 - float((pos_b * pos_b + neg_b * neg_b) / (n2 * n2))
    return (n1 / n) * gini_a + (n2 / n) * gini_b


def split_list(list_a, split):
    right = list_a[split:]
    left = list_a[0:split]
    return left, right


def split_list_descrete(list_a, split):
    left = []
    right = []
    for item in list_a:
        if split[0].__contains__(item[0]):
            left.append(item)
        else:
            right.append(item)

    return left, right


def split_atribute(list_a):
    last = list_a[0][0]
    index = -1
    best_gini = 2
    best_index = 0
    for item in list_a:
        index += 1
        if item[0] != last:
            last = item[0]
            left, right = split_list(list_a, index)
            gini = gini_list(left, right, dictrid)
            if best_gini > gini:
                best_gini = gini
                best_index = index

    return best_gini, list_a[best_index][0]  # list_a[best_index][0]


def split_atribute_descrete(list_a):
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
        a, b = split_list_descrete(list_a, split)
        gini = gini_list(a, b, dictrid)
        if best_gini > gini:
            best_gini = gini
            best_split = split

    return best_gini, best_split


def choose_split(leafset, dataset):
    best = 2
    best_split = 0
    best_list = []
    column_index = -1
    best_column_index = 0
    for list in dataset:
        column_index += 1
        leaf_list = [item for item in list if leafset.__contains__(item[1])]  # filter list to contain only leaf items
        if isinstance(list[0][0], str):  # check if list contains discrete attributes or continuous
            temp, split = split_atribute_descrete(leaf_list)
        else:
            temp, split = split_atribute(leaf_list)

        if best > temp:
            best = temp
            best_split = split
            best_column_index = column_index
            best_list = leaf_list

        # print(split)
    # print(best_list)
    left, right = split_leaf(best_split, best_list)

    return {'column_split': best_column_index, 'split': best_split, 'left': left, 'right': right}


def split_leaf(split, leaflist):
    if isinstance(leaflist[0][0], str):  # check if list contains discrete attributes or continuous
        left, right = split_list_descrete(leaflist, split)
    else:
        left, right = split_list(leaflist, [item[0] for item in leaflist].index(split))

    leftset = set([item[1] for item in left])
    rightset = set([item[1] for item in right])
    return leftset, rightset


def decide_class(leafset):
    temp = Counter([dictrid[id] for id in leafset])
    present = temp.most_common(1)[0][1]/len(leafset)
    return temp.most_common(1)[0][0], present


def train_tree(dataset, minleafexample, similarity_stop):
    leaf = {item for item in range(0,len(dictrid))}
    root = choose_split(leaf, dataset)
    unfinished_nodes.append(root)
    while len(unfinished_nodes) > 0:
        node = unfinished_nodes.pop(0)
        for child in ['left', 'right']:
            if decide_class(node[child])[1] < similarity_stop and len(node[child]) > minleafexample:
                node[child] = choose_split(node[child], dataset)
                unfinished_nodes.append(node[child])
            else:
                node[child] = decide_class(node[child])
            # if decide_class(node[child])[1] > 0.8:
            #     print('man')

    return root


def make_prediction(tree,example):
    if not isinstance(tree, dict):
        return tree
    value = example[tree['column_split']]
    if isinstance(value, str):
        if tree['split'][0].__contains__(value):
            res = make_prediction(tree['left'],example)
        else:
            res = make_prediction(tree['right'],example)
    else:
        if value < tree['split']:
            res = make_prediction(tree['left'],example)
        else:
            res = make_prediction(tree['right'], example)
    return res


def print_the_tree(node, columnnames, prefix = ''):
    print(prefix[:-2] + "--Split with: " + str(node['split']) + ' at column '+ str(columnnames[node['column_split']]))
    prefix = prefix + '|  '
    for child in ['left', 'right']:
        if isinstance(node[child], dict):
            print_the_tree(node[child],columnnames, prefix)
        else:
            print(prefix[:-2] + '--' + str(node[child]))


#dataset = [listed_data, family_data]
dataset, dictrid, columnnames = openthefile('heart.csv')
# print('the dataset is')
# print(dictrid)
# columnnames = list(columnnames)
# print(columnnames)
# leaf = {item for item in range(0,len(dictrid))}
# print(len(leaf))
# print('start trainig')
tree = train_tree(dataset, 5, 0.9)
print_the_tree(tree, columnnames)
ex = [56,1,1,120,236,0,1,178,0,0.8,2,0,2]
print(make_prediction(tree, ex))