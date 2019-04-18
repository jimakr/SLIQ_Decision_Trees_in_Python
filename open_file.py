from sortedcontainers import SortedList
import pandas as pd


def openthefile(name):
    data = pd.read_csv(name, delimiter=',', na_values= ['no info', '.'])
    num_cols = len(data.columns)
    length = len(data)
    listed_data = []
    for index in range(num_cols - 1):
        attribute_list = SortedList()  # create list for the attribute, we want it to be sorted
        for i in range(length):
            list1 = [data[data.columns[index]][i], i]
            attribute_list.add(list1)
        listed_data.append(attribute_list)  # add the new list to listed_data

    # create a dictionary for the labels
    dictionary = dict()
    for index in range(length):
        dictionary.update({index: data[data.columns[num_cols - 1]].iloc[index]})

    # print(dictionary)

    return listed_data, dictionary, data.columns
