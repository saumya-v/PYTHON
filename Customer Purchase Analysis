# Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Create dummy data
np.random.seed(42)
n = 1000

data = pd.DataFrame({
    'Customer_ID': np.random.choice([f'CUST_{i}' for i in range(100)], size=n),
    'Date': pd.to_datetime(np.random.choice(pd.date_range('2023-01-01', '2023-12-31'), size=n)),
    'Product_Category': np.random.choice(['Pet Food', 'Grooming', 'Vet Visit', 'Accessories'], size=n),
    'Order_Amount': np.random.randint(100, 5000, size=n),
    'City': np.random.choice(['Delhi', 'Mumbai', 'Bengaluru', 'Hyderabad', 'Pune'], size=n)
})

# Overview
print(data.head())
print("\nMissing values:\n", data.isnull().sum())
print("\nData Summary:\n", data.describe())

# Monthly Revenue
data['Month'] = data['Date'].dt.to_period('M')
monthly_revenue = data.groupby('Month')['Order_Amount'].sum()

plt.figure(figsize=(10,5))
monthly_revenue.plot(marker='o')
plt.title('Monthly Revenue')
plt.ylabel('Revenue')
plt.xlabel('Month')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# New vs. Repeat Customers
first_purchase = data.groupby('Customer_ID')['Date'].min().reset_index()
first_purchase.columns = ['Customer_ID', 'First_Purchase_Date']
data = data.merge(first_purchase, on='Customer_ID')
data['Is_New'] = data['Date'] == data['First_Purchase_Date']
customer_counts = data['Is_New'].value_counts()

plt.figure(figsize=(5,5))
plt.pie(customer_counts, labels=['Repeat', 'New'], autopct='%1.1f%%', colors=['#66b3ff','#99ff99'])
plt.title('New vs. Repeat Transactions')
plt.show()

# AOV (Average Order Value)
aov = data.groupby('Customer_ID')['Order_Amount'].mean().sort_values(ascending=False).head(10)
print("Top 10 customers by AOV:")
print(aov)

# Top Cities by Revenue
top_cities = data.groupby('City')['Order_Amount'].sum().sort_values(ascending=False)

plt.figure(figsize=(8,4))
sns.barplot(x=top_cities.index, y=top_cities.values, palette='viridis')
plt.title('Revenue by City')
plt.ylabel('Revenue')
plt.xlabel('City')
plt.tight_layout()
plt.show()

# Product Category Revenue
category_revenue = data.groupby('Product_Category')['Order_Amount'].sum().sort_values(ascending=False)

plt.figure(figsize=(6,4))
sns.barplot(x=category_revenue.values, y=category_revenue.index, palette='magma')
plt.title('Revenue by Product Category')
plt.xlabel('Revenue')
plt.ylabel('Product Category')
plt.tight_layout()
plt.show()
