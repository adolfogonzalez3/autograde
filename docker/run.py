"""A script for running the autograder."""
import json
import argparse
from pathlib import Path

from autograde import CppProgram
from autograde.tools import compile_cpp, execute_program


def get_args():
    """Gets command line arguments for the script."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'build_info', help='Path to the assignments.')
    return parser.parse_args()


def main():
    args = get_args()
    target_path = Path()
    build_path = Path("/", "build")
    build_info = json.loads(args.build_info)
    program = CppProgram(*build_info["source_files"])
    program.set_entry_point(build_info["entry_point"])
    print("Compiling...")
    compile_result = compile_cpp(program, target_path)

    print("STDOUT")
    print(compile_result.stdout)
    print("STDERR")
    print(compile_result.stderr)
    if compile_result.executable is not None:
        print("Executing...")
        execute_result = execute_program(
            compile_result.executable, cwd=target_path,
            program_input=build_info["program_input"])
        print("STDOUT:")
        print(execute_result.stdout)
        print("STDERR")
        print(execute_result.stderr)
    else:
        print("Compiling Unsuccessful")


if __name__ == "__main__":
    print("Something")
    main()
