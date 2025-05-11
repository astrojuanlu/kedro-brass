import importlib.metadata
import typing as t

from kedro.framework.startup import ProjectMetadata
from kedro.pipeline import Pipeline
from kedro_inspect.pipeline import InspectedPipeline
from structlog import get_logger
from yaml import safe_dump

from .project import PipelineExplicitConfig

logger = get_logger(__name__)


def inspect_pipeline(pipeline: Pipeline) -> dict[str, t.Any]:
    inspected_pipeline = InspectedPipeline.from_kedro_pipeline(pipeline)
    return inspected_pipeline.to_dict()


def migrate_pipeline(
    pipeline_name: str, separate_nodes: bool, metadata: ProjectMetadata
) -> None:
    if separate_nodes:
        raise NotImplementedError("The 'separate_nodes' option is not implemented yet")

    from kedro.framework.project import pipelines

    if pipeline_name not in pipelines:
        raise ValueError(f"Pipeline '{pipeline_name}' not found in the project")

    pipeline_dict = inspect_pipeline(pipelines[pipeline_name])

    # TODO: Refactor to avoid code duplication with create_pipeline
    pipeline_dir = (
        metadata.source_dir / metadata.package_name / "pipelines" / pipeline_name
    )
    pipeline_py = pipeline_dir / "pipeline.py"
    pipeline_bak = pipeline_dir / "pipeline.py.bak"

    if pipeline_py.exists():
        pipeline_py.rename(pipeline_bak)
    else:
        logger.warning(f"Pipeline file '{pipeline_py}' does not exist")

    init_py = pipeline_dir / "__init__.py"
    init_bak = init_py.with_suffix(".bak")

    if init_py.exists():
        init_py.rename(init_bak)
    else:
        logger.warning(f"Init file '{init_py}' does not exist")

    header = f"""\"\"\"
This is a boilerplate pipeline {pipeline_name}.
Generated using Kedro-Brass {importlib.metadata.version("kedro-brass")}.
\"\"\"
"""

    init_py.write_text(
        header
        + """
from kedro_brass.project import create_pipeline_factory

create_pipeline = create_pipeline_factory(__name__)

__all__ = ["create_pipeline"]
"""
    )

    pipeline_yaml = pipeline_dir / "pipeline.yaml"
    pipeline_config = PipelineExplicitConfig(
        nodes=[
            {
                "func": node["function"]["func"],
                "inputs": node["inputs"],
                "outputs": node["outputs"],
                "name": node["name"],
            }
            for node in pipeline_dict["nodes"]
        ]
    )

    with pipeline_yaml.open("w") as yaml_file:
        safe_dump(pipeline_config.model_dump(), yaml_file)

    logger.info(
        "Pipeline migrated successfully",
        pipeline_name=pipeline_name,
        pipeline_dir=str(pipeline_dir),
    )
