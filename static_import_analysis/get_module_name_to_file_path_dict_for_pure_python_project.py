from .get_module_names_and_file_paths_for_pure_python_project import get_module_names_and_file_paths_for_pure_python_project


def get_module_name_to_file_path_dict_for_pure_python_project(project_path: str) -> dict[str, str]:
    return dict(get_module_names_and_file_paths_for_pure_python_project(project_path))
