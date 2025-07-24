import random
import uuid
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka import SerializingProducer
import time

class TrafficMeasureProducer:
    def __init__(self, topic: str):
        self.schema_registry_client = self.create_schema_registry_client()
        self.producer = self.create_producer()
        self.topic = topic
        self.organizations = ["CNP", "DGT"]
        self.areas = ["CAD", "SEV", "MAL", "HUE", "COR", "JAE"]

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
            'value.serializer': avro_serializer
        }

        return SerializingProducer(producer_conf)

    def get_random_organization(self):
        return random.choice(self.organizations)

    def get_random_area(self):
        return random.choice(self.areas)

    def produce(self, traffic_measure):
        self.producer.produce(
            topic=self.topic,
            key=str(uuid.uuid4()),
            value=traffic_measure,
            headers=[("organization", self.get_random_organization()), ("area", self.get_random_area())]
        )
    
    def close(self):
        self.producer.flush()


def main():
    # Create a TrafficMeasureProducer object
    tm_producer = TrafficMeasureProducer("traffic-measures")
    traffic_measures_list = []

    # Produce batch of traffic measures
    for i in range(100):
        # Create a TrafficMeasure object
        traffic_measure = {
                "timestamp": int(time.time() * 1000),
                "average_speed": random.randint(0, 100),
                "vehicle_count": random.randint(0, 100),
                "occupancy_percent": random.randint(0, 100),
                "location_geojson": "POINT(" + str(random.randint(0, 1000)/10.0) + " " + str(random.randint(0, 1000)/10.0) + ")" }

        traffic_measures_list.append(traffic_measure)

    for traffic_measure in traffic_measures_list:
        # Produce the traffic measure to the Kafka topic
        tm_producer.produce(traffic_measure)

    # Close the producer
    tm_producer.close()

    print(f"Produced traffic measures to the Kafka topic: {tm_producer.topic}")

if __name__ == "__main__":
    main()

