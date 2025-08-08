CREATE SCHEMA IF NOT EXISTS stage;
CREATE SCHEMA IF NOT EXISTS marts;

-- Master/Product
CREATE TABLE IF NOT EXISTS stage_dim_product (
  sku TEXT PRIMARY KEY,
  fruit TEXT,
  variety TEXT,
  size TEXT,
  label TEXT,
  grade TEXT,
  origin TEXT
);

-- Sales fact (ngày)
CREATE TABLE IF NOT EXISTS stage_fact_sales (
  txn_date DATE,
  sku TEXT REFERENCES stage_dim_product(sku),
  qty_kg NUMERIC,
  revenue NUMERIC,
  channel TEXT
);

-- Purchase fact (PO/GRN)
CREATE TABLE IF NOT EXISTS stage_fact_purchase (
  po_date DATE,
  grn_date DATE,
  sku TEXT REFERENCES stage_dim_product(sku),
  supplier TEXT,
  qty_kg NUMERIC,
  unit_cost NUMERIC
);

-- Inventory snapshot (cuối ngày/tháng)
CREATE TABLE IF NOT EXISTS stage_fact_inventory (
  snap_date DATE,
  sku TEXT REFERENCES stage_dim_product(sku),
  on_hand_kg NUMERIC,
  in_transit_kg NUMERIC
);

-- Bán theo tháng
CREATE OR REPLACE VIEW marts_v_monthly_sales AS
SELECT date_trunc('month', txn_date)::date AS month,
       sku,
       SUM(qty_kg) AS qty_kg,
       SUM(revenue) AS revenue
FROM stage_fact_sales
GROUP BY 1,2;

-- Tồn cuối tháng
CREATE OR REPLACE VIEW marts_v_monthly_inventory AS
SELECT date_trunc('month', snap_date)::date AS month,
       sku,
       SUM(on_hand_kg) AS on_hand_kg,
       SUM(in_transit_kg) AS in_transit_kg
FROM stage_fact_inventory
GROUP BY 1,2;
