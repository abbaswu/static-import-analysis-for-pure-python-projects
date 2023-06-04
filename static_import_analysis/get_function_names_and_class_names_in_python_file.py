import ast

from .get_ast_for_python_file import get_ast_for_python_file


def get_function_names_and_class_names_in_python_file(file_path: str) -> tuple[set[str], set[str]]:
    ast_for_file = get_ast_for_python_file(file_path)

    function_names: set[str] = set()
    class_names: set[str] = set()

    for node in ast_for_file.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            function_names.add(node.name)
        elif isinstance(node, ast.ClassDef):
            class_names.add(node.name)

    return function_names, class_names
