# Hive

Note, removed your initials from commands.



```
wget https://files.grouplens.org/datasets/movielens/ml-latest-small.zip
```

```
unzip ml-latest-small.zip
```

```
hdfs dfs -mkdir -p /bronze/movies
```
```
hdfs dfs -mkdir -p /bronze/ratings
```
```
hdfs dfs -ls /bronze
```
```
cd ml-latest-small
```

```
ls
```

```
hdfs dfs -put movies.csv /bronze/movies/
```

```
hdfs dfs -put ratings.csv /bronze/ratings/
```

use -f to overwrite if exists

```
hdfs dfs -ls /bronze
hdfs dfs -ls /bronze/movies
hdfs dfs -ls /bronze/ratings
```

disk size
```
hdfs dfs -du -h /bronze
```
first 10 lines 
```
hdfs dfs -cat /bronze/movies/movies.csv | head
```
```
hdfs dfs -cat /bronze/movies/movies.csv | head -n 5
```
last 10 lines

```
hdfs dfs -cat /bronze/movies/movies.csv | tail
```

```
hdfs dfs -cat /bronze/movies/movies.csv | tail -n 5
```

last 1 kb of the file, useful for inspecting large file,
does not read all

```
hdfs dfs -tail /bronze/movies/movies.csv
```

```
hdfs dfs -head /bronze/movies/movies.csv
```



# Hive

```
hive
```

```
SHOW DATABASES;
```

```

SELECT current_database();
```

```
SHOW TABLES;
```

```
CREATE DATABASE IF NOT EXISTS movielens;
```

```
SHOW DATABASES;
```

```
USE movielens;
```

```
SELECT current_database();
```

```
CREATE EXTERNAL TABLE IF NOT EXISTS movies_raw (
  movieId INT,
  title STRING,
  genres STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  "separatorChar" = ",",
  "quoteChar"     = "\"",
  "escapeChar"    = "\\"
)
STORED AS TEXTFILE
LOCATION '/bronze/movies';
```

```
SELECT * FROM movies_raw LIMIT 5;
```

```
SELECT COUNT(*) FROM movies_raw;
```

```
SELECT movieId, title
FROM movies_raw
WHERE genres LIKE '%Comedy%'
LIMIT 10
```
Ratings table

```
CREATE EXTERNAL TABLE IF NOT EXISTS ratings_raw (
  userId     INT,
  movieId    INT,
  rating     DOUBLE,
  `timestamp` BIGINT
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  "separatorChar" = ",",
  "quoteChar"     = "\"",
  "escapeChar"    = "\\"
)
STORED AS TEXTFILE
LOCATION '/bronze/ratings'
TBLPROPERTIES (
  "skip.header.line.count" = "1"
);
```

```
SELECT * FROM ratings_raw LIMIT 5;
```

 
EXIT;

