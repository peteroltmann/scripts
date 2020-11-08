#!/usr/bin/env python3

#
# Create a new class from a tempalte.
#

from __future__ import print_function

from Class import Class

import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Create a new class from template.')  # noqa

    parser.add_argument("class_name",      help="the class name")  # noqa
    parser.add_argument("--author",        help="the author name, use git config if omitted")  # noqa
    parser.add_argument("--package",       help="the package/namspace name, remove namepsace if omitted")  # noqa
    parser.add_argument("--include_guard", help="the name for the include guard, use package name if ommited")  # noqa
    parser.add_argument("--date",          help="the date, use today if omitted")  # noqa
    parser.add_argument("--config",        help="the config with replacement strings")  # noqa

    return parser.parse_args()


def main():
    args = parse_args()

    class_data = Class(args)
    class_data.read_config()
    class_data.read_template()
    class_data.replace_all()
    class_data.create_class_files()


if __name__ == "__main__":
    main()
