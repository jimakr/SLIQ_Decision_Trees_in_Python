from anytree import node
from algorithm_u import algorithm_u

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
    gini_a = 1 - float((pos_a*pos_a + neg_a*neg_a)/(n1*n1))
    gini_b = 1 - float((pos_b*pos_b + neg_b*neg_b)/(n2*n2))
    return (n1/n)*gini_a + (n2/n)*gini_b


def split_list(list_a, index):
    right = list_a[index:]
    left = list_a[0:index]
    return left, right


def split_list_descrete(list_a, split):
    #split = [[1,2],[3,4]]
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

    return best_gini, list_a[best_index][0]


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
    for list in dataset:
        leaf_list = [item for item in list if leafset.__contains__(item[1])]  #filter list to contain only leaf items
        if isinstance(list[0][0], str):  #check if list contains discrete attributes or continuous
            temp, split = split_atribute_descrete(leaf_list)
        else:
            temp, split = split_atribute(leaf_list)

        if best > temp:
            best = temp
            best_split = split
        #print(split)
    return best, best_split


def split_leaf(leafset, data, value):
    leftset = {}
    rightset = {}

    for val in data:  #go through the data
        if val[1] in leafset and val[0] < value:   #check if id belongs to left leaf
            leftset.add(val[1])
        elif val[1] in leafset:   #the data is sorted so if the id is in the leafset it belongs to the right leaf
            rightset.add(val[1])

    return leftset, rightset

def train_tree(dataset):
    leaf = {5, 3, 4, 10, 6, 8, 1, 2, 7, 9}
    leaves = [leaf]
    gini , split = choose_split(leaf, dataset)
    root = split
    return root


dataset = [family_data, listed_data]
print(choose_split({5, 3, 4, 10, 6, 8, 1, 2, 7, 9}, dataset))
print(train_tree(dataset))