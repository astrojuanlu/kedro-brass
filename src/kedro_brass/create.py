from kedro.framework.startup import ProjectMetadata


def create_pipeline(pipeline_name: str, metadata: ProjectMetadata) -> None:
    print(f"Creating pipeline: {pipeline_name}")
    print(metadata)
