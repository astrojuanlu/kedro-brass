import importlib.resources
import typing as t
import warnings

from kedro.pipeline import Pipeline
from kedro.pipeline.node import Node
from pydantic import BaseModel, RootModel
from yaml import safe_load


class NodeConfig(BaseModel):
    func: str
    inputs: list[str] | str | None
    outputs: list[str] | str | None
    name: str | None = None


class PipelineConfig(BaseModel):
    nodes: list[NodeConfig]
    tags: list[str] | None = None


class PipelineNodeNamesConfig(BaseModel):
    nodes: list[str]
    tags: list[str] | None = None


class PipelinesConfig(RootModel):
    root: dict[str, PipelineConfig | PipelineNodeNamesConfig]


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


def _build_pipeline(
    pipeline_config: PipelineConfig | PipelineNodeNamesConfig,
) -> Pipeline:
    if isinstance(pipeline_config, PipelineConfig):
        nodes = [
            Node(
                func=_resolve_function(node.func),
                inputs=node.inputs,
                outputs=node.outputs,
                name=node.name,
            )
            for node in pipeline_config.nodes
        ]
        return Pipeline(nodes)
    elif isinstance(pipeline_config, PipelineNodeNamesConfig):
        raise NotImplementedError(
            "Only pipeline configurations with nodes are supported.",
        )


def find_pipelines(
    raise_errors: bool = False, package_name: str | None = None
) -> dict[str, Pipeline]:
    if package_name is None:
        from kedro.framework.project import PACKAGE_NAME

        package_name = PACKAGE_NAME

    if not package_name:
        raise ValueError("Kedro project not configured and no package name provided.")

    try:
        pipelines_package = importlib.resources.files(f"{PACKAGE_NAME}.pipelines")
    except ModuleNotFoundError:
        if raise_errors:
            raise
        else:
            warnings.warn(
                f"Error found while importing '{PACKAGE_NAME}.pipelines', "
                "no pipelines will be registered.",
                UserWarning,
            )
            return {}

    pipelines_dict = {}
    for pipeline_dir in pipelines_package.iterdir():
        if (pipeline_yaml_file := (pipeline_dir / "pipeline.yaml")).is_file():
            with pipeline_yaml_file.open("r") as fh:
                pipeline_config_dict = safe_load(fh)

            pipeline_config = PipelinesConfig.model_validate(pipeline_config_dict)
            for pipeline_name, pipeline_config in pipeline_config.root.items():
                try:
                    pipelines_dict[pipeline_name] = _build_pipeline(pipeline_config)
                except Exception as e:
                    if raise_errors:
                        raise
                    else:
                        warnings.warn(
                            f"Error found while building pipeline '{pipeline_name}': {e}",
                            UserWarning,
                        )
                        continue

    return pipelines_dict
