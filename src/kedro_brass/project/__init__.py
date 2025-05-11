import importlib.resources
import typing as t

from kedro.pipeline import Pipeline
from kedro.pipeline.node import Node
from pydantic import BaseModel, RootModel, TypeAdapter
from yaml import safe_load


class ExplicitNodeConfig(BaseModel):
    func: str
    inputs: list[str] | str | None
    outputs: list[str] | str | None
    name: str | None = None


class FullNodeConfig(ExplicitNodeConfig):
    name: str | None = None


class PipelineExplicitConfig(BaseModel):
    nodes: list[FullNodeConfig]
    tags: list[str] | None = None


class PipelineNodeNamesConfig(BaseModel):
    nodes: list[str]
    tags: list[str] | None = None


PipelineConfig = TypeAdapter(PipelineExplicitConfig | PipelineNodeNamesConfig)


class NodesConfig(RootModel):
    root: dict[str, ExplicitNodeConfig]


def _resolve_function(func_name: str, module_name: str | None = None) -> t.Callable:
    if "." in func_name:
        module_name, func_name = func_name.rsplit(".", 1)
    elif not module_name:
        raise ValueError(
            "Module name must be provided when function name does not contain a dot."
        )

    module = importlib.import_module(module_name)
    func = getattr(module, func_name)
    return func


def _find_pipeline(pipeline_package_name: str) -> Pipeline:
    pipeline_package = importlib.resources.files(pipeline_package_name)
    if (pipeline_yaml_file := (pipeline_package / "pipeline.yaml")).is_file():
        with pipeline_yaml_file.open("r") as fh:
            pipeline_config_dict = safe_load(fh)

        pipeline_config = PipelineConfig.validate_python(pipeline_config_dict)
        if isinstance(pipeline_config, PipelineNodeNamesConfig):
            if (node_yaml_file := (pipeline_package / "nodes.yaml")).is_file():
                with node_yaml_file.open("r") as fh:
                    node_config_dict = safe_load(fh)

                node_config = NodesConfig.model_validate(node_config_dict)
                nodes = [
                    Node(
                        func=_resolve_function(
                            node.func, pipeline_package_name + ".nodes"
                        ),
                        inputs=node.inputs,
                        outputs=node.outputs,
                        name=node_name,
                    )
                    for node_name, node in node_config.root.items()
                ]
        else:
            nodes = [
                Node(
                    func=_resolve_function(node.func, pipeline_package_name + ".nodes"),
                    inputs=node.inputs,
                    outputs=node.outputs,
                    name=node.name,
                )
                for node in pipeline_config.nodes
            ]

        return Pipeline(nodes, tags=pipeline_config.tags)

    raise ValueError(f"No valid pipeline found in package '{pipeline_package_name}'.")


def create_pipeline_factory(package_name: str) -> t.Callable[[], Pipeline]:
    def create_pipeline() -> Pipeline:
        return _find_pipeline(package_name)

    return create_pipeline
