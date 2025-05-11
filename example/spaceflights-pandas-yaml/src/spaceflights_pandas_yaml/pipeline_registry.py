"""Project pipelines."""

from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline
from kedro_brass.project import find_pipelines as find_yaml_pipelines


def register_pipelines() -> dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    pipelines = find_pipelines(raise_errors=False)
    yaml_pipelines = find_yaml_pipelines()
    # https://github.com/kedro-org/kedro/issues/2526
    pipelines["__default__"] = sum(pipelines.values(), start=Pipeline([])) + sum(
        yaml_pipelines.values(), start=Pipeline([])
    )
    return pipelines
