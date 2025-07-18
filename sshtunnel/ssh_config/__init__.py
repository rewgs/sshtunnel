from pathlib import Path

# TODO: offer to make default_dir if it doesn't exist?
default_dir: Path = Path.home().joinpath(".ssh")
default_file: Path = default_dir.joinpath("config")

__all__ = ["default_dir", "default_file"]
