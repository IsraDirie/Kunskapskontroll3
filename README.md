Köksglädje

our project is about how to analys, transform and read data
In this project it has five tables where one is customers , products , transactions, transactionDetails , stores.
In customers there are four columns one is active member, the other is approved to contact, join date and last one is customer id.
The next tabel which the name of it is product has six columns where one is productId , productname, descriptions, categoryname, price, costprice.
the third tabel is stores where the columns are storeId, store names and last one is location
the fourth is transaction details where one columns  are transactiondetaileid, transactionId, productid , quantity, price at purchase, total price
Last but not least is the transaction tabel which the columns begins with transactionid , storeid, customerid and the last one is transaction date.
if you want to check it you can find it in this database here just click on the repository ("Köksglädje.db"). What we used is Api scheduling time where we laid our project by creating, updating and deleting and improving.

Here is one of the koding where i was very proud of doing

connection = sqlite3.connect (r"C:\Users\israd\Data science\Köksglädje.db")

query = """select Stores.StoreName,TransactionDetails.Totalprice
from Stores
Join TransactionDetails on Stores.StoreID = TransactionDetails.TransactionID """

try:
    df = pd.read_sql(query, connection)
    print(" Stores on go!")
except Exception as e:
    print ("Data doesn't work:",e)
    raise
finally:
        connection.close()
if "StoreName" in df.columns and "TotalPrice" in df.columns:
     df['TotalPrice'] = df['TotalPrice'].astype(float)
   
     print("Stores is working")
     print("StoreName info:")
     print(df["StoreName"].info())
else:
    print('Data is not working')
    print(df.head())
   
fig, ax = plt.subplots(figsize=(10,5))
df.plot(
x='StoreName',
y='TotalPrice',
kind='bar',
title='Stores',
ax=ax,
color='green'
)

plt.xticks(rotation=45, ha= 'right')
plt.yticks()
plt.tight_layout()
plt.show()

print(df.head())
print(df.info())  

what the graph is about how to analys Stores Names and Total price. What you need to install for this project are (import streamlit as st ,import numpy as np,import matplotlib.pyplot as plt, import sqlite3, import pandas as pd, import seaborn as sns ) and make sure you do this so your koding can work.




