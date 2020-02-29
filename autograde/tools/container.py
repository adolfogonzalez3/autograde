"""
A module that has functions to compile and execute programs with containers."""

import json
import subprocess
from itertools import chain
from autograde.components.cpp_components import CppProgram

from typing import Optional


def compile_run_cpp(
        program: CppProgram, program_input: Optional[str] = None):
    """Compiles and runs a cpp program and returns the result.

    args:
        program: A cpp program that can be compiled.
    returns:
        Returns a result which contains stdout and stderr for
        compiling and running steps of the program.
    """
    if program.entry_point is None:
        return None
    entry_path = program.entry_point.path
    build_path_map = {
        build_path: f"/build/build_{i}"
        for i, build_path in enumerate(program.build_paths)
    }
    source_files = [
        f"{build_path_map[source_file.path.parent]}/{source_file.path.name}"
        for source_file in program.source_files
    ]
    build_info = {
        "source_files": source_files,
        "program_input": program_input,
        "entry_point": f"{build_path_map[entry_path.parent]}/{entry_path.name}"
    }
    volumes = [
        ("-v", f"{bpath.resolve()}:{mpath}:ro")
        for bpath, mpath in build_path_map.items()
    ]
    command = [
        "docker", "run", "--rm", "-i", "-a", "stdout", "-a", "stderr",
        "-a", "stdin"
    ]
    command.extend(chain.from_iterable(volumes))
    command.append("cpp-container")
    command.append(json.dumps(build_info))
    print(command)
    proc_status = subprocess.run(
        command, capture_output=True, text=True
    )
    print("STDOUT")
    print(proc_status.stdout)
    print("STDERR")
    print(proc_status.stderr)
