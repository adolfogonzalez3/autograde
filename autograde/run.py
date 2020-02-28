"""A script for running the autograder."""
import argparse
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor

from autograde import CppProgram

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
    assn_path = args.path_to_assn
    print(args.program_input)
    print("-"*80)
    with ProcessPoolExecutor() as executor:
        students = sorted([
            (student_path, CppProgram(student_path))
            for student_path in assn_path.iterdir()
        ])
        for name, student in students:
            student.collect_source()
            compile_result = student.compile()
            print('*'*80)
            print(f'Student: {name}')
            if compile_result:
                print("Executing...")
                print(student.executable)
                execute_result = student.execute(args.program_input)
                print(execute_result.stdout)
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
            print(student.check())
            #if student.header:
            #    print("EXISTS")
            #else:
            #    print("NOTHING")
            #if result:
            #    print(result.stdout.decode())
            #else:
            #    print("NOTHING")
            print('*'*80)
        # responses = executor.map(compile_and_run, students,
        #                         [trials] * len(students))
    #responses, students, grades = zip(*list(responses))
    # for student, grade in zip(students, grades):
    #    print(f'{student} {sum(grade)} correct out of {len(grade)}')
    print("-"*80)
    # with open(args.output, 'wt') as log:
    #    json.dump(responses, log, indent=4)

if __name__ == "__main__":
    main()
