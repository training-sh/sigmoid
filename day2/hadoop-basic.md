# Check YARN status
```
yarn version
```
```
yarn node -list
```
```
yarn application -list
```
```
yarn queue -status default
```

# Resource overview
```
yarn cluster --list-node-labels
```
```
yarn scheduler
```

# HDFS basics (input & output locations)
## Check HDFS

```
hdfs dfs -ls /
```
```
hdfs dfs -df -h
```

# Create input directory

Since we share cluster, change the <<your-initial>>, for me ,   gks
 

```
hdfs dfs -mkdir -p /user/hadoop/input-<<your-initial>>
```
 
## Upload sample file
```
echo "hello emr hadoop yarn hadoop emr" > wc-<<your-initial>>.txt
```
```
hdfs dfs -put wc-<<your-initial>>.txt /user/hadoop/input-<<your-initial>>
```

Remove output directory if exists

```
hdfs dfs -rm -r /user/hadoop/output_wc-<<your-initial>>
```

## Hadoop WordCount (low resource usage)
## Hadoop examples JAR location (EMR default)
```
ls /usr/lib/hadoop-mapreduce/
```

You will see:

hadoop-mapreduce-examples.jar

# Submit WordCount with low memory & cores

Minimal YARN resource job

```
yarn jar /usr/lib/hadoop-mapreduce/hadoop-mapreduce-examples.jar \
wordcount \
-D mapreduce.job.queuename=default \
-D mapreduce.map.memory.mb=1256 \
-D mapreduce.reduce.memory.mb=1256 \
-D mapreduce.map.java.opts="-Xmx1200m" \
-D mapreduce.reduce.java.opts="-Xmx1200m" \
-D mapreduce.map.cpu.vcores=1 \
-D mapreduce.reduce.cpu.vcores=1 \
/user/hadoop/input-<<your-initial>> \
/user/hadoop/output_wc-<<your-initial>>
```

Here after adjust the path based on what you given as output path
 

View job output (HDFS)
```
hdfs dfs -ls /user/hadoop/output_wc-<<your-initial>>
hdfs dfs -cat /user/hadoop/output_wc-<<your-initial>>/part-r-00001
```

# YARN application tracking (CLI)
List applications
```
yarn application -list
```

Get application status
```
yarn application -status application_XXXXXXXXXXXX_XXXX
```

Kill application (if needed)
```
yarn application -kill application_XXXXXXXXXXXX_XXXX
```
# Application logs (VERY IMPORTANT)

View logs from CLI
```
yarn logs -applicationId application_XXXXXXXXXXXX_XXXX
```

Logs for specific container

```
yarn logs -applicationId <app_id> -containerId <container_id>
```
