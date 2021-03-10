FROM confluentinc/cp-kafka-connect-base:6.1.0

#installs the twitter connector and 
RUN confluent-hub install jcustenborder/kafka-connect-twitter:0.3.33 --no-prompt

