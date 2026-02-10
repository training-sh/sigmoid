```
CREATE DATABASE IF NOT EXISTS ecdb;
USE ecdb;
```

```
CREATE TABLE products (
    product_id INT,
    product_name STRING,
    brand_id INT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;
```

```
CREATE TABLE brands (
    brand_id INT,
    brand_name STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;
```

Insert 

```
INSERT INTO TABLE products VALUES
(1, 'iPhone', 100),
(2, 'Galaxy', 200),
(3, 'Redme', 300),   -- no matching brand
(4, 'Pixel', 400);
```

insert

```
INSERT INTO TABLE brands VALUES
(100, 'Apple'),
(200, 'Samsung'),
(400, 'Google'),
(500, 'Sony');      -- no matching product
```

### INNER JOIN

Only matching records on both sides
```
SELECT
    p.product_id,
    p.product_name,
    b.brand_name
FROM products p
INNER JOIN brands b
ON p.brand_id = b.brand_id;
```

### LEFT JOIN
All products, brand if available

```
SELECT
    p.product_id,
    p.product_name,
    b.brand_name
FROM products p
LEFT JOIN brands b
ON p.brand_id = b.brand_id;
```

### RIGHT JOIN

All brands, product if available
```
SELECT
    p.product_name,
    b.brand_name
FROM products p
RIGHT JOIN brands b
ON p.brand_id = b.brand_id;
```

### FULL OUTER JOIN

Everything from both sides
```
SELECT
    p.product_name,
    b.brand_name
FROM products p
FULL OUTER JOIN brands b
ON p.brand_id = b.brand_id;
```
### ORDER BY vs SORT BY  

- Global sort
- Single reducer
- Slow on large data
- Sorts entire dataset
- Produces one file

```
SELECT * FROM products
ORDER BY product_name;
```

### SORT BY
- Sorts within each reducer
- Parallel, scalable
- produces many files, a file per reducer
- data is sorted within reducer, not across reducers

When to use SORT BY,

- Writing data to HDFS
- Preparing data for merge, bucket join, sampling
- You don’t care about final visual order
- You want parallelism

```
SELECT * FROM products
SORT BY product_name;
```

Output order not globally guaranteed

# DISTRIBUTE BY + SORT BY

Controls reducer + sorting

```
SELECT *
FROM products
DISTRIBUTE BY brand_id
SORT BY product_name;
```

Same brand_id → same reducer → sorted inside reducer

More tips,

Brand is inserted while it was sorted by brand_id,


```
CREATE TABLE products_sorted (
    product_id INT,
    product_name STRING,
    brand_id INT
)
STORED AS ORC;
```

```
INSERT OVERWRITE TABLE products_sorted
SELECT *
FROM products
SORT BY brand_id;
```

The best option, use distributed by and sort, so you could control order at best cases, if not always

```
SELECT *
FROM products
DISTRIBUTE BY brand_id
SORT BY product_name;
```

## Map-side JOIN (broadcast join)

- One table very small (brands)
- Avoid shuffle

Enable in hive

```
SET hive.auto.convert.join=true;
SET hive.mapjoin.smalltable.filesize=25000000;
```

Query

```
SELECT /*+ MAPJOIN(b) */
    p.product_name,
    b.brand_name
FROM products p
JOIN brands b
ON p.brand_id = b.brand_id;
```

# Bucketed JOIN

- Same bucket key
- Same number of buckets
- Hive avoids full shuffle

### Create bucketed tables (ORC + buckets)
```
CREATE TABLE products_bucketed (
    product_id INT,
    product_name STRING,
    brand_id INT
)
CLUSTERED BY (brand_id) INTO 4 BUCKETS
STORED AS ORC;
```

```
CREATE TABLE brands_bucketed (
    brand_id INT,
    brand_name STRING
)
CLUSTERED BY (brand_id) INTO 4 BUCKETS
STORED AS ORC;
```

Enable

```
SET hive.enforce.bucketing=true;
```

```
INSERT INTO TABLE products_bucketed
SELECT * FROM products;
```

```
INSERT INTO TABLE brands_bucketed
SELECT * FROM brands;
```

Bucket Join

```
SELECT
    p.product_name,
    b.brand_name
FROM products_bucketed p
JOIN brands_bucketed b
ON p.brand_id = b.brand_id;
```

Hive knows:

- same bucket key

- same number of buckets, Bucket-to-bucket join (faster)
