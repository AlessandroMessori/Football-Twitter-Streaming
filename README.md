# Football Twitter Streaming

This is a project for the Unstructured and Streaming Data Engineering Course from the M.Sc. of Computer Science and Engineering of Politecnico di Milano<br/>

It's a Data pipeline to analyze real time football data extracted from Twitter posts.


## Architecture

The technology stack used for this project is the following:


* Kafka and Confluent, as Streaming frameworks
* Twitter Developer API and Confluent Connector, as data source 
* PySpark, to make processing queries on the Kafka topics
* Elasticsearch and Kibana, for data storage and visualization respectively




## Setup

First of all you have to clone this repository:

```bash
git clone https://github.com/AlessandroMessori/Football-Twitter-Streaming
```

Once you have clone the repo, you need to insert your Twitter Developer credentials into the config file.

If you don't have them you can get a set here: https://developer.twitter.com/en

Cd into the cloned directory and start the docker cluster:

```bash
docker-compose up -d
```

Depending on your Docker installation you might need to use sudo to run the Docker commands.

After the command have been executed, you should now have a completely setup Kafla cluster connected to the Twitter Source and the Elasticsearch Sink

You can access the  Confluent control center at http://localhost:9021/ 

You can now start running the real time queries written in Spark by using this command:


```bash
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1 pySpark/main.py > output.txt
```

To visualize the results of the computation you can connect to Kibana at http://localhost:5601/.

You can create your own visualization or use the one I already configured.

## Limitations and Future Improvements