"""Create generate files."""

import glob
from doit.tools import create_folder

DOIT_CONFIG = {"default_tasks": ["all"]}


def task_html():
    """Make HTML documentation."""
    return {
        "actions": ["sphinx-build -M html docs build"],
    }


def task_test():
    """Run tests."""
    return {
        "actions": ["python -m unittest"],
    }


def task_pot():
    """Re-create .pot ."""
    return {
        "actions": ["pybabel extract -o FinanceAnalyzer.pot FinanceAnalyzer"],
        "file_dep": glob.glob("FinanceAnalyzer/*.py"),
        "targets": ["FinanceAnalyzer.pot"],
    }


def task_po():
    """Update translations."""
    return {
        "actions": ["pybabel update -D FinanceAnalyzer -d po -i FinanceAnalyzer.pot"],
        "file_dep": ["FinanceAnalyzer.pot"],
        "targets": ["po/ru/LC_MESSAGES/FinanceAnalyzer.po"],
    }


def task_mo():
    """Compile translations."""
    return {
        "actions": [(create_folder, ["FinanceAnalyzer/ru/LC_MESSAGES"]),
                    "pybabel compile -D FinanceAnalyzer -l ru "
                    "-i po/ru/LC_MESSAGES/FinanceAnalyzer.po -d FinanceAnalyzer"],
        "file_dep": ["po/ru/LC_MESSAGES/FinanceAnalyzer.po"],
        "targets": ["FinanceAnalyzer/ru/LC_MESSAGES/FinanceAnalyzer.mo"],
    }


def task_wheel():
    """Create binary wheel distribution."""
    return {
        'actions': ['python -m build -w'],
        'task_dep': ['mo'],
    }
