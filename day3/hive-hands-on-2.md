### Hive Managed Tables

### Hive Data Partitions

### Hive Aggregate queries

```
 hdfs dfs -ls /
'''

```
 hdfs dfs -ls /user
```

```
 hdfs dfs -ls /user/hive
```

```
hdfs dfs -ls /user/hive/warehouse
```


```
hive
```

```
CREATE DATABASE IF NOT EXISTS company;
USE company;
```

```
CREATE TABLE emp_managed (
    name   STRING,
    dept   STRING,
    salary INT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;
```

location in hadoop

/user/hive/warehouse/company.db/emp_managed

```
INSERT INTO TABLE emp_managed VALUES
('James',  'Sales',     3000),
('Michael','Sales',     4600),
('Robert', 'Sales',     4100),
('Maria',  'Finance',   3000),
('James',  'Sales',     3000),
('Scott',  'Finance',   3300),
('Jen',    'Finance',   3900),
('Jeff',   'Marketing', 3000),
('Kumar',  'Marketing', 2000),
('Saif',   'Sales',     4100),
('Joe',    'Sales',     4200),
('Venkat', 'Sales',     4000);
```

```
SELECT * FROM emp_managed;
```
```
SELECT
    dept,
    SUM(salary) AS total_salary
FROM emp_managed
GROUP BY dept;
```

```
SELECT
    dept,
    AVG(salary) AS avg_salary
FROM emp_managed
GROUP BY dept;
```

```
SELECT
    dept,
    COUNT(*) AS emp_count
FROM emp_managed
GROUP BY dept;
```

```
SELECT
    dept,
    SUM(salary) AS total_salary,
    MAX(salary) AS max_salary
FROM emp_managed
GROUP BY dept;
```

```
CREATE TABLE dept_salary_summary (
    dept STRING,
    total_salary INT
);
```

```
INSERT INTO TABLE dept_salary_summary
SELECT
    dept,
    SUM(salary)
FROM emp_managed
GROUP BY dept;
```

```
Classic Hive (TEXTFILE / ORC without ACID)
Operation	Supported?
UPDATE	  No
DELETE	  No
INSERT	  Yes  (append mode)
INSERT OVERWRITE  Yes (remove existing, append again)
```

---

```
CREATE TABLE emp_part (
    name   STRING,
    salary INT
)
PARTITIONED BY (dept STRING)
STORED AS TEXTFILE;
```

```
/user/hive/warehouse/company.db/emp_part/
  ├── dept=Sales/
  ├── dept=Finance/
  └── dept=Marketing/
```

```
INSERT INTO TABLE emp_part PARTITION (dept='Sales')
VALUES
('James',   3000),
('Michael', 4600),
('Robert',  4100),
('James',   3000),
('Saif',    4100),
('Joe',     4200),
('Venkat',  4000);
```

```
INSERT INTO TABLE emp_part PARTITION (dept='Finance')
VALUES
('Maria', 3000),
('Scott', 3300),
('Jen',   3900);
```

```
INSERT INTO TABLE emp_part PARTITION (dept='Marketing')
VALUES
('Jeff',  3000),
('Kumar', 2000);
```

Dynamic partitions

```
SET hive.exec.dynamic.partition = true;
SET hive.exec.dynamic.partition.mode = nonstrict;
```

```
CREATE TABLE emp_stage (
    name STRING,
    dept STRING,
    salary INT
);
```

```
INSERT INTO TABLE emp_stage VALUES
('James','Sales',3000),
('Michael','Sales',4600),
('Robert','Sales',4100),
('Maria','Finance',3000),
('James','Sales',3000),
('Scott','Finance',3300),
('Jen','Finance',3900),
('Jeff','Marketing',3000),
('Kumar','Marketing',2000),
('Saif','Sales',4100),
('Joe','Sales',4200),
('Venkat','Sales',4000);

```

```
INSERT INTO TABLE emp_part PARTITION (dept)
SELECT
    name,
    salary,
    dept
FROM emp_stage;
```
```
SHOW PARTITIONS emp_part;
```

Full table scan

```
SELECT * FROM emp_part;
```

Partition pruning (FAST )
```
SELECT * 
FROM emp_part
WHERE dept = 'Sales'
```

Total salary per department
```
SELECT
    dept,
    SUM(salary) AS total_salary
FROM emp_part
GROUP BY dept;
```

```
SELECT
    dept,
    AVG(salary) AS avg_salary
FROM emp_part
GROUP BY dept;
```

```
SELECT
    dept,
    COUNT(*) AS emp_count
FROM emp_part
GROUP BY dept;
```

```
INSERT OVERWRITE TABLE emp_part PARTITION (dept='Sales')
SELECT
    name,
    salary
FROM emp_part
WHERE dept = 'Sales'
  AND salary >= 4000;
```

```
TRUNCATE TABLE emp_part;
```

```
TRUNCATE TABLE emp_part PARTITION (dept='Sales');
```

delete dept=Sales/

```
TRUNCATE TABLE external_table;
```

You already know to drop table
