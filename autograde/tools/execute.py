

import subprocess
from os import PathLike
from pathlib import Path

from autograde.tools.result import ExecuteResult


def execute_program(
        executable_path: PathLike, cwd: PathLike,
        program_input=None) -> ExecuteResult:
    """Executes the program indicated on the path.

    args:
        executable_path: The program to execute.
        cwd: The folder to execute the program from.
    returns:
        Returns the result of running the program.
    """
    executable_path = Path(executable_path)
    proc_status = subprocess.run(
        [str(executable_path.resolve())], cwd=cwd,
        capture_output=True, text=True, input=program_input
    )
    return ExecuteResult(
        proc_status.stdout, proc_status.stderr,
        proc_status.returncode)
