listed_data = [[20, 1],
               [20, 3],
               [20, 10],
               [25, 8],
               [20, 6],
               [30, 2],
               [30, 4],
               [30, 7],
               [40, 5],
               [40, 9]]

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
    gini_a = float((pos_a * pos_a + neg_a * neg_a) / (n1 * n1))
    gini_b = float((pos_b * pos_b + neg_b * neg_b) / (n2 * n2))
    return 1 - (n1 / n) * gini_a - (n2 / n) * gini_b


def split_leaf(leafset, data, value):
    leftset = {}
    rightset = {}

    for val in data:  #go through the data
        if val[1] in leafset and val[0] < value:   #check if id belongs to left leaf
            leftset.add(val[1])
        elif val[1] in leafset:   #the data is sorted so if the id is in the leafset it belongs to the right leaf
            rightset.add(val[1])

    return leftset, rightset 


split = gini_list([[30, 2],
                   [30, 4],
                   [30, 7],
                   [40, 5],
                   [40, 9]], [[20, 1],
                              [20, 3],
                              [20, 10],
                              [25, 8],
                              [20, 6]]
                  , dictrid)

print(split)
