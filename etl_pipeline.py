import duckdb
import os
import pandas as pd

DATA_DIR = "data"
OUTPUT_DIR = "."
DB_PATH = os.path.join(OUTPUT_DIR, 'gold_layer.duckdb')

print("Starting ELT Pipeline - Native DuckDB Engine")

# Delete old database to ensure fresh start
if os.path.exists(DB_PATH):
    try:
        os.remove(DB_PATH)
    except PermissionError:
        pass # If locked by dashboard, we'll try to connect and DROP tables instead

conn = duckdb.connect(DB_PATH)

# ==========================================
# 1. BRONZE LAYER (Direct read from CSVs)
# ==========================================
print("Extracting to Bronze Layer...")
conn.execute(f"CREATE OR REPLACE VIEW bronze_sales AS SELECT * FROM read_csv_auto('{os.path.join(DATA_DIR, 'Sales.csv')}')")
conn.execute(f"CREATE OR REPLACE VIEW bronze_items AS SELECT * FROM read_csv_auto('{os.path.join(DATA_DIR, 'Items.csv')}')")
conn.execute(f"CREATE OR REPLACE VIEW bronze_store AS SELECT * FROM read_csv_auto('{os.path.join(DATA_DIR, 'Store.csv')}')")
conn.execute(f"CREATE OR REPLACE VIEW bronze_client AS SELECT * FROM read_csv_auto('{os.path.join(DATA_DIR, 'Client.csv')}')")

# ==========================================
# 2. SILVER LAYER (Data Cleansing)
# ==========================================
print("Transforming to Silver Layer...")
conn.execute("""
    CREATE OR REPLACE TABLE silver_sales AS 
    SELECT 
        CAST(SALESDATE AS VARCHAR) AS DateKey,
        strptime(CAST(SALESDATE AS VARCHAR), '%Y%m%d') AS Data,
        StoreID,
        ITEMCODE,
        TRY_CAST(REPLACE(CAST("Vendas Unidades" AS VARCHAR), ',', '') AS INTEGER) AS Vendas_Unidades,
        TRY_CAST(REPLACE(REPLACE(CAST(PVP AS VARCHAR), ' €', ''), '€', '') AS DOUBLE) AS PVP
    FROM bronze_sales
""")

conn.execute("UPDATE silver_sales SET Vendas_Unidades = 0 WHERE Vendas_Unidades IS NULL")
conn.execute("UPDATE silver_sales SET PVP = 0 WHERE PVP IS NULL")
conn.execute("ALTER TABLE silver_sales ADD COLUMN Vendas_Valor DOUBLE")
conn.execute("UPDATE silver_sales SET Vendas_Valor = Vendas_Unidades * PVP")

conn.execute("""
    CREATE OR REPLACE TABLE silver_items AS 
    SELECT * FROM bronze_items 
    WHERE ITEMCODE IS NOT NULL
""")

# ==========================================
# 3. GOLD LAYER (Kimball Star Schema)
# ==========================================
print("Loading Star Schema to Gold Layer...")

# A. Fact_Sales
conn.execute("""
    CREATE OR REPLACE TABLE Fact_Sales AS 
    SELECT 
        StoreID, 
        ITEMCODE, 
        DateKey, 
        Vendas_Unidades AS "Vendas Unidades", 
        PVP, 
        Vendas_Valor AS "Vendas Valor"
    FROM silver_sales
    WHERE Vendas_Unidades > 0 AND Vendas_Valor >= 0
""")

# B. Dim_Item (With 'Unknown' inference for missing SKUs)
conn.execute("""
    CREATE OR REPLACE TABLE Dim_Item AS 
    SELECT ITEMCODE, SKU, Category, Brand, Segment FROM silver_items
    UNION ALL
    SELECT DISTINCT 
        s.ITEMCODE, 
        '⚠️ UNMAPPED (Missing SKU)' AS SKU, 
        'Beverages' AS Category, 
        'Beverama' AS Brand, 
        'Unknown' AS Segment 
    FROM silver_sales s
    LEFT JOIN silver_items i ON s.ITEMCODE = i.ITEMCODE
    WHERE i.ITEMCODE IS NULL
""")

# C. Dim_Store (Joining Store and Client)
conn.execute("""
    CREATE OR REPLACE TABLE Dim_Store AS 
    SELECT 
        s.StoreID,
        s.Store,
        CASE WHEN s.Store LIKE '%-%' THEN trim(split_part(s.Store, '-', -1)) ELSE 'Unknown' END AS City,
        s.Cliente,
        c.Cliente AS Client_Name,
        COALESCE(s."Store Type", c."Store Type") AS "Store Type"
    FROM bronze_store s
    LEFT JOIN bronze_client c ON s.Cliente = c.Cliente AND s.BannerID = c.BannerID
""")

# D. Dim_Date (Dynamic Calendar generation in Pandas, loaded to DuckDB)
min_year = conn.execute("SELECT MIN(EXTRACT(YEAR FROM Data)) FROM silver_sales").fetchone()[0]
max_year = conn.execute("SELECT MAX(EXTRACT(YEAR FROM Data)) FROM silver_sales").fetchone()[0]

date_range = pd.date_range(start=f"{int(min_year)}-01-01", end=f"{int(max_year)}-12-31", freq='D')
dim_date = pd.DataFrame({'Data': date_range})
dim_date['DateKey'] = dim_date['Data'].dt.strftime('%Y%m%d')
dim_date['Ano'] = dim_date['Data'].dt.year
dim_date['Mes'] = dim_date['Data'].dt.month
dim_date['Dia'] = dim_date['Data'].dt.day
dim_date['Trimestre'] = dim_date['Data'].dt.quarter
dim_date['Nome_Mes'] = dim_date['Data'].dt.month_name()
dim_date['AnoMes'] = dim_date['Data'].dt.strftime('%Y-%m')

conn.execute("CREATE OR REPLACE TABLE Dim_Date AS SELECT * FROM dim_date")

# Cleanup Intermediate Views/Tables
conn.execute("DROP VIEW bronze_sales")
conn.execute("DROP VIEW bronze_items")
conn.execute("DROP VIEW bronze_store")
conn.execute("DROP VIEW bronze_client")
conn.execute("DROP TABLE silver_sales")
conn.execute("DROP TABLE silver_items")

conn.close()
print(f"ELT concluded successfully! Native DuckDB engine output at: {DB_PATH}")
