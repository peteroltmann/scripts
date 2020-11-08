#!/usr/bin/env python3

#
# Create a new class snippet for VSCode from a template.
#

from __future__ import print_function

from Class import Class

import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser(description='Create a new class snippet from template.')  # noqa

    # default arguments: vscode snippet variables
    parser.add_argument("--class_name",    help="the class name",                 default="${1:ClassName}")  # noqa
    parser.add_argument("--author",        help="the author name",                default="${2:author}")  # noqa
    parser.add_argument("--date",          help="the date",                       default="$CURRENT_DATE.$CURRENT_MONTH.$CURRENT_YEAR")  # noqa
    parser.add_argument("--package",       help="the package/namspace name",      default="${3:package}")  # noqa
    parser.add_argument("--include_guard", help="the name for the include guard", default="${3/(.*)/${1:/upcase}/}_${1/(.*)/${1:/upcase}/}")  # noqa
    parser.add_argument("--snippet_name",  help="the name of the snippet",        default="class_template")  # noqa
    parser.add_argument("--snippet_dir",   help="the directory of the snippet",   default=".vscode")  # noqa

    return parser.parse_args()


def add_snippet_data(class_data, name):
    # extra line at end of snippet (\n in last line is not sufficient)
    class_data.data.header.append("\n")  # new line at EOF

    for i, line in enumerate(class_data.data.header):
        line = line.replace("\\", "\\\\")  # replace \ with \\ (doxygen)
        line = '            "' + line      # indentation in snippet body
        line = line.replace('\n', '",\n')  # prepend \n with string and comma
        class_data.data.header[i] = line   # update data

    class_data.data.header.insert(0, '{\n')
    class_data.data.header.insert(1, '    "Create new class file": {\n')
    class_data.data.header.insert(2, '        "scope": "cpp",\n')
    class_data.data.header.insert(3, '        "prefix": "' + name + '",\n')
    class_data.data.header.insert(4, '        "body": [\n')
    class_data.data.header.append(   '        ],\n')  # noqa
    class_data.data.header.append(   '        "description": "Create a new class file from template"\n')  # noqa
    class_data.data.header.append(   '    }\n')  # noqa
    class_data.data.header.append(   '}\n')  # noqa


def create_snippet_file(class_data, directory, filename):
    snippet = os.path.join(directory, filename + ".code-snippets")
    os.makedirs(directory, exist_ok=True)
    with open(snippet, "w") as file:
        file.writelines(class_data.data.header)


def main():
    args = parse_args()

    class_data = Class(args)

    class_data.read_template()
    class_data.replace_all()

    add_snippet_data(class_data, args.snippet_name)
    create_snippet_file(class_data, args.snippet_dir, args.snippet_name)


if __name__ == "__main__":
    main()
