from unittest.mock import mock_open, patch
from modbag.model_runner import ModelRunner

class DummyModelRunner(ModelRunner):
    def run(self):
        pass

def test_load_config():
    fake_yaml = """
        mode: online
        online:
          output:
            kafka:
              bootstrap_servers: "localhost:9092"
              topic: "test-topic"
              group_id: "test-group"
        model_path: "fake_model.joblib"
        """
    with patch("builtins.open", mock_open(read_data=fake_yaml)):
        with patch("joblib.load") as mock_joblib_load:
            mock_joblib_load.return_value = "dummy_model_object"
            runner = DummyModelRunner(config_path="fake_config.yaml")
            assert runner.config["mode"] == "online"
            assert runner.kafka_conf["topic"] == "test-topic"
            assert runner.kafka_conf["bootstrap_servers"] == "localhost:9092"
            mock_joblib_load.assert_called_once_with("fake_model.joblib")
