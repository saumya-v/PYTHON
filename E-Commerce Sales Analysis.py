# Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import timedelta

# Create synthetic dataset
np.random.seed(42)

n = 3000
customer_ids = [f"CUST_{i}" for i in range(1, 401)]
products = ['Laptop', 'Smartphone', 'Headphones', 'Camera', 'Tablet']
categories = ['Electronics', 'Accessories']
cities = ['Delhi', 'Mumbai', 'Bengaluru', 'Chennai', 'Hyderabad']
start_date = pd.to_datetime("2023-01-01")

data = pd.DataFrame({
    'Order_ID': [f"ORD_{i}" for i in range(1, n+1)],
    'Customer_ID': np.random.choice(customer_ids, size=n),
    'Order_Date': [start_date + timedelta(days=int(x)) for x in np.random.uniform(0, 364, size=n)],
    'Product': np.random.choice(products, size=n),
    'Category': np.random.choice(categories, size=n),
    'Revenue': np.random.randint(500, 50000, size=n),
    'City': np.random.choice(cities, size=n)
})

# Save to CSV (optional)
# data.to_csv("ecommerce_data.csv", index=False)

#  Quick Look
print(data.head())
print(data.describe())

# Monthly Sales Trend
data['Month'] = data['Order_Date'].dt.to_period('M')
monthly_sales = data.groupby('Month')['Revenue'].sum()

plt.figure(figsize=(10,5))
monthly_sales.plot(marker='o')
plt.title('Monthly Revenue Trend')
plt.xlabel('Month')
plt.ylabel('Revenue')
plt.grid()
plt.tight_layout()
plt.show()

#Revenue by Product
top_products = data.groupby('Product')['Revenue'].sum().sort_values(ascending=False)

plt.figure(figsize=(8,4))
sns.barplot(x=top_products.index, y=top_products.values, palette='cubehelix')
plt.title('Revenue by Product')
plt.ylabel('Revenue')
plt.xlabel('Product')
plt.tight_layout()
plt.show()

#  Category Performance
cat_sales = data.groupby('Category')['Revenue'].sum()

plt.figure(figsize=(6,4))
cat_sales.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['#66c2a5', '#fc8d62'])
plt.title('Sales Share by Category')
plt.ylabel('')
plt.tight_layout()
plt.show()

#Revenue by City
city_sales = data.groupby('City')['Revenue'].sum().sort_values(ascending=False)

plt.figure(figsize=(8,4))
sns.barplot(x=city_sales.index, y=city_sales.values, palette='viridis')
plt.title('Revenue by City')
plt.ylabel('Revenue')
plt.xlabel('City')
plt.tight_layout()
plt.show()

#Top Customers
top_customers = data.groupby('Customer_ID')['Revenue'].sum().sort_values(ascending=False).head(10)
print("\nTop 10 Customers by Revenue:")
print(top_customers)

Average Order Value (AOV)
aov = data['Revenue'].mean()
print(f"\nAverage Order Value (AOV): ₹{aov:.2f}")

# RFM Segmentation (basic)
snapshot_date = data['Order_Date'].max() + timedelta(days=1)
rfm = data.groupby('Customer_ID').agg({
    'Order_Date': lambda x: (snapshot_date - x.max()).days,
    'Order_ID': 'count',
    'Revenue': 'sum'
})
rfm.columns = ['Recency', 'Frequency', 'Monetary']

# Quantile segmentation
rfm['R'] = pd.qcut(rfm['Recency'], 4, labels=[4,3,2,1])
rfm['F'] = pd.qcut(rfm['Frequency'].rank(method='first'), 4, labels=[1,2,3,4])
rfm['M'] = pd.qcut(rfm['Monetary'], 4, labels=[1,2,3,4])
rfm['RFM_Score'] = rfm[['R','F','M']].astype(str).sum(axis=1)

print("\nSample RFM Table:")
print(rfm.head())

#Segment Customers
def segment(rfm_score):
    if rfm_score == '444':
        return 'Champions'
    elif rfm_score.startswith('4'):
        return 'Loyal Customers'
    elif rfm_score.endswith('4'):
        return 'Big Spenders'
    else:
        return 'Others'

rfm['Segment'] = rfm['RFM_Score'].apply(segment)
seg_counts = rfm['Segment'].value_counts()

plt.figure(figsize=(6,4))
sns.barplot(x=seg_counts.index, y=seg_counts.values, palette='coolwarm')
plt.title('Customer Segments')
plt.ylabel('Count')
plt.xlabel('Segment')
plt.tight_layout()
plt.show()
