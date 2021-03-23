# Football Twitter Streaming

This is a project for the Unstructured and Streaming Data Engineering Course from the M.Sc. of Computer Science and Engineering of Politecnico di Milano<br/>

It's a Data pipeline to analyze real time football data extracted from Twitter posts.


## Architecture

The technology stack used for this project is the following:


* Kafka and Confluent, as Streaming frameworks
* Twitter Developer API and Confluent Connector, as data source 
* PySpark, to make processing queries on the Kafka topics
* Elasticsearch and Kibana, for data storage and visualization respectively

![alt text](https://i.ibb.co/0ykJVzc/pipeline.png?raw=true)



## Setup

This tutorial assumes you have Docker and Docker-Compose installed on your system, if you don't you can get them from https://www.docker.com/

Once you have Docker set up,you can clone the repository:

```bash
git clone https://github.com/AlessandroMessori/Football-Twitter-Streaming
```

Inside the cloned the repo, you need to replace the asterisks in the "twitter_connector_config" file in the config folder with your Twitter Developer credentials.

If you don't have them you can get a set here: https://developer.twitter.com/

To start the docker cluster cd into the cloned directory run the following command:

```bash
docker-compose up -d
```

Depending on your Docker installation you might need to use sudo.

After the command have been executed, you should now have a working Kafla cluster with a single Broker.

You can access the  Confluent control center at http://localhost:9021/ 

For a guide on how to use the control center refer to https://docs.confluent.io/platform/current/control-center/index.html

You should now upload the configurations for the Twitter Source connector and the Elasticsearch Sink connector from the config file,you can do it in the Connectors section of the Control Center


![alt text](https://i.ibb.co/rd7gPTJ/upload.png?raw=true)



You can access a Jupyter Notebook with PySpark installed and run all stream analysis queries at http://localhost:8888/ (access token: usde)

To visualize the results of the computation you can connect to Kibana at http://localhost:5601/.

You can create your own visualization or use the one I already configured,you can load it by uploading the file "" in the Dashboard section of Kibana.

## Limitations and Future Improvements

This project has the objective of counting the most popular football topics on Twitter;
It does its job  nicely but there are still a few problems that should be addressed in the future:

* Multiword topics aren't considered (e.g. "Real Madrid","Manchester United")
* Only topics corresponding to the most popular teams and players in the Fifa dataset are considered, other relevant topics such as coaches,staff members or competitions are at the moment not considered in the word count.
* The number of hastags monitored it's limited, for now I only considered the word "football" translated in the languages of the most important european leagues (english,spanish,italian,french and german). It would be nice to find a way to monitor more hashtags without adding any bias to the data collection (for example if I started monitoring "#Juventus" the data distribution would be skewed towards players of this particular team).