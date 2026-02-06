# Hive


```
mkdir <<your-initial>>
```

```
cd <<your-initial>>
```

```
wget https://files.grouplens.org/datasets/movielens/ml-latest-small.zip
```

```
unzip ml-latest-small.zip
```

```
hdfs dfs -mkdir -p /bronze-<<your-initial>>/movies
```
```
hdfs dfs -mkdir -p /bronze-<<your-initial>>/ratings
```
```
hdfs dfs -ls /bronze-<<your-initial>>
```
```
cd /home/hadoop/<<your-initial>>/ml-latest-small
```

```
ls
```

```
hdfs dfs -put movies.csv /bronze-<<your-initial>>/movies/
```

```
hdfs dfs -put ratings.csv /bronze-<<your-initial>>/ratings/
```

use -f to overwrite if exists

```
hdfs dfs -ls /bronze-<<your-initial>>
hdfs dfs -ls /bronze-<<your-initial>>/movies
hdfs dfs -ls /bronze-<<your-initial>>/ratings
```

disk size
```
hdfs dfs -du -h /bronze-<<your-initial>>
```
first 10 lines 
```
hdfs dfs -cat /bronze-<<your-initial>>/movies/movies.csv | head
```
```
hdfs dfs -cat /bronze-<<your-initial>>/movies/movies.csv | head -n 5
```
last 10 lines

```
hdfs dfs -cat /bronze-<<your-initial>>/movies/movies.csv | tail
```

```
hdfs dfs -cat /bronze-<<your-initial>>/movies/movies.csv | tail -n 5
```

last 1 kb of the file, useful for inspecting large file,
does not read all

```
hdfs dfs -tail /bronze-<<your-initial>>/movies/movies.csv
```

```
hdfs dfs -head /bronze-<<your-initial>>/movies/movies.csv
```
