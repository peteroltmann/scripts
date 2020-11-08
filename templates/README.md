# Templates

Scripts to create new files/classes from a template.

The template is expected in the script's directory named `Template.hpp` and `Template.cpp`.

## New Class

Use `new_class.py` to create new class files (.hpp and .cpp) from a given template.

Run help for parameter info
```
./new_class.py --help
```

Examples:

```sh
./new_class.py MyClass
./new_class.py MyClass --package mypackage
./new_class.py MyClass --package mypackage --author "John Doe"
./new_class.py MyClass --config config.json
```

Create a JSON cofnig file to specify the strings to be replaced in the template.
  
Example:
```json
{
    "class_name": "ClassName",
    "author": "First Last (shrt)",
    "date": "dd.mm.yyyy",
    "package": "packagename",
    "include_guard": "PACKAGENAME_CLASSNAME"
}
```

If you ommit the config the values from the example above are used by default.

## New Snippet

Use the `new_class_snippet.py` script to generate a VSCode snippet file from a template. The script uses the same interface as the new class script above but adds VSCode snippet compliant arguments as default values (e.g. `${1:ClassName}`).

Run:
```
./new_class_snippet.py

```
Run help for optional parameter info:
```
./new_class_snippet.py --help
```

## Usage Recommendation

Create a bash alias to the `new_class.py` so you can create new class files from everywhere without specifying the whole path to the script. 

Example:

```sh
alias new_class='<path_to_script_repository>/templates/new_class.py'
```
