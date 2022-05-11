import re
import os
import sys


class StaticCodeAnalyzerError(Exception):
    pass


class TooLongLineError(StaticCodeAnalyzerError):
    pass


class IndentationError(StaticCodeAnalyzerError):
    pass


class UnnecessarySemicolonError(StaticCodeAnalyzerError):
    pass


class NotEnoughSpacesError(StaticCodeAnalyzerError):
    pass


class TODOFoundError(StaticCodeAnalyzerError):
    pass


class TooManyBlankLinesError(StaticCodeAnalyzerError):
    pass


class TooManySpaceConstructionNameError(StaticCodeAnalyzerError):
    pass


class CamelCaseError(StaticCodeAnalyzerError):
    pass


class SnakeCaseError(StaticCodeAnalyzerError):
    pass


class StaticCodeAnalyzer:

    def __init__(self, path_file: str):
        self.path_file = path_file
        self.__check_funcs = [
            self.__check_long,
            self.__check_indentation,
            self.__check_semicolon,
            self.__check_spaces,
            self.__check_todo_existing,
            self.__check_blank_lines,
            self.__check_construction_def,
            self.__check_construction_class,
            self.__check_camel_case,
            self.__check_snake_case
        ]
        self.__count_blank_lines_in_row = 0

    def check_file(self):
        with open(self.path_file, 'r') as f:
            number_line = 1
            for line in f:
                self.__check_errors(number_line, line)
                number_line += 1

    def __check_errors(self, number_line, line):
        for func in self.__check_funcs:
            try:
                func(line)
            except StaticCodeAnalyzerError as err:
                self.__print_error(self.path_file, number_line, err.args[0], err.args[1])

    @staticmethod
    def __print_error(file, number_line, code, error):
        print("{}: Line {}: {} {}".format(file, number_line, code, error))

    @staticmethod
    def __check_long(line):
        long = 79
        if len(line) > long:
            raise TooLongLineError('S001', "Too long")

    @staticmethod
    def __check_indentation(line):
        if line != '\n' and (len(line) - len(line.lstrip())) % 4:
            raise IndentationError('S002', "Indentation is not a multiple of four")

    @staticmethod
    def __check_semicolon(line):
        parts_line = line.split('#')
        if parts_line[0].rstrip("\n").rstrip(" ").endswith(";"):
            raise UnnecessarySemicolonError('S003', "Unnecessary semicolon")

    @staticmethod
    def __check_spaces(line):
        if re.match(r"[^#]*[^ ]( ?#)", line):
            raise NotEnoughSpacesError('S004', "At least two spaces required before inline")

    @staticmethod
    def __check_todo_existing(line):
        if re.search(r'(?i)# *todo', line):
            raise TODOFoundError('S005', "TODO found")

    def __check_blank_lines(self, line):
        if line.rstrip('\n') == "":
            self.__count_blank_lines_in_row += 1
        if line.rstrip('\n') != "" and self.__count_blank_lines_in_row > 2:
            self.__count_blank_lines_in_row = 0
            raise TooManyBlankLinesError('S006', "More than two blank lines preceding a code line")
        if line.rstrip('\n') != "":
            self.__count_blank_lines_in_row = 0

    @staticmethod
    def __check_construction_def(line):
        error_object = re.match(r'\s*\b(def)\s{2,}\w+\(\w*\):$', line)
        if error_object:
            raise TooManySpaceConstructionNameError("S007", f"Too many spaces after '{error_object.group(1)}'")

    @staticmethod
    def __check_construction_class(line):
        error_object = re.match(r'\b(class)\s{2,}\w*(\(\w+\))?:$', line)
        if error_object:
            raise TooManySpaceConstructionNameError("S007", f"Too many spaces after '{error_object.group(1)}'")

    @staticmethod
    def __check_camel_case(line):
        error_object = re.match(r'\bclass\s+([^A-Z]([a-z_\d-]|\d)*)(\(\w+\))?:$', line)
        if error_object:
            raise CamelCaseError("S008", f"Class name '{error_object.group(1)}' should use CamelCase")

    @staticmethod
    def __check_snake_case(line):
        any_func = re.match(r'\bdef\s+(.+)\(.*\):$', line)
        if any_func:
            correct_func = re.match(r'\bdef\s+([a-z\d_]+)\(.*\):$', line)
            if correct_func is None:
                raise SnakeCaseError("S009", f"Function name '{any_func.group(1)}' should use snake_case")


if __name__ == "__main__":

    args = sys.argv
    input_path = args[1]


    def call_analyzer_error(path):
        error_checking = StaticCodeAnalyzer(path)
        error_checking.check_file()
        return None


    if os.path.isdir(input_path):

        for root, dirs, files in os.walk(input_path):
            for file_name in files:
                if file_name.endswith(".py") is False:
                    continue

                file_path = os.path.join(root, file_name)
                call_analyzer_error(file_path)

    else:
        call_analyzer_error(input_path)
