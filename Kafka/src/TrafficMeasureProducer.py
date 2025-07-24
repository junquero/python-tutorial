import confluent_kafka
import avro.schema
from avro.io import DatumWriter, BinaryEncoder
import time
import io
from confluent_kafka.schema_registry import SchemaRegistryClient, SchemaRegistryError, Schema

class TrafficMeasureProducer:
    def __init__(self, topic: str):
        self.producer = confluent_kafka.Producer({
            "bootstrap.servers": "localhost:9092",
            "group.id": "traffic-measure-producer",
        })
        self.topic = topic
        self.schema_str = open("./src/TrafficMeasure.avsc", "r").read()
        self.schema = avro.schema.parse(self.schema_str)
        self.schema_registry_client = SchemaRegistryClient({
            "url": "http://localhost:8081"
        })
        # Catch the error if the schema is not registered
        try:
            # Check if the schema is already registered
            latest_version = self.schema_registry_client.get_latest_version(self.topic)
            # Get schema id from the latest version
            self.schema_id = latest_version.schema_id
            print(f"Got existing Schema id: {self.schema_id}")
        except SchemaRegistryError as e:
            # Register the schema
            self.schema_id = self.schema_registry_client.register_schema(
                self.topic,
                Schema(self.schema_str, "AVRO")
            )
            print(f"Registered Schema id: {self.schema_id}")


    def produce(self, traffic_measure):
        # Producer the traffic measure to the Kafka topic as avro format
        # Create a writer for the avro schema
        writer = DatumWriter(self.schema)
        # Create a buffer for the avro data
        buffer = io.BytesIO()
        encoder = BinaryEncoder(buffer) 
        # Write the traffic measure to the buffer
        writer.write(traffic_measure, encoder)
        # Produce the traffic measure to the Kafka topic
        self.producer.produce(self.topic, buffer.getvalue(), schema_id=self.schema_id)
        print(f"Produced traffic measure to the Kafka topic: {self.topic}")
    
    def close(self):
        self.producer.flush()


def main():
    producer = TrafficMeasureProducer("traffic-measures")
    # Create a TrafficMeasure object
    traffic_measure = {
            "timestamp": int(time.time() * 1000),
            "average_speed": 40.0,
            "vehicle_count": 10,
            "occupancy_percent": 0.5,
            "location_geojson": "POINT(10.0 10.0)" }

    # Produce the traffic measure to the Kafka topic
    producer.produce(traffic_measure)

    producer.close()

if __name__ == "__main__":
    main()

