# Static Import Analysis for Pure Python Projects

Code that uses the built-in `ast` module to do static import analysis for pure Python projects.

Assumptions:

- Pure Python project with the only importable modules being Python files and directories containing Python files (e.g. no `.so` files or `.pyd` files).
- If a directory is an importable module (a package), it *must* have an `__init__.py` file within it.
- No Python file manipulates `sys.path` or `sys.modules`.

The main entry point function is `do_static_import_analysis_for_pure_python_project` in `do_static_import_analysis_for_pure_python_project.py`. This function accepts `project_path: str` as a parameter and returns the following values:

- `module_name_to_file_path_dict: dict[str, str]`, which maps *module names* to *file paths*, e.g., `'thefuck': '/home/abbas/thefuck/thefuck/__init__.py'`.
- `module_name_to_defined_function_name_set_dict: dict[str, set[str]]`, which maps *module names* to names of functions *defined* (i.e., not imported) in that module, e.g., `'thefuck.rules.java': {'get_new_command', 'match'}`.
- `module_name_to_defined_class_name_set_dict: dict[str, set[str]]`, which maps *module names* to names of classes *defined* (i.e., not imported) in that module, e.g., `'thefuck.types': {'Command', 'CorrectedCommand', 'Rule'}`.
- `imported_external_module_name_set: set[str]`, a set of *module names* which are `Import`'ed or `ImportFrom`'ed by Python files within the project but are *not* within `module_name_to_file_path_dict` (i.e., they most likely are names of external modules), e.g., `{'CommandNotFound', 'anydbm', 'argparse', 'array', 'atexit', 'backports.shutil_get_terminal_size', 'collections'}`.
