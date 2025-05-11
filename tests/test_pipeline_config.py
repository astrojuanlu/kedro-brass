import pytest
from pydantic import ValidationError

from kedro_brass.project import PipelinesConfig


def test_valid_pipelines_config():
    valid_data = {
        "data_science": {
            "nodes": [
                {
                    "func": "split_data",
                    "inputs": ["model_input_table", "params:model_options"],
                    "outputs": ["X_train", "X_test", "y_train", "y_test"],
                    "name": "split_data_node",
                },
                {
                    "func": "train_model",
                    "inputs": ["X_train", "y_train"],
                    "outputs": "regressor",
                    "name": "train_model_node",
                },
                {
                    "func": "evaluate_model",
                    "inputs": "regressor",
                    "outputs": ["X_test", "y_test"],
                },
            ]
        },
        "reporting": {
            "nodes": [
                "compare_passenger_capacity_exp",
                "compare_passenger_capacity_go",
                "create_confusion_matrix",
            ]
        },
    }

    pipelines_config = PipelinesConfig.model_validate(valid_data)
    assert "data_science" in pipelines_config.root
    assert "reporting" in pipelines_config.root
    assert len(pipelines_config.root["data_science"].nodes) == 3
    assert len(pipelines_config.root["reporting"].nodes) == 3
    assert pipelines_config.root["data_science"].nodes[0].func == "split_data"
    assert pipelines_config.root["data_science"].nodes[0].inputs == [
        "model_input_table",
        "params:model_options",
    ]
    assert pipelines_config.root["data_science"].nodes[0].outputs == [
        "X_train",
        "X_test",
        "y_train",
        "y_test",
    ]


def test_invalid_pipelines_config():
    invalid_data = {
        "data_science": {
            "nodes": [
                {
                    "unexpected": "data",
                }
            ]
        }
    }

    with pytest.raises(
        ValidationError, match="4 validation errors for PipelinesConfig"
    ):
        PipelinesConfig.model_validate(invalid_data)
