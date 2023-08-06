from .api import *  # noqa

__version__ = "0.2.0"

__doc__ = """
tree_decode - Library that helps to remove the black-box
surrounding decision trees from scikit-learn, making it
easier to understand how they work and more importantly,
to diagnose their issues when they produce unexpected results.

The decision tree classes that scikit-learn currently supports are:

* DecisionTreeClassifier
* DecisionTreeRegressor

Support for other such scikit-learn classes is being actively worked on.
"""


def test():
    """
    Run unit tests on the current tree_decode installation.
    """

    try:
        import pytest  # noqa
    except ImportError:
        raise ImportError("pytest not found. Please install "
                          "with `pip install pytest`")

    from subprocess import call
    from os.path import dirname

    directory = dirname(__file__)
    call(["pytest", directory])
