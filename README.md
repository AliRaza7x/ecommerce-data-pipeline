# E-Commerce Data Engineering Pipeline

A beginner-friendly Data Engineering project demonstrating data ingestion, data validation, PostgreSQL database management, SQL analytics, and query optimization using Python, Pandas, PostgreSQL, and Docker.

---

## Project Overview

This project implements a small end-to-end data pipeline for an e-commerce dataset.

The pipeline takes order data from a CSV file, loads it into PostgreSQL using Python, performs data quality checks, applies database constraints, and performs analytical queries.

The project also demonstrates PostgreSQL concepts such as indexes, transactions, views, materialized views, `EXPLAIN ANALYZE`, and performance optimization.

### Pipeline

```text
orders.csv
    ↓
Python + Pandas
    ↓
PostgreSQL
    ↓
Raw Data Table
    ↓
Data Quality Checks
    ↓
Clean Data Table
    ↓
SQL Analytics
    ↓
Views & Materialized Views
    ↓
Indexes & Query Optimization
```

---

## Objectives

The main objectives of this project are:

- Practice building a basic Data Engineering pipeline
- Load CSV data into PostgreSQL using Python
- Perform data quality checks
- Apply database constraints
- Perform analytical queries using SQL
- Create PostgreSQL views and materialized views
- Create and use indexes
- Analyze query performance using `EXPLAIN ANALYZE`
- Practice PostgreSQL transactions
- Run PostgreSQL using Docker
- Organize a Data Engineering project using Git and GitHub

---

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Data ingestion |
| Pandas | Reading and processing CSV data |
| PostgreSQL | Relational database |
| SQL | Data transformation and analysis |
| Docker | Running PostgreSQL |
| psycopg2 | Python-PostgreSQL connection |
| Git | Version control |
| GitHub | Project repository |

---

## Project Structure

```text
ecommerce-data-pipeline/
│
├── data/
│   └── orders.csv
│
├── scripts/
│   └── load_data.py
│
├── sql/
│   ├── create_tables.sql
│   ├── analysis.sql
│   └── views.sql
│
├── logs/
│
└── README.md
```

---

## Dataset

The project uses an e-commerce orders dataset containing:

- Order ID
- Customer ID
- Customer Name
- City
- Product
- Category
- Quantity
- Unit Price
- Order Date

The dataset is stored in:

```text
data/orders.csv
```

---

# Docker & PostgreSQL

PostgreSQL is running inside a Docker container.

### PostgreSQL Configuration

```text
Container Name: postgres-db
Database: mydatabase
Username: admin
Port: 5432
```

### Start PostgreSQL Container

```bash
docker start postgres-db
```

### Check Container

```bash
docker ps
```

### Connect to PostgreSQL

```bash
docker exec -it postgres-db psql -U admin -d mydatabase
```

---

# Python Data Ingestion

The Python script is located at:

```text
scripts/load_data.py
```

The script performs the following steps:

```text
CSV File
   ↓
Pandas DataFrame
   ↓
PostgreSQL Connection
   ↓
Insert Records
   ↓
Commit Transaction
```

### Required Libraries

```bash
pip install pandas psycopg2-binary
```

### Run the Pipeline

From the project root:

```bash
python scripts/load_data.py
```

Expected output:

```text
Rows loaded from CSV: 25
Data successfully loaded into PostgreSQL.
```

---

# Database Design

The project uses two main tables.

### Raw Table

```text
orders_raw
```

This table stores the incoming raw data.

### Clean Table

```text
orders
```

The clean table uses database constraints to maintain data integrity.

Example:

```sql
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    customer_name VARCHAR(100),
    city VARCHAR(50),
    product VARCHAR(100),
    category VARCHAR(50),
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(12,2) NOT NULL CHECK (unit_price >= 0),
    order_date DATE NOT NULL
);
```

---

# Data Quality Checks

Before moving data into the clean table, several checks are performed.

### Check Missing Customer IDs

```sql
SELECT COUNT(*)
FROM orders_raw
WHERE customer_id IS NULL;
```

### Check Missing Products

```sql
SELECT COUNT(*)
FROM orders_raw
WHERE product IS NULL;
```

### Check Invalid Quantities

```sql
SELECT *
FROM orders_raw
WHERE quantity <= 0;
```

### Check Negative Prices

```sql
SELECT *
FROM orders_raw
WHERE unit_price < 0;
```

These checks help identify invalid records before the data is used for analysis.

---

# SQL Analysis

The project includes several analytical queries.

### Total Revenue

```sql
SELECT
    SUM(quantity * unit_price) AS total_revenue
FROM orders;
```

### Revenue by City

```sql
SELECT
    city,
    SUM(quantity * unit_price) AS revenue
FROM orders
GROUP BY city
ORDER BY revenue DESC;
```

### Revenue by Category

```sql
SELECT
    category,
    SUM(quantity * unit_price) AS revenue
FROM orders
GROUP BY category
ORDER BY revenue DESC;
```

### Average Order Value

```sql
SELECT
    AVG(quantity * unit_price) AS average_order_value
FROM orders;
```

### Monthly Revenue

```sql
SELECT
    DATE_TRUNC('month', order_date) AS month,
    SUM(quantity * unit_price) AS revenue
FROM orders
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month;
```

---

# PostgreSQL Views

A view was created to provide a reusable city-level sales summary.

```sql
CREATE VIEW city_sales AS
SELECT
    city,
    COUNT(*) AS orders,
    SUM(quantity * unit_price) AS revenue
FROM orders
GROUP BY city;
```

The view can be queried using:

```sql
SELECT *
FROM city_sales
ORDER BY revenue DESC;
```

---

# Materialized View

A materialized view was created for monthly sales analysis.

```sql
CREATE MATERIALIZED VIEW monthly_sales AS
SELECT
    DATE_TRUNC('month', order_date) AS month,
    SUM(quantity * unit_price) AS revenue,
    COUNT(*) AS orders
FROM orders
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month;
```

When the underlying data changes, the materialized view can be refreshed:

```sql
REFRESH MATERIALIZED VIEW monthly_sales;
```

---

# Query Optimization

An index was created on `customer_id` to improve customer-based queries.

```sql
CREATE INDEX idx_orders_customer_id
ON orders(customer_id);
```

Query performance can be investigated using:

```sql
EXPLAIN ANALYZE
SELECT *
FROM orders
WHERE customer_id = 101;
```

This allows the query execution plan and execution time to be analyzed.

---

# Transactions

The project also demonstrates PostgreSQL transactions.

Start a transaction:

```sql
BEGIN;
```

Perform an operation:

```sql
INSERT INTO orders
VALUES (
    999999,
    999,
    'Test Customer',
    'Karachi',
    'Test Product',
    'Testing',
    1,
    1000,
    '2026-08-01'
);
```

Cancel the transaction:

```sql
ROLLBACK;
```

Or permanently save the changes:

```sql
COMMIT;
```

---

# PostgreSQL Concepts Practiced

This project brings together the following PostgreSQL concepts:

- PostgreSQL architecture
- Storage and pages
- Indexes
- B-tree indexes
- Query planning
- `EXPLAIN`
- `EXPLAIN ANALYZE`
- Transactions
- MVCC
- Primary keys
- `NOT NULL`
- `CHECK` constraints
- Views
- Materialized views
- Partitioning concepts
- Query optimization
- `VACUUM`
- `ANALYZE`

---

# Learning Outcomes

After completing this project, I gained practical experience with:

1. Running PostgreSQL using Docker
2. Connecting Python to PostgreSQL
3. Loading CSV data into a relational database
4. Performing data quality checks
5. Designing tables with constraints
6. Writing analytical SQL queries
7. Creating database views
8. Creating materialized views
9. Creating indexes
10. Investigating query performance
11. Working with PostgreSQL transactions
12. Organizing a small Data Engineering project

---

# Future Improvements

Possible future improvements include:

- Use a larger dataset
- Add automated data validation
- Add PostgreSQL partitioning
- Add an ETL/ELT orchestration tool
- Add Docker Compose
- Add automated testing
- Add better logging and error handling
- Add a data warehouse layer
- Add a Power BI dashboard
- Deploy the pipeline to a cloud platform

---

# Learning Journey

```text
Python
   ↓
SQL
   ↓
Docker
   ↓
PostgreSQL
   ↓
Data Engineering Pipeline
   ↓
ETL / ELT
   ↓
Orchestration
   ↓
Cloud
   ↓
Data Warehouse
   ↓
Production Data Engineering
```

---

## Author

**Ali Raza**

This project was created as part of my Data Engineering learning journey and PostgreSQL practice.