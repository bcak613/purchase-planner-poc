# Seasonal Purchase Planner POC

This repository contains a quickstart proof-of-concept for exploring ERP data with PostgreSQL, Adminer, and Metabase. It sets up a local analytics stack and provides SQL to create staging tables and simple BI views.

## Getting Started

1. **Start the stack**
   ```bash
   docker compose up -d
   ```
   Services will be available at:
   - **Postgres**
     - Host: `postgres` (inside Docker network) or `localhost:5432` from your machine
     - `POSTGRES_USER=planner`
     - `POSTGRES_PASSWORD=planner`
     - `POSTGRES_DB=erp`
   - **Adminer**
     - URL: [http://localhost:8080](http://localhost:8080)
     - Connect to Postgres using host `postgres` from the Adminer container or `localhost` from the host
   - **Metabase**
     - URL: [http://localhost:3000](http://localhost:3000)
     - When adding the database, set host to `postgres` so Metabase reaches Postgres via the Docker network

2. **Create schemas and tables**

   In Adminer choose the `erp` database, click **SQL command**, then either paste the contents of [`sql/schema.sql`](sql/schema.sql) or use the *File to upload* field to upload it and execute so all tables and views are created. The file can also be run via `psql -f sql/schema.sql` if you prefer the CLI.

3. **Import CSV data**

    Save your files with **UTF-8 encoding** and **comma** separators. If any values need quoting, wrap them in **double quotes** to match Adminer defaults. Import the CSVs into the `stage_*` tables via Adminer (Table → Import → CSV) and see [Section 7](#7-troubleshooting) if Adminer misreads delimiters or quotes. Sample files in [`sample_data/`](sample_data/) demonstrate the required headers and one row of data for each table:

    `dim_product.csv` → `stage_dim_product`

    ```csv
    sku,fruit,variety,size,label,grade,origin
    APPL001,Apple,Gala,Medium,FarmCo,A,USA
    ```

    `sales_2024.csv` → `stage_fact_sales`

    ```csv
    txn_date,sku,qty_kg,revenue,channel
    2024-01-15,APPL001,100,2000,Wholesale
    ```

    `purchase_2024.csv` → `stage_fact_purchase`

    ```csv
    po_date,grn_date,sku,supplier,qty_kg,unit_cost
    2023-12-20,2024-01-05,APPL001,SupplierCo,120,10.50
    ```

    `inventory_2024.csv` → `stage_fact_inventory`

    ```csv
    snap_date,sku,on_hand_kg,in_transit_kg
    2024-01-31,APPL001,80,20
    ```

    Use these as templates when preparing your own data and import them via Adminer. Ensure the headers match the columns defined in [`sql/schema.sql`](sql/schema.sql); for example, the purchase file must include `po_date`, `grn_date`, `sku`, `supplier`, `qty_kg`, and `unit_cost` to align with `stage_fact_purchase`.

4. **Explore in Metabase**

   Connect Metabase to the `erp` database (host `postgres`, user `planner`, password `planner`) and build dashboards using the provided views.


## 7) Troubleshooting

- Postgres not up: `docker logs poc_postgres` (check for port 5432 conflicts).
- Metabase first launch is slow: wait 1–2 minutes for initialization.
- Import CSV fails due to delimiters or quotes: switch to a `;` delimiter or set `QUOTE '"'` in Adminer.
