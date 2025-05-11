"""Complete Data Science pipeline for the spaceflights tutorial"""

from kedro_brass.project import create_pipeline_factory  # NOQA

create_pipeline = create_pipeline_factory(__name__)

__all__ = ["create_pipeline"]
