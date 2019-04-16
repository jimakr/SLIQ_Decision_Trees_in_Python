import pandas as pd


data = pd.read_csv('data-discrete.csv',delimiter = ';',skiprows = 1, na_values = ['no info', '.'],names= ['country', 'sex', 'age', 'suicides_no', 'generation'] )
print(data.head(5))
print(data.columns)

print(data['suicides_no'].dtypes)
print(data['age'].dtypes)


list_age = []
for i in range(len(data['age'])):
    list1 = [data['age'][i],i+1]
    list.append(list1)
print(list)

