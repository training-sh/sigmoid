```

CREATE DATABASE IF NOT EXISTS sales
LOCATION '/user/hive/warehouse/sales.db';

```

```
USE sales;
```

# Table WITHOUT partition, WITHOUT bucket

SCAN all data, shuffle all data during join

```
CREATE TABLE sales.orders_plain (
  order_id     BIGINT,
  customer_id  BIGINT,
  product_id   BIGINT,
  order_date   DATE,
  amount       DECIMAL(10,2)
)
STORED AS ORC;
```

```
sales.db/orders_plain/
 ├── 000000_0.orc
 ├── 000001_0.orc
```

Table with partition (alredy discussed)

```
CREATE TABLE sales.orders_partitioned (
  order_id     BIGINT,
  customer_id  BIGINT,
  product_id   BIGINT,
  amount       DECIMAL(10,2)
)
PARTITIONED BY (order_date DATE)
STORED AS ORC;
```

```
sales.db/orders_partitioned/
 ├── order_date=2025-02-01/
 ├── order_date=2025-02-02/
```

## Table WITH BUCKET only (no partition)

```
CREATE TABLE sales.orders_bucketed_only (
  order_id     BIGINT,
  customer_id  BIGINT,
  product_id   BIGINT,
  order_date   DATE,
  amount       DECIMAL(10,2)
)
CLUSTERED BY (customer_id) INTO 4 BUCKETS
STORED AS ORC;
```

```
sales.db/orders_bucketed_only/
 ├── 000000_0.orc
 ├── 000001_0.orc
 ├── 000002_0.orc
 ├── 000003_0.orc
```

# table with all, plus compression

-- Partition pruning
-- Bucketed joins
-- ORC + compression
-- Enforced bucketing

hive settings

```
SET hive.exec.dynamic.partition=true;
SET hive.exec.dynamic.partition.mode=nonstrict;

SET hive.enforce.bucketing=true;
SET hive.exec.compress.output=true;
SET hive.exec.orc.default.compress=SNAPPY;
```

```
CREATE TABLE sales.orders_part_bucketed (
  order_id     BIGINT,
  customer_id  BIGINT,
  product_id   BIGINT,
  amount       DECIMAL(10,2)
)
PARTITIONED BY (order_date DATE)
CLUSTERED BY (customer_id) INTO 4 BUCKETS
STORED AS ORC
TBLPROPERTIES (
  'orc.compress'='SNAPPY'
);
```

```
sales.db/orders_part_bucketed/
 ├── order_date=2025-02-01/
 │    ├── 000000_0.orc
 │    ├── 000001_0.orc
 │    ├── 000002_0.orc
 │    ├── 000003_0.orc
 ├── order_date=2025-02-02/
 │    ├── 000000_0.orc
 │    ├── 000001_0.orc
 ```

```
INSERT INTO sales.orders_part_bucketed PARTITION (order_date)
SELECT
  order_id,
  customer_id,
  product_id,
  amount,
  order_date
FROM sales.orders_plain;
```


# Insert data into orders_plain

- Base table – no partition, no bucket
- 20 records, 5 different order dates, many customer_ids

```
INSERT INTO TABLE sales.orders_plain VALUES
(1001, 101, 501, DATE '2025-02-01', 1200.50),
(1002, 102, 502, DATE '2025-02-01', 850.00),
(1003, 103, 503, DATE '2025-02-01', 430.75),
(1004, 104, 504, DATE '2025-02-01', 999.99),

(1005, 101, 505, DATE '2025-02-02', 1500.00),
(1006, 102, 506, DATE '2025-02-02', 300.25),
(1007, 105, 507, DATE '2025-02-02', 720.40),
(1008, 106, 508, DATE '2025-02-02', 640.00),

(1009, 107, 509, DATE '2025-02-03', 2000.00),
(1010, 108, 510, DATE '2025-02-03', 1100.10),
(1011, 103, 511, DATE '2025-02-03', 560.60),
(1012, 104, 512, DATE '2025-02-03', 890.00),

(1013, 109, 513, DATE '2025-02-04', 450.45),
(1014, 110, 514, DATE '2025-02-04', 780.00),
(1015, 101, 515, DATE '2025-02-04', 620.00),
(1016, 102, 516, DATE '2025-02-04', 300.00),

(1017, 111, 517, DATE '2025-02-05', 950.00),
(1018, 112, 518, DATE '2025-02-05', 1250.75),
(1019, 105, 519, DATE '2025-02-05', 400.00),
(1020, 106, 520, DATE '2025-02-05', 670.30);
```

Insert into partitioned table

Dynamic partitioning
Hive automatically creates folders by order_date

```
SET hive.exec.dynamic.partition=true;
SET hive.exec.dynamic.partition.mode=nonstrict;
```

```
INSERT INTO TABLE sales.orders_partitioned PARTITION (order_date)
SELECT
  order_id,
  customer_id,
  product_id,
  amount,
  order_date
FROM sales.orders_plain;
```


Insert into bucket-only table

No partitions
Data is hashed by customer_id → 4 buckets

Enforce bucketing is required

```
SET hive.enforce.bucketing=true;
```

```
INSERT INTO TABLE sales.orders_bucketed_only
SELECT
  order_id,
  customer_id,
  product_id,
  order_date,
  amount
FROM sales.orders_plain;
```

- Enables bucketed joins on customer_id
- No partition pruning


## Insert into partition + bucket + ORC + SNAPPY

Best-practice Hive table
This is the real production pattern

```
SET hive.exec.dynamic.partition=true;
SET hive.exec.dynamic.partition.mode=nonstrict;

SET hive.enforce.bucketing=true;
SET hive.exec.compress.output=true;
SET hive.exec.orc.default.compress=SNAPPY;
```

```
INSERT INTO TABLE sales.orders_part_bucketed PARTITION (order_date)
SELECT
  order_id,
  customer_id,
  product_id,
  amount,
  order_date
FROM sales.orders_plain;
```

```
sales.db/orders_part_bucketed/
 ├── order_date=2025-02-01/
 │    ├── 000000_0.orc
 │    ├── 000001_0.orc
 │    ├── 000002_0.orc
 │    ├── 000003_0.orc
 ├── order_date=2025-02-02/
 │    ├── 000000_0.orc
 │    ├── 000001_0.orc
 │    ├── 000002_0.orc
 │    ├── 000003_0.orc
 └── ...
 ```


 Features 

 | Feature             | orders_plain | partitioned | bucketed_only | part_bucketed |
|---------------------|--------------|-------------|---------------|---------------|
| Partition pruning   | NO           | YES         | NO            | YES           |
| Bucketed join       | NO           | NO          | YES           | YES           |
| Shuffle reduction   | NO           | PARTIAL     | YES           | YES           |
| ORC + compression   | YES          | YES         | YES           | YES           |
| Production ready    | NO           | PARTIAL     | PARTIAL       | YES           |
