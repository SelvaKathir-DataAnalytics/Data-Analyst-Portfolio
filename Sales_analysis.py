import pandas as pd
import matplotlib.pyplot as plt
# Load the dataset
df = pd.read_csv("sales_data.csv")

# Display first 5 rows
print(df.head())
# Check for missing values
print(df.isnull().sum())

# Get dataset info
print(df.info())

# Get summary statistics
print(df.describe())
sales_per_product = df.groupby("Product")["Total Sales"].sum()
print(sales_per_product)
sales_per_region = df.groupby("Region")["Total Sales"].sum()
print(sales_per_region)
best_selling_product = df.groupby("Product")["Quantity Sold"].sum().idxmax()
print(f"Best-Selling Product: {best_selling_product}")
sales_per_product.plot(kind="bar", title="Total Sales per Product", colormap="viridis")
plt.xlabel("Product")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.show()
sales_per_region.plot(kind="pie", autopct="%1.1f%%", title="Sales Distribution by Region")
plt.ylabel("")
plt.show()
sales_per_product.to_csv("sales_per_product.csv")
sales_per_region.to_csv("sales_per_region.csv")
