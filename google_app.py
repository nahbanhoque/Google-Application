#!/usr/bin/env python
# coding: utf-8

# In[83]:


import numpy as np
import pandas as pd
from pandas import Series
from pandas import DataFrame
from numpy import nan as NA
from matplotlib import pyplot as plt
from matplotlib import cm


# **Load file into Pandas DataFrame**

# In[84]:


google = pd.read_excel('GooglePlaystore.xlsx')
google


# # Preprocessing (28 pts)

# **Task 1: [3 pts] Often there are outliers which do not match the overall data type. There is one record in this data where the "Reviews" has value "3.0M" which does not match the rest of the data. Remove that record.**

# In[85]:


index_drop = google[google['Reviews'] == '3.0M'].index[0] # Index of row that needs to be dropped
google = google.drop(index_drop, axis=0)
# Converting Reviews column to ints for analysis later on
def make_reviews_int(c):
    return int(c)
google['Reviews'] = google['Reviews'].apply(make_reviews_int)
# Now there are 10840 rows instead of 10841
google.info()




# In[86]:


rows_2_delete = []
for row in google.iterrows():
    if 'Varies with device' in row[1].values:
        rows_2_delete.append(row[0]) # Adding index of row to delete
google = google.drop(rows_2_delete, axis=0)
# Now there are 9059 rows instead of 10840 (1781 removed)
google.info()



# In[87]:


import re
def change_android(c):
    if str(c) == 'nan':
        return c
    c = c.strip(' and up')
    is_hyphen = c.find('-')
    
    # Takes care of ranges (i.e. 4.0-9.0)
    if is_hyphen != -1:
        c = c[:is_hyphen-1]
    if c.count('.') >= 2: # More than one decimal place
        first_decimal = c.find('.')
        second_decimal = c[first_decimal+1:].find('.')
        c = c[:second_decimal]
    # Removes any non-numeric characters
    c = re.sub('[A-Za-z]','',c)
    return float(c)
google['Android Ver'] = google['Android Ver'].apply(change_android)
google['Android Ver']



# In[88]:


# Removing commas and plus signs
def change_installs(c):
    c = re.sub('[+,]','',c)
    return c
google['Installs'] = google['Installs'].apply(change_installs)

# Seeing if any 'Installs' vals are not ints after edits
lst = []
for index in google['Installs'].index:
    val = google.loc[index,'Installs']
    if re.search('[^0-9]',val):
        lst.append(index)

# Only remove rows if there's any in lst
if len(lst) != 0:
    google = google.drop(lst, axis=0)

# Converting 'Installs' vals to ints for later analysis
def make_installs_int(c):
    return int(c)
google['Installs'] = google['Installs'].apply(make_installs_int)

# No rows were removed, still 9059 rows
google['Installs']



# In[89]:


null_rating = google[google['Rating'].isnull()]
rows_2_delete = []
for index in null_rating.index:
    num_reviews = null_rating.loc[index,'Reviews']
    num_installs = null_rating.loc[index,'Installs']
    if num_reviews<100 and int(num_installs)<50000:
        rows_2_delete.append(index)
    else:
        category = null_rating.loc[index,'Category']
        cat_df = google[google['Category']==category]
        avg = round(cat_df['Rating'].mean(),2)
        google.loc[index,'Rating'] = avg
if len(rows_2_delete) != 0:
    google = google.drop(rows_2_delete, axis=0)
# Showing only first 25 rows, NaNs are filled in
# Many rows have been removed (now 7685 instead of 9059)
google['Rating'].head(25)



# In[90]:


import math
def convert_size(c):
    ending = c[-1] # either 'K' or 'M'
    number = float(c[:-1])
    if ending=='K' or ending=='k':
        number *= math.pow(10,3)
        return int(number)
    elif ending=='M' or ending=='m':
        number *= math.pow(10,6)
        return int(number)
    return int(number)
google['Size'] = google['Size'].apply(convert_size)
# Size column has been converted
google['Size']






# In[91]:


google.groupby(['Category','Rating']).describe()



# In[92]:


def top_free_apps(c):
    df = free_apps.groupby('Category')[c.name].nlargest(3).reset_index(level=1)
    indexes = df['level_1'].values
    app_names = []
    for index in indexes:
        app_names.append(free_apps.loc[index,'App'])
    df['level_1'] = app_names
    df_new = df.rename(columns={'level_1':'App'})
    return df_new

free_apps = google[google['Type']=='Free']
free_apps


# a. Rating (gives top 3 most highly rated applications in each category)

# In[93]:


df = top_free_apps(free_apps['Rating'])
df


# b. Installs (gives top 3 most installed applications in each category)

# In[94]:


df2 = top_free_apps(free_apps['Installs'])
df2


# c. Reviews (gives top 3 most reviewed applications in each category)

# In[95]:


df3 = top_free_apps(free_apps['Reviews'])
df3


# **Task 3: [4 pts] Find the average, maximum and minimum price of the paid applications.**

# In[96]:


paid_apps = google[google['Type']!='Free']
print('Average price of paid applications is $' + str(round(paid_apps['Price'].mean(),2)))
print('Maximum price of paid applications is $' + str(paid_apps['Price'].max()))
print('Minimum price of paid applications is $' + str(paid_apps['Price'].min()))



# #### 1. Number of Applications per genre

# In[97]:


google['Genres'] = google['Genres'].str.split(';')
google['Genres']


# In[100]:


google = google.explode("Genres")


# In[111]:


n = google["Genres"].value_counts().reset_index().values

plt.pie(n[:,1], labels=n[:,0])

plt.title("Genre Pie Chart")

plt.legend(bbox_to_anchor=(1.05,1),ncol=4,fancybox=True,shadow=False)

plt.show()


# In[ ]:






# In[114]:


google[(google["Category"]=="EDUCATION") | (google["Category"]=="BUSINESS")].boxplot(column="Rating",by="Category")


# In[ ]:




