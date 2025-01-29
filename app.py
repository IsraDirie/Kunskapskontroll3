import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
import pandas as pd
import seaborn as sns

###1. Läsa in data från en SQL-databas (Load data from an SQL database)
connection = sqlite3.connect("Köksglädje.db")

# Create connection to database file
st.subheader("Products")
products_query = "SELECT * FROM Products;"
products = pd.read_sql(products_query, connection)
products

st.subheader("Stores")
Stores_query = "SELECT * FROM Stores;"
Stores_df = pd.read_sql(Stores_query, connection)
Stores_df

st.subheader("Transactions")
Transactions_query = 'SELECT * FROM [Transactions];'  
Transactions_df = pd.read_sql(Transactions_query, connection)
Transactions_df

st.subheader("Customers")
Customers_query = "SELECT * FROM Customers;"
Customers = pd.read_sql(Customers_query, connection)
Customers

st.subheader("TransactionDetails")
transaction_details_query = "SELECT * FROM TransactionDetails"
transaction_details = pd.read_sql(transaction_details_query, connection)
transaction_details

# Display the data
print(transaction_details.head())
tables_query = "SELECT name FROM sqlite_master WHERE type='table';"
tables_df = pd.read_sql(tables_query, connection)
print(tables_df)

###2. Transformera datan i Pandas 
#Merging Products with transaction_details data
st.subheader("Merging Products with transaction_details data")
df = pd.merge(products, transaction_details, on="ProductID")
df

# Merging transactions with store data
st.subheader("Merging transactions with store data")
df1 = pd.merge(Transactions_df, Stores_df, on="StoreID")
df1

# Grouping and analyzing quantity by product
st.subheader("Grouping and analyzing quantity by product")
df.groupby("ProductName").Quantity.mean()
query = '''SELECT Productname, Price FROM Products
WHERE ProductName = "Kockkniv";'''
print(df)
df . describe()
# To plot boxplots in Streamlit, you must create a Figure object with plt.gcf()
fig = plt.gcf()
# Put the boxplot on the Axes object and plot with st.pyplot()
ax = df.boxplot(figsize = (15,10))
st.pyplot(fig)

# Checking unique values in the dataset
df .nunique()
# Query for sales data
query = """
    SELECT 
        t.TransactionDate, s.StoreName, s.Location, 
        p.ProductName, p.CategoryName, td.Quantity, 
        td.TotalPrice, p.Price, p.CostPrice,
        (td.TotalPrice - (p.CostPrice * td.Quantity)) AS Profit
    FROM TransactionDetails td
    JOIN Products p ON td.ProductID = p.ProductID
    JOIN Transactions t ON td.TransactionID = t.TransactionID
    JOIN Stores s ON t.StoreID = s.StoreID
"""
# Load sales data
sales_data = pd.read_sql_query(query, connection)

# Convert TransactionDate to datetime
sales_data["TransactionDate"] = pd.to_datetime(sales_data["TransactionDate"])

# 1. Total Sales by Store
sales_by_store = sales_data.groupby("StoreName")["TotalPrice"].sum().sort_values(ascending=False)
print("Total Sales by Store:")
print(sales_by_store)

# Visualization of sales by store 
st.header("Total Sales by Store")
st.bar_chart(sales_by_store)

# Using Matplotlib and Seaborn to customize the color (blue)
fig, ax = plt.subplots(figsize=(10, 8))
sns.barplot(x=sales_by_store.index, y=sales_by_store.values, ax=ax, color="blue")

# Customize chart labels
ax.set_title("Total Sales by Store")
ax.set_xlabel("Store Name")
ax.set_ylabel("Total Sales ($)")
plt.xticks(rotation=0)

# 2. Total Sales by Product
sales_by_product = (
    sales_data.groupby("ProductName")["TotalPrice"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.header("Total Sales by Product")
st.bar_chart(sales_by_product)

plt.figure(figsize=(5, 7))
sales_by_product.plot(kind="bar", title="Total Sales by Product", color="blue")
plt.ylabel("Total Sales ($)")
plt.show()

# 3. Total Profit by Category
profit_by_category = (
    sales_data.groupby("CategoryName")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

st.header("Total Profit by Category")

# Seaborn horizontal bar chart with green color
fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(x=profit_by_category.values, y=profit_by_category.index, ax=ax, color="green")

# Customize chart labels
ax.set_title("Total Profit by Category")
ax.set_xlabel("Total Profit ($)")
ax.set_ylabel("Category Name")

# Display the customized plot in Streamlit
st.pyplot(fig)

# Total profit by store
profit_by_store = sales_data.groupby("StoreName")["Profit"].sum().sort_values(ascending=False)

# Display the result in Streamlit
st.write("### Total Profit by Store:")
#st.write(profit_by_store)

# Visualization
fig, ax = plt.subplots(figsize=(10, 8))
profit_by_store.plot(kind="bar", ax=ax, color="darkblue")
ax.set_title("Total Profit by Store")
ax.set_ylabel("Total Profit ($)")

# Show the plot in Streamlit
st.pyplot(fig)


# 4. Monthly Sales Trend Analysis
# Assuming sales_data is already defined and loaded
sales_data["TransactionDate"] = pd.to_datetime(sales_data["TransactionDate"])

# Perform Monthly Sales Trend Analysis  for peak month.
monthly_sales = sales_data.groupby(sales_data["TransactionDate"].dt.to_period("M"))["TotalPrice"].sum()
peak_month = monthly_sales.idxmax()
peak_sales_value = monthly_sales.max()

st.header("Monthly Sales Trend Analysis  for Peak Month")
# Using Matplotlib to create a customized purple line chart
fig, ax = plt.subplots(figsize=(10, 6))
monthly_sales.plot(kind="line", ax=ax, color="purple", marker='o', linewidth=5)
ax.set_title("Monthly Sales Trends")
ax.set_xlabel("Month")
ax.set_ylabel("Total Sales ($)")
ax.axhline(y=peak_sales_value, color='r', linestyle='--', label=f"Peak: {peak_month}")
ax.legend()
ax.grid(True)
# Show the customized chart in Streamlit
st.pyplot(fig)

st.header("Monthly Sales Trends")
# Plot Monthly Sales Trends
fig, ax = plt.subplots(figsize=(10, 6))
monthly_sales.plot(kind="bar", ax=ax, color="skyblue")
ax.set_title("Monthly Sales Trends")
ax.set_xlabel("Month")
ax.set_ylabel("Total Sales ($)")
ax.grid(axis='y')

# Show the customized chart in Streamlit
st.pyplot(fig)

# Plot Monthly Sales Trends
fig, ax = plt.subplots(figsize=(10, 6))
monthly_sales.plot(kind="bar", ax=ax, color="skyblue")
ax.set_title("Monthly Sales Trends")
ax.set_xlabel("Month")
ax.set_ylabel("Total Sales ($)")
ax.grid(axis='y')

#  create a horizontal bar chart showing top-selling products
def top_selling_products(df):
    # Group by ProductName and sum the total sales to get the top-selling products
    top_10_products = df.groupby("ProductName")["TotalPrice"].sum().sort_values(ascending=False).head(10)

    # Display the top-selling products in Streamlit
    st.header("Top 10 Selling Products")
    #st.write(top_10_products)  
    # Create a horizontal bar chart
    fig, ax = plt.subplots(figsize=(8, 6))  
    top_10_products.plot(kind='barh', ax=ax, color='brown')

    # Set chart labels and title
    ax.set_xlabel('Total Sales ($)')
    ax.set_ylabel('Product Name')
    ax.set_title('Top 10 Selling Products')
    ax.grid(True)

    # Display the chart in Streamlit
    st.pyplot(fig)
# Main function to run the Streamlit app
def main():
    # display the top-selling products
    top_selling_products(df)
if __name__ == "__main__":
    main()

# 6. Transaction Details Query Example
transaction_query = """
SELECT transaction_date, transactionID, storeID, customerID
FROM "Transactions"
"""
try:
    transaction = pd.read_sql(transaction_query, connection)
    print("Transaction data retrieved successfully!")
    print(transaction.head())
except Exception as e:
    print(f"An error occurred: {e}")

# 7. Data Cleaning Techniques
# Cleaning column names and handling missing values
sales_data.columns = sales_data.columns.str.strip()
print("Missing Values Count:")
print(sales_data.isnull().sum())

# Forward fill missing values
sales_data.ffill(inplace=True)

# Convert 'TransactionDate' to datetime if not already
if "TransactionDate" in sales_data.columns:
    sales_data["TransactionDate"] = pd.to_datetime(sales_data["TransactionDate"])

# Remove duplicates
sales_data.drop_duplicates(inplace=True)

# 8. Detect Outliers in 'TotalPrice'
if "TotalPrice" in sales_data.columns:
    sns.boxplot(x=sales_data["TotalPrice"])
    plt.title("Outlier Detection in TotalPrice")
    plt.show()

# 9. Customer Segmentation Analysis
# Check for repeat customers
if "CustomerID" in sales_data.columns and "TransactionID" in sales_data.columns:
    repeat_customers = sales_data.groupby("CustomerID")["TransactionID"].count().reset_index()
    repeat_customers.columns = ["CustomerID", "PurchaseCount"]
    repeat_customers["Segment"] = repeat_customers["PurchaseCount"].apply(lambda x: "Repeat" if x > 1 else "New")
    print(repeat_customers.head())

    # Recency-Frequency-Monetary (RFM) Analysis
    sales_data["TransactionDate"] = pd.to_datetime(sales_data["TransactionDate"], errors="coerce")
    rfm = sales_data.groupby("CustomerID").agg({
        "TransactionDate": "max",
        "TransactionID": "count",
        "TotalPrice": "sum"
    }).reset_index()

    rfm.columns = ["CustomerID", "Recency", "Frequency", "Monetary"]
    rfm["Recency"] = (sales_data["TransactionDate"].max() - rfm["Recency"]).dt.days
    print(rfm.head())

    # Plot customer purchase frequency distribution
    plt.title("Customer Purchase Frequency Distribution")
    plt.xlabel("Number of Purchases")
    plt.ylabel("Count of Customers")
    plt.hist(repeat_customers["PurchaseCount"], bins=30)
    plt.show()

# Function to load data from the database
def load_data():
    try:
        connection = sqlite3.connect("Köksglädje.db")

        # Load all necessary tables from the database
        products = pd.read_sql("SELECT * FROM Products", connection)
        stores_df = pd.read_sql("SELECT * FROM Stores", connection)
        transactions_df = pd.read_sql("SELECT * FROM Transactions", connection)
        customers = pd.read_sql("SELECT * FROM Customers", connection)
        transaction_details = pd.read_sql("SELECT * FROM TransactionDetails", connection)

        connection.close()
        return products, stores_df, transactions_df, customers, transaction_details
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None, None, None

# Function to transform data
def transform_data(products, stores, transactions, transaction_details):
    try:
        # Merging transactions with transaction details
        merged_df = pd.merge(transactions, transaction_details, on="TransactionID", how="inner")

        # Merging with products to get product details
        final_df = pd.merge(merged_df, products, on="ProductID", how="inner")

        return final_df, merged_df
    except Exception as e:
        st.error(f"Error transforming data: {e}")
        return None, None

# Function to analyze and visualize data
def analyze_and_visualize(df):
    try:
        

        # Boxplot of numeric columns
        st.write("### Boxplot of Numeric Columns")
        fig, ax = plt.subplots(figsize=(15, 10))
        df.boxplot(ax=ax)
        st.pyplot(fig)

        
    except Exception as e:
        st.error(f"Error during analysis and visualization: {e}")

# Main function to run the Streamlit app
def main():
    # Load data from the database
    products, stores_df, transactions_df, customers, transaction_details = load_data()

    # Ensure data is loaded successfully
    if products is None or stores_df is None or transactions_df is None or transaction_details is None:
        st.error("Failed to load data. Please check the database connection.")
        return

    # Transform data if necessary
    df, df1 = transform_data(products, stores_df, transactions_df, transaction_details)

    # Ensure transformation was successful
    if df is None or df1 is None:
        st.error("Data transformation failed.")
        return

    # Analyze and visualize the data
    analyze_and_visualize(df)

# Run the app
if __name__ == "__main__":
 main()

# Repeat Customer Segmentation
# Load data from the SQLite database
connection = sqlite3.connect("Köksglädje.db")

# Fetch the data from the transactions table
df2 = pd.read_sql("SELECT * FROM transactions", connection)

# Remove spaces from column names
df2.columns = df2.columns.str.strip()

# Check if the required columns exist
if "CustomerID" in df2.columns and "TransactionID" in df2.columns:
    # Group by CustomerID and count the number of transactions (PurchaseCount)
    repeat_customers = df2.groupby("CustomerID")["TransactionID"].count().reset_index()
    repeat_customers.columns = ["CustomerID", "PurchaseCount"]

    # Filter only repeat customers (those with more than one purchase)
    repeat_customers_only = repeat_customers[repeat_customers["PurchaseCount"] > 1]

    # Streamlit app title
    st.title('Repeat Customer Segmentation')
# Plot for Repeat customers
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(repeat_customers_only["CustomerID"], repeat_customers_only["PurchaseCount"], color='lightcoral')
    ax.set_title("Repeat Customers")
    ax.set_xlabel("Customer ID")
    ax.set_ylabel("Number of Purchases")
    ax.tick_params(axis='x', rotation=90)  

    # Display the plot
    plt.tight_layout()
    st.pyplot(fig)
else:
    st.error("The required columns 'CustomerID' or 'TransactionID' are missing.")

# Customer data display
    st.title(" Customers Data")
connection = sqlite3.connect ("Köksglädje.db")
Customers_query = """select CustomerID, JoinDate, ActiveMember, Approvedtocontact from Customers """
 
try:
    df = pd.read_sql(Customers_query, connection)
except Exception as e:
    st.write("Customers tabell doesn't work:",e)
    raise
finally:
    connection.close()
 
if "JoinDate" in df.columns:
    st.write(df['JoinDate'].info())
   
 
    df['JoinDate']=pd.to_datetime(df['JoinDate'],errors='coerce')
   
    radio_button=st.radio("Do i want to see the Graph?", options= ["yes","No"])
 
if radio_button== "yes":
 
    fig, ax= plt.subplots(figsize=(10,5))
   
    ax.set(title='Customers Data Display')
    ax.set_xlabel('JoinDate')
    ax.bar(x=df['JoinDate'],height=df['CustomerID'],color='green')
 
    plt.xticks(rotation=45,ha='right')
    plt.tight_layout()
    st.pyplot(fig)
