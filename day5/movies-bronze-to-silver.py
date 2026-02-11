from pyspark.conf import SparkConf
config = SparkConf()

# config.set("property", "value")
# dont set master, these shall be passed via cli during yarn submit
# config.setMaster("local[4]").setAppName("MovieLens")

from pyspark.sql import SparkSession
# spark Session, entry point for Spark SQL, DataFrame
spark = SparkSession.builder\
                    .config(conf=config)\
                    .getOrCreate()

sc = spark.sparkContext

# how to create schema programatically instead of using inferSchema
from pyspark.sql.types import StructType, LongType, StringType, IntegerType, DoubleType
# True is nullable, False is non nullable
movieSchema = StructType()\
                .add("movieId", IntegerType(), True)\
                .add("title", StringType(), True)\
                .add("genres", StringType(), True)

# read movie data
# read using dataframe with defind schema
# we can use folder path - all csv in the folder read
# use file path, only that file read

# spark is session, entry point for data frame/sql

# hdfs://localhost:9000/ml-latest-small/movies.csv

movieDf = spark.read.format("csv")\
                .option("header", True)\
                .schema(movieSchema)\
                .load("/bronze/movies")

movieDf.printSchema()
movieDf.show(2) # action

print (movieDf.count())

movieDf.write.mode("overwrite").parquet("/silver/movies")

