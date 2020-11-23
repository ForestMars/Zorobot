from logging import StreamHandler
from kafka_producer import KafkaSend

class KafkaHandler(StreamHandler):

    def __init__(self, broker, topic):
        StreamHandler.__init__(self)
        self.broker = broker
        self.topic = topic

        # Kafka Broker Configuration
        self.kafka_broker = KafkaSend(broker)

    def emit(self, record):
        msg = self.format(record)
        self.kafka_broker.send(msg, self.topic)
