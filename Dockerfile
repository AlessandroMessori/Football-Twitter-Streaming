FROM confluentinc/cp-kafka-connect-base:6.1.0

#installs the twitter connector
RUN confluent-hub install jcustenborder/kafka-connect-twitter:0.3.33 --no-prompt

#installs the datagen connector
RUN confluent-hub install confluentinc/kafka-connect-datagen:0.4.0 --no-prompt

#installs the elastichsearch connector
RUN confluent-hub install confluentinc/kafka-connect-elasticsearch:5.4.0 --no-prompt

#TODO
#Upload Twitter Connector Configuration
#Upload Elasticsearch Connector Configuration