import random
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka import SerializingProducer
import time

class TrafficMeasureProducer:
    def create_schema_registry_client(self):
        schema_registry_conf = {'url': 'http://localhost:8081'}
        return SchemaRegistryClient(schema_registry_conf)
    
    # Define how to convert your dict to something AvroSerializer can use
    def dict_to_avro(self,obj, ctx):
        return obj

    def create_producer(self):

        # Read Avro schema as string
        with open('./src/TrafficMeasure.avsc', 'r') as f:
            schema_str = f.read()


        avro_serializer = AvroSerializer(
            self.schema_registry_client,
            schema_str,
            self.dict_to_avro
        )

        producer_conf = {
            'bootstrap.servers': 'localhost:9092',
#            'key.serializer': StringSerializer('utf_8'),
            'value.serializer': avro_serializer,
            'group.id': 'traffic-measure-producer'
        }

        return SerializingProducer(producer_conf)

    def __init__(self, topic: str):
        self.schema_registry_client = self.create_schema_registry_client()
        self.producer = self.create_producer()
        self.topic = topic


    def produce(self, traffic_measure):
        self.producer.produce(
            topic=self.topic,
            key=str(traffic_measure["timestamp"]),
            value=traffic_measure,
            headers=[("organization", "CNP"), ("source", "traffic-measure-producer")]
        )
    
    def close(self):
        self.producer.flush()


def main():
    # Create a TrafficMeasureProducer object
    tm_producer = TrafficMeasureProducer("traffic-measures")

    # Produce batch of traffic measures
    for i in range(100):
        # Create a TrafficMeasure object
        traffic_measure = {
                "timestamp": int(time.time() * 1000),
                "average_speed": random.randint(0, 100),
                "vehicle_count": random.randint(0, 100),
                "occupancy_percent": random.randint(0, 100),
                "location_geojson": "POINT(" + str(random.randint(0, 1000)/10.0) + " " + str(random.randint(0, 1000)/10.0) + ")" }

        # Produce the traffic measure to the Kafka topic
        tm_producer.produce(traffic_measure)

    print(f"Produced traffic measures to the Kafka topic: {tm_producer.topic}")

    # Close the producer
    tm_producer.close()

if __name__ == "__main__":
    main()

