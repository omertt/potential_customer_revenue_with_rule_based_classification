#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
df = pd.read_csv("persona.csv")


# **DATA EXPLORATION**

# In[2]:


df.shape


# In[3]:


df.info()


# In[4]:


df.describe()


# **Number of unique source**

# In[5]:


df["SOURCE"].nunique()


# **Frequency of source**

# In[6]:


df["SOURCE"].value_counts()


# **Number of unique price**

# In[7]:


df["PRICE"].nunique()


# **Number of sales by price**

# In[8]:


df["PRICE"].value_counts()


# **Number of sales by country**

# In[9]:


df["COUNTRY"].value_counts()


# **Total earned revenue from sales by country**

# In[10]:


df.groupby("COUNTRY").agg({"PRICE" : "sum"})


# **Number of sales by source types**

# In[11]:


df.groupby("SOURCE").agg({"PRICE" : "count"})


# **Price averages by country**

# In[12]:


df.groupby("COUNTRY").agg({"PRICE" : "mean"})


# **Price averages by sources**

# In[13]:


df.groupby("SOURCE").agg({"PRICE" : "mean"})


# **Price averages by Country and Source**

# In[14]:


df.groupby(["COUNTRY", "SOURCE"]).agg({"PRICE" : "mean"})


# **Average earnings by Country, Source, Sex and Age**

# In[15]:


df.groupby(["COUNTRY","SOURCE","SEX","AGE"]).agg({"PRICE" : "mean"})


# **The previous output is sorted in descending order of price. The result is saved as agg_df.**

# In[16]:


agg_df = df.groupby(["COUNTRY","SOURCE","SEX","AGE"]).agg({"PRICE" : "mean"}).sort_values(by = "PRICE", ascending = False)

agg_df


# **The indexes have been converted to variables and the changes have been made permanent with the inplace method.**

# In[17]:


agg_df.reset_index(["COUNTRY","SOURCE","SEX","AGE"],inplace = True)

agg_df


# **The numeric variable age was converted to a categorical variable. Then the ranges were created.**

# In[18]:


agg_df["AGE_CAT"] = agg_df["AGE"].astype("category")

agg_df["AGE_CAT"] = pd.cut(agg_df.AGE_CAT,[0,18,23,30,40,70],labels = ['0_18', '19_23', '24_30', '31_40', '41_70'])

agg_df


# **A variable named customer_level_based has been created and added to the dataset. Since there can be more than one of the same expression, singularization has been made with the groupby method.**

# In[19]:


agg_df["customers_level_based"] = [col[0].upper() + "_" + col[1].upper() + "_" + col[2].upper() + "_" + col[5] for col in agg_df.values]

agg_df = agg_df.groupby("customers_level_based").agg({"PRICE" : "mean"})

agg_df


# **Price values ​​are segmented and the Segment variable is added to the dataset.**

# In[20]:


agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"],4, labels = ["D","C","B","A"])

agg_df.groupby("SEGMENT").agg({"PRICE" : ["mean","max","sum"]})

agg_df = agg_df.reset_index()

agg_df


# **A function has been created to see the revenue that potential customers can bring and to find the segment.**

# In[21]:


def find_segment():
    COUNTRY = input("Enter the country (USA / BRA / DEU / TUR / FRA / CAN): ")
    SOURCE = input("Enter the source (ANDROID / IOS): ")
    SEX = input("Enter the sex (MALE / FEMALE): ")
    AGE = int(input("Enter the age: "))
    if AGE < 19:
        AGE = "0_18"
    elif AGE > 18 and AGE < 24:
        AGE = "19_23"
    elif AGE > 23 and AGE < 31:
        AGE = "24_30"
    elif AGE > 30 and AGE < 41:
        AGE = "31_40"
    else:
        AGE = "41_70"
    new_user = COUNTRY + "_" + SOURCE + "_" + SEX + "_" + AGE
    print(agg_df[agg_df["customers_level_based"] == new_user])


# In[ ]:


find_segment()

