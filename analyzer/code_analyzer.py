import os
import re
import sys


class CodeAnalyzer:
    def __init__(self):
        self.args = sys.argv
        self.path = ''.join(self.args[1:])
        self.directory = None
        self.list_files = None
        self.file_to_open = None
        self.current_line_string = None
        self.current_line_no = 1
        self.blanklines_count = 0
        self.split_code_comment = None

    def dir_or_file(self):
        dot = self.path.find('.')
        if (dot > 0) and (self.path[dot+1:] == 'py'):
            self.line_reader()
        if dot == -1:
            self.directory = self.path
            self.list_files = sorted(os.listdir(self.path))
            self.file_reader()

    def file_reader(self):
        for file in self.list_files:
            dot = file.find('.')
            if (dot > 0) and (file[dot+1:] == 'py'):
                self.current_line_no = 1
                self.file_to_open = file
                self.path = os.path.join(self.directory, file)
                self.line_reader()

    def line_reader(self):
        with open(self.path, "r") as file:
            for line in file.readlines():
                self.current_line_string = line
                self.code_analyzer()
                self.current_line_no += 1

    def code_analyzer(self):
        self.length_checker()  # S001
        self.indent_checker()  # S002
        self.semicolon_checker()  # S003
        self.space_checker()  # S004
        self.todo_checker()  # S005
        self.blanklines_checker()  # S006
        self.spaces_after_construction()  # S007

    def length_checker(self):
        length_of_line = len(self.current_line_string)
        if length_of_line > 79:
            self.error_message("S001")

    def indent_checker(self):
        string_space_count = 0
        for x in self.current_line_string:
            if x == " ":
                string_space_count += 1
            elif x != " ":
                break
        if string_space_count % 4 != 0:
            self.error_message("S002")

    def code_comment(self, access):
        self.split_code_comment = self.current_line_string.split("#", 1)
        if access == "code":
            return self.split_code_comment[0]
        elif access == "comment":
            return self.split_code_comment[1]

    def semicolon_checker(self):
        inside_string = False
        for x in self.code_comment("code"):
            if x == "'" or x == '"':
                if not inside_string:
                    inside_string = True
                    continue
                if inside_string:
                    inside_string = False
                    continue
            if x == ";" and inside_string is False:
                self.error_message("S003")
                break

    def space_checker(self):
        assert len(self.split_code_comment) == 1 or len(self.split_code_comment) == 2
        if len(self.split_code_comment) == 2 and self.split_code_comment[0] != "":
            reverse_space_count = 0
            for x in reversed(self.code_comment("code")):
                if x == " ":
                    reverse_space_count += 1
                else:
                    break
            if reverse_space_count < 2:
                self.error_message("S004")
        else:
            pass

    def todo_checker(self):
        assert len(self.split_code_comment) == 1 or len(self.split_code_comment) == 2
        if len(self.split_code_comment) == 2 and \
                self.split_code_comment[1].upper().find("TODO") != -1:
            self.error_message("S005")
        else:
            pass

    def blanklines_checker(self):
        assert len(self.split_code_comment) == 1 or len(self.split_code_comment) == 2
        if self.blanklines_count == 3:
            self.blanklines_count = 0
            self.error_message("S006")
        elif len(self.split_code_comment) == 1 and self.split_code_comment[0] == "\n":
            self.blanklines_counter("increase")
        else:
            self.blanklines_counter("reset")

    def blanklines_counter(self, action):
        if action == "increase":
            self.blanklines_count += 1
        else:
            self.blanklines_count = 0

    def spaces_after_construction(self):
        temp_def = r' *def  +'
        temp_class = r' *class  +'
        if re.match(temp_def, self.current_line_string) is not None:
            self.error_message("S007")
        elif re.match(temp_class, self.current_line_string) is not None:
            self.error_message("S007")

    def error_message(self, code):
        error_dict = {"S001": "Line Too Long",
                      "S002": "Indentation is not a multiple of four",
                      "S003": "Unnecessary semicolon",
                      "S004": "Less than two spaces before inline comments",
                      "S005": "TODO found",
                      "S006": "More than two blank lines used before this line",
                      "S007": "Too many spaces after construction_name (def or class)"
                      }
        print("{}: Line {}: {} {}".format(self.path, self.current_line_no, code, error_dict.get(code)))


def main():
    file_to_check = CodeAnalyzer()
    file_to_check.dir_or_file()


if __name__ == "__main__":
    main()
