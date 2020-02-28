"""A script for running the autograder."""
import argparse
from pathlib import Path

from autograde import CppProgram
from autograde.tools import compile_cpp, execute_program


def get_args():
    """Gets command line arguments for the script."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'path_to_assn', help='Path to the assignments.', type=Path)
    parser.add_argument(
        "--program_input", help="A string which is fed into all programs.",
        default=None, type=lambda x: x.replace("\\n", "\n")
    )
    return parser.parse_args()


def main():
    args = get_args()
    assignment_path = args.path_to_assn
    student_paths = sorted(assignment_path.iterdir())
    for student_path in student_paths:
        program = CppProgram(student_path)
        program.collect_source()
        program.set_entry_point()
        compile_result = compile_cpp(program, student_path)
        print("STDOUT")
        print(compile_result.stdout)
        print("STDERR")
        print(compile_result.stderr)
        if compile_result.executable is not None:
            print("Executing...")
            execute_result = execute_program(
                compile_result.executable, cwd=student_path,
                program_input=args.program_input)
            print("STDOUT:")
            print(execute_result.stdout)
            print("STDERR")
            print(execute_result.stderr)
        else:
            print("Error")
            stdout = compile_result.stdout.split("\n", maxsplit=5)
            stdout = "\n".join(stdout[:5])
            stderr = compile_result.stderr.split("\n", maxsplit=5)
            stderr = "\n".join(stderr[:5])
            print(stdout)
            print(stderr)
        print("Header")
        print('*'*80)
    print("-"*80)


if __name__ == "__main__":
    main()
