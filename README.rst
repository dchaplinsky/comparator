comparator
================

Simple tool to compare almost similar names which are coming **from the same source** (for example list of all company owners and officers of that company). Helps to cluster together persons with a slight difference in name spelling/typos. Better suited for Cyrillic names, but should work everywhere.

It's heuristic based and as any algorithm of such a nature it **make errors** sometime (see Accuracy section below for details). 

Installation
==================================
Install from PyPI.

.. code-block:: bash

    $ pip install names_comparator

Accuracy
==================================

You can test your installation on a ground truth data and check confusion matrix by running:

.. code-block:: bash

    $ python comparator/__init__.py comparator/data/ground_truth.csv
	+--------------------+----------+----------+
	|                    | Positive | Negative |
	+--------------------+----------+----------+
	| Predicted positive |   290    |    9     |
	| Predicted negative |    14    |   687    |
	+--------------------+----------+----------+
	Precision:  0.97
	Recall:  0.95
	F1 score:  0.96

You can also run it with debug flag to see all the errors algorithm made:

.. code-block:: bash

    $ python comparator/__init__.py comparator/data/ground_truth.csv yes

Usage
==================================

.. code-block:: python

    >>> from comparator import full_compare
    >>> full_compare("Barack Hussein Obama", "Obama, Barak")
    True
    >>> full_compare("Петро Мазепа", "Мазепа Петро")
    True
    >>> full_compare("Марченко Петро Миколайович", "Панченко Петро Миколайович")
    False
    >>> full_compare("Овдієнко Сергій Костантинович", "Овдієнко Сергій Костянтинович")
    True
    >>> full_compare("Іванов Михайло Юрійович", "Іванов Юрій Михайлович")
    False
