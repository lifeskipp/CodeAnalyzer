class   CodeAnalyzer:
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

    def     file_reader(self):
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

class  fkfkkf:

