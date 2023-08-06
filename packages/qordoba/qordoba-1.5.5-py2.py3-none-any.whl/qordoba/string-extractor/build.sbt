name := "qordoba-string-extractor"

version := "1.0"

scalaVersion := "2.11.8"

libraryDependencies ++= Seq(
  "ch.qos.logback" % "logback-classic" % "1.2.3",
  "com.github.scopt" %% "scopt" % "3.6.0",
  "com.opencsv" % "opencsv" % "3.10",
  "com.typesafe.scala-logging" %% "scala-logging-slf4j" % "2.1.2",
  "org.antlr" % "antlr4-runtime" % "4.7",
  "org.scalatest" %% "scalatest" % "2.2.4" % Test
)
