from kedro.framework.startup import ProjectMetadata


def migrate_pipeline(
    pipeline_name: str, separate_nodes: bool, metadata: ProjectMetadata
) -> None:
    print(f"Migrating pipeline: {pipeline_name}, separate_nodes: {separate_nodes}")
    print(metadata)
