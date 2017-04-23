package play_crawler

import org.apache.log4j.{Level, Logger}
import org.apache.spark.sql.{SQLContext, SaveMode}
import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.sql.functions._

/**
  * Created by mukul on 22/1/17.
  */
object scrap {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setMaster("local[*]").setAppName("dftry")
    val sc = new SparkContext(conf)
    val sqlContext = new SQLContext(sc)

    val rootLogger = Logger.getRootLogger()
    rootLogger.setLevel(Level.ERROR)

    val playScrapCSVPath = "/home/mukul/IdeaProjects/spark/src/main/resources/scrap.csv"
    val playScrapDF = sqlContext.read
      .format("com.databricks.spark.csv")
      .option("header","true")
      .load(playScrapCSVPath)

    playScrapDF.show()
    playScrapDF.cache()

    playScrapDF
      .coalesce(10)
      .write
      .mode(SaveMode.Overwrite)
      .format("com.databricks.spark.csv")
      .option("header","true")
      .save("/home/mukul/Documents/Play_Crawler/static/play-scrap-csv")

    val total = playScrapDF.count()

    val genreDF = playScrapDF
      .select(playScrapDF("genre"), playScrapDF("name"))
      .groupBy("genre")
      .agg(
        count("*").alias("no_of_Apps"),
        count("*").multiply(100).divide(total).cast("integer").alias("percentage")
      )
    genreDF.show()

    genreDF
      .coalesce(1)
      .write
      .mode(SaveMode.Overwrite)
      .format("com.databricks.spark.csv")
      .option("header","true")
      .save("/home/mukul/Documents/Play_Crawler/static/genre-csv")

    val downloadsDF = playScrapDF
      .select(playScrapDF("downloads"), playScrapDF("name"))
      .groupBy("downloads")
      .agg(
        count("*").alias("no_of_Apps"),
        count("*").multiply(100).divide(total).cast("integer").alias("percentage")
      )
    downloadsDF.show()

    downloadsDF
      .coalesce(1)
      .write
      .mode(SaveMode.Overwrite)
      .format("com.databricks.spark.csv")
      .option("header","true")
      .save("/home/mukul/Documents/Play_Crawler/static/downloads-csv")

    val contentRateDF = playScrapDF
      .select(playScrapDF("contentRating"), playScrapDF("name"))
      .groupBy("contentRating")
      .agg(
        count("*").alias("no_of_Apps"),
        count("*").multiply(100).divide(total).cast("integer").alias("percentage")
      )
    contentRateDF.show()

    contentRateDF
      .coalesce(1)
      .write
      .mode(SaveMode.Overwrite)
      .format("com.databricks.spark.csv")
      .option("header","true")
      .save("/home/mukul/Documents/Play_Crawler/static/content-rate-csv")

    val scoreClassDF = playScrapDF
      .select(playScrapDF("scoreClass"), playScrapDF("name"))
      .groupBy("scoreClass")
      .agg(
        count("*").alias("no_of_Apps"),
        count("*").multiply(100).divide(total).cast("integer").alias("percentage")
      )
    scoreClassDF.show()

    scoreClassDF
      .coalesce(1)
      .write
      .mode(SaveMode.Overwrite)
      .format("com.databricks.spark.csv")
      .option("header","true")
      .save("/home/mukul/Documents/Play_Crawler/static/score-class-csv")

    playScrapDF.unpersist()
  }
}