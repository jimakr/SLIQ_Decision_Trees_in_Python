import pandas as pd
from sortedcontainers import SortedList
import numpy as np

def get_data_dictionary(data ,num_cols,len):
    list_data = []
    for index in range(num_cols - 1):
        list = SortedList()  # create list for the attribute, we want it to be sorted
        # print(data.columns[index])
        for i in range(len):  # for each row
            list1 = [data[data.columns[index]].iloc[i], i]  # we use iloc because we need the i row not the i id,
            list.add(list1)                                 # as with random the ids are not consecutive now
        #print(list)
        list_data.append(list)  # add the new list to listed_data
        # print(listed_data[index])

    #create a dictionary for the labels
    dictionary = dict()
    for index in range(len):
        dictionary.update({index: data[data.columns[num_cols - 1]].iloc[index]})


    #print(dictionary)
    return list_data, dictionary


def openthefile(name):
    data = pd.read_csv(name,delimiter = ',', na_values = ['no info', '.'] )
    # print(data.head(5))
    # print(data.columns)
    num_cols= len(data.columns)
    # print(num_cols)

    msk = np.random.rand(len(data)) < 0.9  #split the dataset 90-10 for train and test randomly choosing rows
    train = data[msk]
    test = data[~msk]
    train_len =len(train)
    test_len = len(test)

    #for the training data
    train_data,train_dictionary =  get_data_dictionary(train, num_cols, train_len)

    #for the test data
    test_data, test_dictionary = get_data_dictionary(test,num_cols,test_len)

    return train_data, train_dictionary,test_data, test_dictionary, data.columns

