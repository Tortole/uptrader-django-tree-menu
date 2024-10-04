"""
Project scripts for run through Poetry
"""

import sys
import subprocess


def manager():
    subprocess.run(["poetry", "run", "python", "manage.py", *sys.argv[1:]], check=False)


def full_migrate():
    subprocess.run(
        ["poetry", "run", "python", "manage.py", "makemigrations"], check=False
    )
    subprocess.run(["poetry", "run", "python", "manage.py", "migrate"], check=False)


def flake8():
    subprocess.run(["poetry", "run", "flake8", "."], check=False)


def black():
    subprocess.run(["poetry", "run", "black", "."], check=False)
    flake8()


def export_requirements():
    subprocess.run(
        [
            "poetry",
            "export",
            "-f",
            "requirements.txt",
            "-o",
            "requirements.txt",
            "--without-hashes",
        ],
        check=False,
    )
