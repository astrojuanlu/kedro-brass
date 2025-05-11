import pytest
from pydantic import ValidationError

from kedro_brass.project import PipelineConfig


def test_valid_explicit_pipelines_config():
    data_science = {
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
    }

    pipeline_config = PipelineConfig.validate_python(data_science)
    assert len(pipeline_config.nodes) == 3
    assert pipeline_config.nodes[0].func == "split_data"


def test_valid_node_names_pipelines_config():
    reporting = {
        "nodes": [
            "compare_passenger_capacity_exp",
            "compare_passenger_capacity_go",
            "create_confusion_matrix",
        ]
    }
    pipeline_config = PipelineConfig.validate_python(reporting)
    assert len(pipeline_config.nodes) == 3


def test_invalid_pipelines_config():
    invalid_data_science = {
        "nodes": [
            {
                "unexpected": "data",
            }
        ]
    }

    with pytest.raises(ValidationError, match="4 validation errors"):
        PipelineConfig.validate_python(invalid_data_science)
