import pandas as pd
from sortedcontainers import SortedList


def openthefile(name):
    data = pd.read_csv(name,delimiter = ',', na_values = ['no info', '.'] )
    # print(data.head(5))
    # print(data.columns)
    num_cols= len(data.columns)
    # print(num_cols)

    listed_data = []
    for index in range(num_cols-2):
        list = SortedList()   #create list for the attribute
        # print(data.columns[index])
        for i in range(len(data[data.columns[index]])):  #for each row
            list1 = [data[data.columns[index]][i], i]
            list.add(list1)
        # print(list)
        listed_data.append(list) #add the new list to listed_data
        #print(listed_data[index])

    dictionary = dict()
    for index in range(len(data[data.columns[num_cols-1]])):
        dictionary.update({index: data[data.columns[num_cols-1]][index]})

    #print(dictionary)
    return listed_data, dictionary, data.columns