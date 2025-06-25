import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('data/ecommerce_data.csv')

# Clean and format
df['Order Date'] = pd.to_datetime(df['Order Date'])

# Group by category
category_summary = df.groupby('Category').agg({
    'Revenue': 'sum',
    'Order ID': pd.Series.nunique
}).rename(columns={'Order ID': 'Unique Orders'}).reset_index()

# Calculate AOV (Average Order Value) per category
category_summary['AOV'] = category_summary['Revenue'] / category_summary['Unique Orders']

print("Category-wise Sales Summary:")
print(category_summary)

# Bar chart for revenue per category
plt.figure(figsize=(8, 4))
plt.barh(category_summary['Category'], category_summary['Revenue'], color='skyblue')
plt.title('Revenue by Category')
plt.xlabel('Revenue')
plt.ylabel('Category')
plt.tight_layout()
plt.show()
