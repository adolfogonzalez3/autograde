"""Tests the build module's functions."""

import autograde.components as components
import autograde.tools.build as build_tools
import autograde.tools.execute as execute_tools


def test_execute(tmp_path, simple_program):
    """Tests CppProgram compile method."""
    cpp_program = components.CppProgram(tmp_path)
    cpp_program.collect_source()
    cpp_program.set_entry_point()
    compile_result = build_tools.compile_cpp(cpp_program, target_path=tmp_path)
    execute_result = execute_tools.execute_program(
        compile_result[0], tmp_path
    )
    assert execute_result.return_code == 0
    assert bool(execute_result)
