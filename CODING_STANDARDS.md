Coding Standards
========

* Follow [PEP-8](http://legacy.python.org/dev/peps/pep-0008/) as closely as possible
* Be: explicit, self-documenting, readable, DRY, KISS, consistant

Naming
--------

* Module: Camelcase, lower first letter
* Global: Uppercase, _ separated
* Local: Lowercase, _ separated
* Local: Single letter only for indexes or intermediates
* Function: Lowercase, _ separated
* Class: Camelcase, uppercase first letter

Strings
--------

* Docstrings in """
* Multiline comments and strings in "
* Anything argument or variable like in '

Spaces
--------

* Readability is king, aligning is fine
* 4 spaces/tabwidth
* No tabs
* None required for short calculations: pi = 22/7
* Can be used for clarity: ymin = 5*xmin - 1
* Always a space after a ,
* Newlines separate logical segments or subfunctions

Commenting
--------

* Use when clarifying, documenting, or sectioning
* Code should be self-documenting at any time possible
* Use two spaces before inline comments
* Capital first letter of a sentence

Decimals
--------

* Be explicit when expecting a floating point, even with 'division': 1/5.
* Don't write unneccesary digits: '0.' versus '0.0'

