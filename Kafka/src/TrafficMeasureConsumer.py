from confluent_kafka import Consumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import SerializationContext, MessageField
import time 

class TrafficMeasureConsumer:
    def __init__(self, topic: str):
        self.schema_registry_client = self.create_schema_registry_client()
        self.consumer = self.create_consumer()
        self.topic = topic

    def create_schema_registry_client(self):
        schema_registry_conf = {'url': 'http://localhost:8081'}
        return SchemaRegistryClient(schema_registry_conf)

    def create_consumer(self):

        with open('./src/TrafficMeasure.avsc', 'r') as f:
            schema_str = f.read()
        self.deserializer = AvroDeserializer(self.schema_registry_client, schema_str)

        consumer_conf = {
            'bootstrap.servers': 'localhost:9092',
            'group.id': 'traffic-measure-consumer',
            'auto.offset.reset': 'earliest'
        }
        return Consumer(consumer_conf)
    
    def consume(self):
        self.consumer.subscribe([self.topic])
        try:
            while True:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    print(f"Error: {msg.error()}")
                    continue
                # Deserialize the message
                value = self.deserializer(msg.value(), SerializationContext(self.topic, MessageField.VALUE))
                print(msg.headers())
                print(value)
        except KeyboardInterrupt:
            self.consumer.close()
            print("Consumer closed")
   
def main():
    consumer = TrafficMeasureConsumer("traffic-measures")
    consumer.consume()

if __name__ == "__main__":
    main()