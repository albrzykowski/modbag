import yaml
import json
import joblib
import logging
from confluent_kafka import Producer, Consumer
from json.decoder import JSONDecodeError
from fastavro import reader, writer, parse_schema, validation
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class ModelRunner(ABC):
    def __init__(self, config_path="config.yaml"):
        self.config = self._load_config(config_path)
        self.mode = self.config.get("mode")
        self.kafka_conf = self._get_kafka_config()
        self._init_kafka()
        self._load_model()

    def _load_config(self, path):
        with open(path, "r") as f:
            return yaml.safe_load(f)

    def _get_kafka_config(self):
        return self.config.get(self.mode, {}).get("output", {}).get("kafka", {})

    def _init_kafka(self):
        if self.kafka_conf:
            logger.info(f"Kafka config: {self.kafka_conf}")
            self.producer = Producer({'bootstrap.servers': self.kafka_conf["bootstrap_servers"]})
            self.consumer = Consumer({
                'bootstrap.servers': self.kafka_conf["bootstrap_servers"],
                'group.id': self.kafka_conf.get("group_id", "model-runner-group"),
                'auto.offset.reset': 'earliest'
            })
            self.consumer.subscribe([self.kafka_conf["topic"]])
        else:
            self.producer = None
            self.consumer = None

    def _load_model(self):
        model_path = self.config.get("model_path", "model.joblib")
        logger.info(f"Loading model from {model_path}")
        self.model = joblib.load(model_path)

    def _read_avro(self, path):
        logger.info(f"Reading data from Avro: {path}")
        with open(path, "rb") as f:
            avro_reader = reader(f)
            return list(avro_reader)

    def _write_avro(self, path, schema_path, records):
        logger.info(f"Writing results to Avro: {path}")
        with open(schema_path, "r") as f:
            schema_dict = json.load(f)
        parsed_schema = parse_schema(schema_dict)
        with open(path, "a+b") as out:
            writer(out, parsed_schema, records)
    
    def _validate_message(self, msg):
        with open(self.config["online"]["input"]["kafka"]["schema_path"]) as f:
            schema_json = json.load(f)
            schema = parse_schema(schema_json)
        return validation.validate(msg, schema)

    @abstractmethod
    def run(self):
        pass
