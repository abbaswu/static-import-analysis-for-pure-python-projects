# Static Import Analysis for Pure Python Projects

Code that uses the built-in `ast` module to do static import analysis for pure Python projects.

Assumptions:

- Pure Python project with the only importable modules being Python files and directories containing Python files (e.g. no `.so` files or `.pyd` files).
- If a directory is an importable module (a package), it *must* have an `__init__.py` file within it.
- No Python file manipulates `sys.path` or `sys.modules`.

The main entry point function is `do_static_import_analysis_for_pure_python_project` in `do_static_import_analysis_for_pure_python_project.py`. This function accepts `project_path: str` as a parameter and returns the following values:

- `module_name_to_file_path_dict: dict[str, str]`, which maps *module names* to *file paths*, e.g., `'thefuck': '/home/abbas/thefuck/thefuck/__init__.py'`.
- `module_name_to_defined_function_name_set_dict: dict[str, set[str]]`, which maps *module names* to names of functions *defined* (i.e., not imported) in that module, e.g., `'thefuck.rules.java': {'get_new_command', 'match'}`.
- `module_name_to_defined_type_name_set_dict: dict[str, set[str]]`, which maps *module names* to names of types (classes) *defined* (i.e., not imported) in that module, e.g., `'thefuck.types': {'Command', 'CorrectedCommand', 'Rule'}`.
- `module_name_to_imported_module_name_set_dict: dict[str, set[str]]`, which maps *module names* to names of modules imported in that module which are in `module_name_to_file_path_dict` (i.e., *within the scope of the project*). All *relative imports* are resolved to *absolute imports* (e.g. the `.` in `from . import logs, const` in the module `thefuck.ui` which is a file becomes `thefuck`).
- `module_name_to_imported_external_module_name_set_dict: dict[str, set[str]]`, which maps *module names* to names of modules imported in that module which are not in `module_name_to_file_path_dict` (i.e., *out of the scope of the project*).


Usage:

Assume we have cloned [`nvbn/thefuck`](https://github.com/nvbn/thefuck) to `/tmp`:

```sh
abbas@abbas-ThinkPad-X1-Carbon-Gen-9:/tmp$ git clone https://github.com/nvbn/thefuck.git
```

Let's do a static import analysis on this project:


```python
>>> from do_static_import_analysis_for_pure_python_project import do_static_import_analysis_for_pure_python_project
>>> module_name_to_file_path_dict, module_name_to_defined_function_name_set_dict, module_name_to_defined_type_name_set_dict, module_name_to_imported_module_name_set_dict, module_name_to_imported_external_module_name_set_dict = do_static_import_analysis_for_pure_python_project('/tmp/thefuck')
```

Let's focus on the module `thefuck.ui`, presented below:

```python
# -*- encoding: utf-8 -*-

import sys
from .conf import settings
from .exceptions import NoRuleMatched
from .system import get_key
from .utils import get_alias
from . import logs, const


def read_actions(): ...


class CommandSelector(object): ...


def select_command(corrected_commands): ...
```

What are the names of the functions defined in this module?

```python
>>> module_name_to_defined_function_name_set_dict['thefuck.ui']
{'read_actions', 'select_command'}
```

What are the names of the types (classes) defined in this module?

```python
>>> module_name_to_defined_type_name_set_dict['thefuck.ui']
{'CommandSelector'}
```

What are the names of the modules imported in this module?

```python
>>> module_name_to_imported_module_name_set_dict['thefuck.ui']
{'thefuck.exceptions', 'thefuck', 'thefuck.conf', 'thefuck.system', 'thefuck.utils'}
>>> module_name_to_imported_external_module_name_set_dict['thefuck.ui']
{'sys'}
```

Note that all the *relative imports* in this file have been resolved:

```python
from .conf import settings
from .exceptions import NoRuleMatched
from .system import get_key
from .utils import get_alias
from . import logs, const
```
