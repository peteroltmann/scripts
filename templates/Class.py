from collections import namedtuple
import datetime
import json
import os
import subprocess


class Class():
    """Read, hold and modify a C++ class data from a template.
    
    Member variables:
    args        -- the arguments given from argparse
                   class_name    -- the class name
                   author        -- the author name
                   date          -- the date
                   package       -- the package/namspace name
                   include_guard -- the name for the include guard
    replace_str -- dict of replace strings, keys analog to args
    data        -- the data for the class, line by line (header, source)
    """

    Data = namedtuple('Data', 'header source')

    def __init__(self, args) -> None:
        """Init the class data (see class description).

        Keyword arguments:
        args -- given from argparse (see class desription).
        """
        self.args = args
        self.replace_str = {
            "class_name": "ClassName",
            "author": "First Last (shrt)",
            "date": "dd.mm.yyyy",
            "package": "packagename",
            "include_guard": "PACKAGENAME_CLASSNAME",
        }
        self.data = Class.Data([], [])

    def read_config(self):
        """Read replace config from a given json file (use args.config).

        Example:
        {
            "class_name": "ClassName",
            "author": "First Last (shrt)",
            "date": "dd.mm.yyyy",
            "package": "packagename",
            "include_guard": "PACKAGENAME_CLASSNAME"
        }
        """
        if self.args.config is None:
            return

        dir_name = os.path.dirname(os.path.abspath(__file__))
        config = os.path.join(dir_name, self.args.config)

        self.replace_str = json.load(open(config))

    def read_template(self, directory=None, filename="Template"):
        """Read the C++ data from a template.
        
        Keyword arguments:
        directory -- the directory in which the template is located
                     (default None)
        filename  -- the filename of the template without extension
                     (.hpp/.cpp is added)
                     (default "Template")
        """
        if directory is None:  # use script dir
            directory = os.path.dirname(os.path.abspath(__file__))

        template_header = os.path.join(directory, filename + ".hpp")
        template_source = os.path.join(directory, filename + ".cpp")

        # read files as lines to allow string modification without copying
        with open(template_header, 'r') as file:
            header = file.readlines()

        with open(template_source, 'r') as file:
            source = file.readlines()

        self.data = Class.Data(header, source)

    def remove(self, str):
        """Remove a line matching the given string.
        
        Keyword arguments:
        str -- the string to be removed.
        """
        for t in range(len(self.data)):  # type: (header, source)
            self.data[t].remove(str)

    def replace(self, old, new):
        """Replace a all given strings with a new one.
        
        Keyword arguments:
        old -- the string to be replaced.
        new -- the new string.
        """
        for t, data in enumerate(self.data):  # type: (header, source)
            for i, line in enumerate(data):  # each line in type data
                self.data[t][i] = line.replace(old, new)

    def replace_class_name(self):
        """Replace the class name"""
        self.replace(self.replace_str['class_name'], self.args.class_name)

    def replace_author(self):
        """Replace the author.
        
        Use author from from git config, if args.author is not set.
        """
        if self.args.author is None:
            # get author from from git config
            self.args.author = subprocess.Popen("git config user.name", shell=True, stdout=subprocess.PIPE).communicate()[
                0].strip().decode("utf-8")

        self.replace(self.replace_str['author'], self.args.author)

    def replace_date(self):
        """Replace the date.
        
        Use the current date, if args.date is not set.
        """
        if self.args.date is None:  # use current date
            date = datetime.date.today()
            date = date.strftime("%d.%m.%Y")
        else:
            date = self.args.date

        self.replace(self.replace_str['date'], date)

    def replace_package(self):
        """Replace the package name if args.package is set."""
        if self.args.package is None:  # do nothing
            return

        self.replace(self.replace_str['package'], self.args.package)

    def replace_include_guard(self):
        """Replace include guard name.
        
        Use args.include_guard, if set.
        Otherwise use args.package and args.class_name.
        """
        # replace with configured include gurad sname
        if self.args.include_guard:
            self.replace(
                self.replace_str['include_guard'], self.args.include_guard)
            return
        
        # remove package name and namepsace if no package is set
        new_str = ""
        if self.args.package is None:
            self.remove("namespace " + self.replace_str['package'] + " {\n")
            self.remove("} // namespace " + self.replace_str['package'] + "\n")
        else:
            new_str = self.args.package.upper() + "_"

        new_str = new_str + self.args.class_name.upper()

        self.replace(self.replace_str['include_guard'], new_str)

    def replace_all(self):
        """Replace all configurable elements."""
        self.replace_class_name()
        self.replace_author()
        self.replace_date()
        self.replace_package()
        self.replace_include_guard()

    def create_class_files(self):
        """Create C++ class files form the class data."""
        # use relative path (current directory)
        header = self.args.class_name + ".hpp"
        source = self.args.class_name + ".cpp"

        with open(header, "w") as file:
            file.writelines(self.data.header)

        with open(source, "w") as file:
            file.writelines(self.data.source)
