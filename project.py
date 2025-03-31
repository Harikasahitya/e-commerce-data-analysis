import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

file_path = 'data.csv'  
data = pd.read_csv(file_path, encoding='ISO-8859-1')

print("Dataset Preview:")
print(data.head())
print(data.info())

data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])

data.dropna(subset=['CustomerID', 'Description'], inplace=True)


data['TotalPrice'] = data['Quantity'] * data['UnitPrice']


sales_trends = data.groupby(data['InvoiceDate'].dt.to_period('M'))['TotalPrice'].sum()

plt.figure(figsize=(10, 6))
sales_trends.plot(kind='line', marker='o', color='blue')
plt.title('Sales Trends Over Time')
plt.xlabel('Month')
plt.ylabel('Total Sales')
plt.grid()
plt.show()

top_products = data.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(10, 6))
top_products.plot(kind='bar', color='orange')
plt.title('Top 10 Best-Selling Products')
plt.xlabel('Product Description')
plt.ylabel('Total Quantity Sold')
plt.xticks(rotation=45)
plt.show()
region_sales = data.groupby('Country')['TotalPrice'].sum().sort_values(ascending=False)

plt.figure(figsize=(10, 6))
region_sales.head(10).plot(kind='bar', color='green')
plt.title('Top 10 Regions by Sales')
plt.xlabel('Country')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.show()

correlation = data['Quantity'].corr(data['UnitPrice'])
print(f"Correlation between Quantity and UnitPrice: {correlation:.2f}")
sns.scatterplot(x=data['UnitPrice'], y=data['Quantity'], alpha=0.6)
plt.title('Quantity vs. UnitPrice')
plt.xlabel('UnitPrice')
plt.ylabel('Quantity')
plt.show()

#
customer_sales = data.groupby('CustomerID')['TotalPrice'].sum()

bins = [0, 500, 2000, 5000, np.inf]
labels = ['Low Spenders', 'Mid Spenders', 'High Spenders', 'Top Spenders']
customer_segments = pd.cut(customer_sales, bins=bins, labels=labels)

segment_counts = customer_segments.value_counts()

plt.figure(figsize=(8, 6))
segment_counts.plot(kind='bar', color='purple')
plt.title('Customer Segmentation')
plt.xlabel('Segment')
plt.ylabel('Number of Customers')
plt.show()

print("Key Insights:")
print("1. Sales trends show peak sales during specific months.")
print("2. Top-selling products should be prioritized in inventory.")
print("3. Regional analysis highlights high-performing markets.")
print("4. Pricing strategy can be optimized based on price-quantity correlations.")
print("5. Customer segmentation reveals opportunities for targeted marketing.")

data.to_csv('cleaned_ecommerce_data.csv', index=False)
print("Cleaned data saved as 'cleaned_ecommerce_data.csv'")