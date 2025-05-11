# kedro-brass

[![Documentation Status](https://readthedocs.org/projects/kedro-brass/badge/?version=latest)](https://kedro-brass.readthedocs.io/en/latest/?badge=latest)
[![Code style: ruff-format](https://img.shields.io/badge/code%20style-ruff_format-6340ac.svg)](https://github.com/astral-sh/ruff)
[![PyPI](https://img.shields.io/pypi/v/kedro-brass)](https://pypi.org/project/kedro-brass)

Write your Kedro pipelines and nodes in YAML.

## Quickstart

Start from a spaceflights starter:

```
$ uvx kedro new --starter spaceflights-pandas --name spaceflights-pandas-yaml
$ cd spaceflights-pandas-yaml
```

Add `kedro-brass` to your project:

```
$ uv add kedro-brass[cli]
```

And migrate the `data_science` pipeline to YAML:

```
$ uv run kedro-brass pipeline migrate data_science
```

Observe that the new directory structure is as follows:

```
src/spaceflights_pandas_yaml/pipelines/data_science/
├── __init__.py
├── nodes.py
├── pipeline.py.bak
└── pipeline.yaml
```

And that the contents of `pipeline.yaml` match the structure of your pipeline:

```yaml
nodes:
- func: split_data
  inputs: [model_input_table, params:model_options]
  outputs: [X_train, X_test, y_train, y_test]
  name: split_data_node
- func: train_model
  inputs: [X_train, y_train]
  outputs: regressor
  name: train_model_node
- func: evaluate_model
  inputs: [regressor, X_test, y_test]
  outputs: null
  name: evaluate_model_node
```

From this point, continue using Kedro as normal:

```
$ uv run kedro registry list
...
- __default__
- data_processing
- data_science
- reporting
$ uv run kedro run -p data_science
...
                    INFO     Pipeline execution completed successfully.
```

## Usage

(TBC)

## Development

To run style checks:

```
$ uv tool install pre-commit
$ pre-commit run -a
```
