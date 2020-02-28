"""Module that contains the Result class."""

from collections import namedtuple
from typing import List, Tuple, Union, Optional

_Result = namedtuple("_Result", ["stdout", "stderr", "return_code"])
_CompileResult = namedtuple(
    "_CompileResult", ["executable", "stdout", "stderr", "return_code"]
)


class Result(_Result):
    __slots__ = ()

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
        return self.return_code == 0


class CompileResult(_CompileResult):
    __slots__ = ()

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
        return self.return_code == 0
