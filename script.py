"""Практика PySpark и SparkSQL (pyspark.sql.functions)
Задача. Сделать пайплайн обработки файла cars.csv.

Необходимо посчитать по каждому производителю (поле manufacturer_name):

кол-во объявлений
средний год выпуска автомобилей
минимальную цену
максимальную цену
Выгрузить результат в output.csv."""

# https://github.com/oleg-agapov/getting-started-with-pyspark-ru/blob/master/practice-2/2-cars-dataset-etl.ipynb

from pyspark.sql import SparkSession, DataFrame
import pyspark.sql.functions as F
import pyspark.sql.types as t


def extract_data(spark: SparkSession) -> DataFrame:
    path = "data/cars.csv"
    return spark.read.option("header", "true").csv(path)


def transform_data(df: DataFrame) -> DataFrame:
    output = (
        df
        .groupBy("manufacturer_name")
        .agg(
            F.count("manufacturer_name").alias("count_ads"),
            F.round(F.avg("year_produced")).cast(t.IntegerType()).alias("avg_year_produced"),
            F.min("price_usd").alias("min_price"),
            F.max("price_usd").alias("max_price"),
        )
        .orderBy(F.col("count_ads").desc())
    )
    return output


def save_data(df: DataFrame) -> None:
    df.coalesce(4).write.mode("overwrite").format("json").save("output.json")


def main():
    spark = SparkSession.builder.appName("Practice 2").getOrCreate()
    df = extract_data(spark)
    output = transform_data(df)
    save_data(output)
    #spark.stop()

main()