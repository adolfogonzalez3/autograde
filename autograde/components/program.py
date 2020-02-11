"""Module that abstracts components of programs."""
from pathlib import Path
from os import PathLike
from abc import abstractmethod
from typing import List, Union, Optional, Set, Tuple


class Check:
    def get_error(self) -> List[str]:
        """Return a list of errors."""
        return []

    def get_warning(self) -> List[str]:
        """Return a list of warnings."""
        return []

    def is_error(self) -> bool:
        """Return True if check found an error."""
        return not self.get_error()

    def is_warning(self) -> bool:
        """Return True if check found a warning."""
        return not self.get_warning()

    def __bool__(self) -> bool:
        """Return True if no errors or warngins."""
        return self.is_error() and self.is_warning()


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

    def __init__(self, root_path: PathLike, entry_point: Optional[PathLike] = None):
        self.entry_point = None
        if entry_point is not None:
            self.entry_point = Path(entry_point)
        self.root_path = root_path
        self.build_paths: Set[Path] = {Path(root_path)}
        self.source_files: Set[Source] = set()
        self.collect_source()

    def add_build_path(self, build_path: Path):
        """
        Add an existing path to look for source files.

        :build_path: A path which may contain source files.
        """
        self.build_paths.add(build_path)
        return self

    def add_source(self, source_file: Source):
        """
        Add a source file to the program.

        args:
            source_file: A source file.
        """
        self.source_files.add(source_file)
        return self

    def collect_source(self):
        """Collect source files from build paths. """
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

    @abstractmethod
    def check(self):
        """Check the program's source files."""
    @abstractmethod
    def compile(self, args=None, kwargs=None):
        """Compile the program with the given arguments."""
    @abstractmethod
    def execute(self, args=None, kwargs=None):
        """Execute the program with given arguments."""
