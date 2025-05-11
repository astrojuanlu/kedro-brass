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
$ uv add kedro-brass[cli,migrate]
```

> ![WARNING] ⚠️
> The step above doesn't actually work because there's no real `kedro-brass`
> release on PyPI yet.
> If you want to add it to your project right now, use this instead:
> `uv pip install "kedro-brass[cli,migrate] @ https://github.com/astrojuanlu/kedro-brass.git"`

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

Kedro-Brass includes 3 main things:

- A custom `create_pipeline` function that understands YAML-defined pipelines,
- A `kedro-brass pipeline create <pipeline_name>` CLI command that
  creates a YAML-defined pipeline according to its expected structure,
- And a `kedro-brass pipeline migrate <pipeline_name>` CLI command that
  migrates an existing Python-based pipeline to a YAML-defined one.

There are 2 ways of authoring YAML-defined pipelines:

### Explicit configuration

A single `pipeline.yaml` file containing all the information:

```yaml
# src/<your_package>/pipelines/<pipeline_name>/pipeline.yaml
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

### Node list configuration

A `pipeline.yaml` file that references nodes defined in a `nodes.yaml` file:

```yaml
# src/<your_package>/pipelines/<pipeline_name>/pipeline.yaml
nodes:
- compare_passenger_capacity_exp
- compare_passenger_capacity_go
- create_confusion_matrix

# src/<your_package>/pipelines/<pipeline_name>/nodes.yaml
compare_passenger_capacity_exp:
  func: compare_passenger_capacity_exp
  inputs: preprocessed_shuttles
  outputs: shuttle_passenger_capacity_plot_exp

compare_passenger_capacity_go:
  func: compare_passenger_capacity_go
  inputs: preprocessed_shuttles
  outputs: shuttle_passenger_capacity_plot_go

create_confusion_matrix:
  func: spaceflights_pandas_yaml.pipelines.reporting.nodes.create_confusion_matrix
  inputs: companies
  outputs: dummy_confusion_matrix
```

These files can be created manually, or with the help of the CLI.

> ![WARNING] ⚠️
> At the moment, node list configuration is not implemented in `kedro-brass migrate`.

For an example of a Spaceflights-like project that contains 1 Python pipeline,
1 YAML pipeline with explicit configuration,
and 1 YAML pipeline with a node list configuration,
check out the `examples/` directory.

## FAQ

### What's the status of the project?

This was created on a whim, mostly as fun weekend experiment.
It might or might not be maintained in the future.

This is **not** an official product by the Kedro team.

### Do you accept contributions?

Rather than contributing to this project, consider forking it
and making it your own.
(See also "status" FAQ item below.)

Pull requests might or might not be accepted.

### What's missing?

Lots of things are missing, including:

- Tests
- A fully working CI
- An actual release
- Not depending on [another experimental package](https://github.com/AlpAribal/kedro-inspect/)
  for the pipeline migration step
- Code quality improvements
- Support for tags, namespaces, and possibly other features

Some things however are deliberately out of scope, including:

- Storing the YAML files under `conf/` ❌
  - Why? Because [pipeline structure isn't configuration](https://github.com/kedro-org/kedro/issues/770)

### Why that name?

If you know, you know.

## Development

We use `uv` for everything, `pytest` for tests, and not much else.
There be dragons.

Originally based on [`copier-pylib`](https://github.com/astrojuanlu/copier-pylib)
by yours truly.
