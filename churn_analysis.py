import sqlite3
import pandas as pd

# Step 1: Load the CSV into Pandas
df = pd.read_csv("customer_churn_data.csv")

# Step 2: Connect to SQLite database (or create it)
conn = sqlite3.connect("customer_churn.db")
cursor = conn.cursor()

# Step 3: Create the customer churn table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS customer_churn (
        Customer_ID INTEGER PRIMARY KEY,
        Region TEXT,
        Subscription_Type TEXT,
        Monthly_Spend INTEGER,
        Total_Purchases INTEGER,
        Churn TEXT
    )
''')

# Step 4: Insert the CSV data into the database
df.to_sql("customer_churn", conn, if_exists="replace", index=False)

print("✅ Data successfully loaded into SQLite!")

# Step 5: Run SQL queries and analyze data

# Query 1: Total Customers by Region
query1 = "SELECT Region, COUNT(*) AS Total_Customers FROM customer_churn GROUP BY Region;"
df_q1 = pd.read_sql(query1, conn)
df_q1.to_csv("total_customers_by_region.csv", index=False)

# Query 2: Churn Rate by Subscription Type
query2 = """
SELECT Subscription_Type, 
       COUNT(CASE WHEN Churn = 'Yes' THEN 1 END) * 100.0 / COUNT(*) AS Churn_Rate
FROM customer_churn
GROUP BY Subscription_Type;
"""
df_q2 = pd.read_sql(query2, conn)
df_q2.to_csv("churn_rate_by_subscription.csv", index=False)

# Query 3: Average Monthly Spend for Churned vs Non-Churned Customers
query3 = "SELECT Churn, AVG(Monthly_Spend) AS Avg_Spend FROM customer_churn GROUP BY Churn;"
df_q3 = pd.read_sql(query3, conn)
df_q3.to_csv("avg_spend_churn_vs_nonchurn.csv", index=False)

# Query 4: Top 5 Highest-Spending Customers
query4 = "SELECT * FROM customer_churn ORDER BY Monthly_Spend DESC LIMIT 5;"
df_q4 = pd.read_sql(query4, conn)
df_q4.to_csv("top_5_highest_spending_customers.csv", index=False)

# Query 5: Customers with High Purchases but Still Churned
query5 = """
SELECT * FROM customer_churn
WHERE Churn = 'Yes' 
AND Total_Purchases > (SELECT AVG(Total_Purchases) FROM customer_churn);
"""
df_q5 = pd.read_sql(query5, conn)
df_q5.to_csv("high_purchases_but_churned.csv", index=False)

print("✅ SQL Analysis Completed & Results Saved as CSV!")

# Step 6: Close the database connection
conn.close()
