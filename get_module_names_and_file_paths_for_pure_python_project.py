import os
import os.path
from typing import Generator


def get_module_names_and_file_paths_for_pure_python_project(project_path: str) -> Generator[tuple[str, str], None, None]:
    for root, directories, files in os.walk(project_path):
        relpath = os.path.relpath(root, project_path)

        python_file_names = []
        python_file_paths = []

        for file in files:
            file_name, file_ext = os.path.splitext(file)
            if file_ext == '.py':
                python_file_names.append(file_name)
                python_file_paths.append(os.path.join(root, file))

        # only handle python files in `os.path.curdir`
        if relpath == os.path.curdir:
            for python_file_name, python_file_path in zip(python_file_names, python_file_paths):
                yield python_file_name, python_file_path
        # handle the directory itself (if there is a python file named `__init__` within the directory) and python files (excluding the python file named `__init__`) in other directories
        else:
            relpath_components = relpath.split(os.path.sep)

            try:
                index_of___init__ = python_file_names.index('__init__')
                module_name = '.'.join(relpath_components)
                yield module_name, python_file_paths[index_of___init__]
            except ValueError:
                pass

            for python_file_name, python_file_path in zip(python_file_names, python_file_paths):
                if python_file_name != '__init__':
                    module_name = '.'.join([*relpath_components, python_file_name])
                    yield module_name, python_file_path
