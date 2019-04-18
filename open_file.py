from sortedcontainers import SortedList

# this function transforms the data from dataframe to a list.
# This contains lists for the attributes(one list for each) with the id and value of every row (sorted using the values)
def openthefile(data):

    num_cols = len(data.columns)
    length = len(data)
    listed_data = []
    for index in range(num_cols - 1):
        attribute_list = SortedList()  # create list for the attribute, we want it to be sorted
        for i in range(length):
            list1 = [data[data.columns[index]].iloc[i], i]
            attribute_list.add(list1)
        listed_data.append(attribute_list)  # add the new list to listed_data

    # create a dictionary for the labels
    dictionary = dict()
    for index in range(length):
        dictionary.update({index: data[data.columns[num_cols - 1]].iloc[index]})

    return listed_data, dictionary, data.columns
