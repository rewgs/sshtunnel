from pathlib import Path

default_dir: Path = Path.home().joinpath(".ssh")
default_file: Path = default_dir.joinpath("config")

__all__ = ["default_dir", "default_file"]
