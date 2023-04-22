from get_function_names_and_class_names_in_python_file import get_function_names_and_class_names_in_python_file
from get_imports_and_import_froms_in_python_file import get_imports_and_import_froms_in_python_file
from get_module_name_to_file_path_dict_for_pure_python_project import \
    get_module_name_to_file_path_dict_for_pure_python_project


# Returns four values
# module_name_to_file_path_dict: dict[str, str]
# module_name_to_defined_function_name_set_dict: dict[str, set[str]]
# module_name_to_defined_type_name_set_dict: dict[str, set[str]]
# module_name_to_imported_module_name_set_dict: dict[str, set[str]]
# module_name_to_imported_external_module_name_set_dict: dict[str, set[str]]
def do_static_import_analysis_for_pure_python_project(project_path: str) -> tuple[
    dict[str, str], dict[str, set[str]], dict[str, set[str]], dict[str, set[str]], dict[str, set[str]]
]:
    module_name_to_file_path_dict: dict[str, str] = get_module_name_to_file_path_dict_for_pure_python_project(
        project_path)

    module_name_to_defined_function_name_set_dict: dict[str, set[str]] = dict()
    module_name_to_defined_type_name_set_dict: dict[str, set[str]] = dict()
    module_name_to_imported_module_name_set_dict: dict[str, set[str]] = dict()
    module_name_to_imported_external_module_name_set_dict: dict[str, set[str]] = dict()

    for module_name, file_path in module_name_to_file_path_dict.items():
        # update module_name_to_defined_function_name_set_dict, module_name_to_defined_type_name_set_dict
        function_names, class_names = get_function_names_and_class_names_in_python_file(file_path)

        module_name_to_defined_function_name_set_dict[module_name] = function_names
        module_name_to_defined_type_name_set_dict[module_name] = class_names

        # update module_name_to_imported_module_name_set_dict, module_name_to_imported_external_module_name_set_dict
        module_name_to_imported_module_name_set_dict[module_name] = imported_module_name_set = set()
        module_name_to_imported_external_module_name_set_dict[module_name] = imported_external_module_name_set = set()

        is_package = file_path.endswith('__init__.py')
        imports, import_froms = get_imports_and_import_froms_in_python_file(file_path, module_name, is_package)

        for imported_module_name, imported_module_name_alias in imports:
            if imported_module_name not in module_name_to_file_path_dict:
                imported_external_module_name_set.add(imported_module_name)
            else:
                imported_module_name_set.add(imported_module_name)
        for imported_module_name, imported_name, imported_name_alias in import_froms:
            if imported_module_name not in module_name_to_file_path_dict:
                imported_external_module_name_set.add(imported_module_name)
            else:
                imported_module_name_set.add(imported_module_name)

    return module_name_to_file_path_dict, \
        module_name_to_defined_function_name_set_dict, \
        module_name_to_defined_type_name_set_dict, \
        module_name_to_imported_module_name_set_dict, \
        module_name_to_imported_external_module_name_set_dict
