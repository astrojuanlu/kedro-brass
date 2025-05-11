import importlib.metadata

import structlog
from kedro.framework.startup import ProjectMetadata

logger = structlog.get_logger(__name__)


def create_pipeline(pipeline_name: str, metadata: ProjectMetadata) -> None:
    """Create a new pipeline directory structure and files."""
    pipelines_dir = metadata.source_dir / metadata.package_name / "pipelines"
    pipeline_dir = pipelines_dir / pipeline_name

    if pipeline_dir.exists():
        raise FileExistsError(f"Pipeline '{pipeline_name}' already exists.")

    # Create pipeline directory
    pipeline_dir.mkdir(parents=True)

    header = f"""\"\"\"
This is a boilerplate pipeline {pipeline_name}
generated using Kedro-Brass {importlib.metadata.version("kedro-brass")}
\"\"\"
"""

    init_file = pipeline_dir / "__init__.py"
    init_file.write_text(
        header
        + """
from kedro_brass.project import create_pipeline_factory

create_pipeline = create_pipeline_factory(__name__)

__all__ = ["create_pipeline"]
"""
    )

    nodes_file = pipeline_dir / "nodes.py"
    nodes_file.write_text(
        header
        + """
def passthrough_node(foo):
    return foo
"""
    )

    pipeline_yaml = pipeline_dir / "pipeline.yaml"
    pipeline_yaml.write_text("""nodes:
- func: passthrough_node  # Comes from nodes.py
  inputs: ds1  # Must be defined in catalog.yml
  outputs: ds2
""")

    logger.info(
        "Pipeline created successfully",
        pipeline_name=pipeline_name,
        pipeline_dir=str(pipeline_dir),
    )
