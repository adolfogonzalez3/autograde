"""
A module that has functions to compile and execute programs with containers."""

import subprocess
from autograde.components.cpp_components import CppProgram


def compile_cpp(program: CppProgram):
    """Compiles a cpp program.

    args:
        program: A cpp program that can be compiled.
    """
    subprocess.run(
        [
            "docker", "run", "--rm", "-v", f"{current_path}:/foo:ro",
            "cpp-container"
        ]
    )
