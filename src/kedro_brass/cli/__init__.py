from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import cappa
from cappa import Subcommands
from kedro.framework.startup import bootstrap_project

from ..create import create_pipeline as do_create_pipeline
from ..migrate import migrate_pipeline as do_migrate_pipeline


def create_pipeline(args: Create) -> None:
    do_create_pipeline(args.pipeline_name, bootstrap_project(Path.cwd()))


def migrate_pipeline(args: Migrate) -> None:
    do_migrate_pipeline(
        args.pipeline_name, args.separate_nodes, bootstrap_project(Path.cwd())
    )


@cappa.command(invoke=create_pipeline)
class Create:
    pipeline_name: str


@cappa.command(invoke=migrate_pipeline)
class Migrate:
    pipeline_name: str
    separate_nodes: bool = False


@dataclass
class Pipeline:
    subcommands: Subcommands[Create | Migrate]


@dataclass
class KedroBrass:
    pipeline: Subcommands[Pipeline]


def main():
    cappa.invoke(KedroBrass)
