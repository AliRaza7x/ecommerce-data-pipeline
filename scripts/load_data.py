import pandas as pd
import psycopg2


df = pd.read_csv("C:\\Users\\HP\\OneDrive - KSBL\\Data Engineering\\ecommerce-data-pipeline-project-2\\data\\orders.csv")

print("Rows loaded from CSV:", len(df))

connection = psycopg2.connect(
    host="localhost",
    port=5433,
    database="mydatabase",
    user="admin",
    password="admin123"
)

cursor = connection.cursor()

insert_query = """
INSERT INTO orders_raw
(order_id, customer_id, customer_name, city, product,
 category, quantity, unit_price, order_date)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

for _, row in df.iterrows():

    cursor.execute(
        insert_query,
        (
            int(row["order_id"]),
            int(row["customer_id"]),
            row["customer_name"],
            row["city"],
            row["product"],
            row["category"],
            int(row["quantity"]),
            float(row["unit_price"]),
            row["order_date"]
        )
    )

connection.commit()

cursor.close()
connection.close()

print("Data successfully loaded into PostgreSQL.")