Download movie lens data, store them into bronze zone

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

```
hdfs dfs -mkdir -p /silver
hdfs dfs -mkdir -p /gold
```

anyone read/write, not safe, you may restrict only to livy notebook user

```
hdfs dfs -chmod -R 777 /silver
hdfs dfs -chmod -R 777 /gold
```

in production, hdfs dfs -chown -R hadoop:hadoop /somedirectory   where hadoop is username, hadoop is group user:group format


Now, run the Movies-Bronze-To-Silver-Notebook.ipynb over EMR Studio

inspect the result 

```
hdfs dfs -ls /silver/movies
```

else 

```
cd ~
```

Deploy Modes Client

```
--deploy-mode client
Driver runs on master
Code must exist on master
Logs appear in terminal
```

```
--deploy-mode cluster (Recommended)
Driver runs inside YARN container
Code must be in S3 or HDFS
More stable
```


```
wget https://raw.githubusercontent.com/training-sh/sigmoid/refs/heads/main/day5/movies-bronze-to-silver.py
```

```
hdfs dfs -rm -r /silver/movies/*
```

```
hdfs dfs -ls   /silver/movies/
```


```
spark-submit --master yarn --deploy-mode cluster movies-bronze-to-silver.py
```

fails, since we don't have enough resources

```
spark-submit \
  --master yarn \
  --deploy-mode cluster \
  --driver-memory 20G \
  --executor-memory 20G \
  --executor-cores 20 \
  --num-executors 1 \
  movies-bronze-to-silver.py
```
