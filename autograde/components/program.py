"""Module that abstracts components of programs."""
from pathlib import Path
from os import PathLike
from abc import abstractmethod
from typing import Union, Optional, Set, Tuple


class Source(object):
    """Represents a source file of a program."""

    def __init__(self, *path_to_source: Union[str, PathLike]):
        self.path = Path(*path_to_source)

    @property
    @abstractmethod
    def functions(self) -> Tuple[(str, str, Tuple[str, ...])]:
        """Returns a list of function signatures from source."""

    @property
    @abstractmethod
    def comments(self) -> Tuple[str]:
        """Returns a list of comments from source."""

    @abstractmethod
    def is_entry_point(self) -> bool:
        """Returns True if the file can be the entry point for a program."""

    def __repr__(self) -> str:
        """Returns a string representation of the Source object."""
        return f"{type(self).__name__}({self.path})"

    def __hash__(self) -> int:
        """Use the underlying path object's __hash__ method."""
        return self.path.__hash__()

    def __eq__(self, other) -> bool:
        """Use the underlying path object's __eq__ method."""
        return self.path == other

    def __lt__(self, other) -> bool:
        """Use the underlying path object's __lt__ method."""
        return self.path.__lt__(other)


class Program(object):
    """Represents that state of a program."""

    def __init__(self, *build_paths: PathLike):
        self.entry_point: Optional[Source] = None
        self.build_paths: Set[Path] = {Path(sp) for sp in build_paths}
        self.source_files: Set[Source] = set()

    def set_entry_point(self, source_file: Optional[PathLike] = None):
        """Sets the entry point for the program.

        args:
            source_file: The path to the source file which serves as the entry
                point of the program. If None then choose a suitable entry
                point from the current source files.
        """
        if source_file is not None:
            self.entry_point = self.source_type(source_file)
        else:
            self.entry_point = next(
                (sf for sf in self.source_files if sf.is_entry_point()), None
            )

    def add_build_path(self, build_path: PathLike):
        """
        Add an existing path to look for source files.

        :build_path: A path which may contain source files.
        """
        self.build_paths.add(Path(build_path))

    def add_source(self, source_file: Source):
        """
        Add a source file to the program.

        args:
            source_file: A source file.
        """
        self.source_files.add(source_file)

    def collect_source(self):
        """Collect all source files from build paths. """
        for build_path in self.build_paths:
            for ext in self.get_extensions():
                self.source_files.update(
                    self.source_type(path)
                    for path in build_path.rglob(f'*{ext}')
                )

    def __repr__(self):
        """Return a string representation of the program."""
        return f'<Program({self.entry_point})>'

    @abstractmethod
    def get_extensions(self):
        """Get the extensions that are needed for compiling the program."""

    @property
    @abstractmethod
    def source_type(self):
        """Returns the Source subclass for program type."""
