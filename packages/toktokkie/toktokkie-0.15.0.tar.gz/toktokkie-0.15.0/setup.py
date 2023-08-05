"""
Copyright 2015-2017 Hermann Krumrey

This file is part of toktokkie.

toktokkie is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

toktokkie is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with toktokkie.  If not, see <http://www.gnu.org/licenses/>.
"""

# imports
import os
import json
from toktokkie import version
from setuptools import setup, find_packages


def readme():
    """
    Reads the readme file and converts it to RST if pypandoc is
    installed. If not, the raw markdown text is returned
    :return: the readme file as a string
    """
    # noinspection PyBroadException
    try:
        # noinspection PyPackageRequirements,PyUnresolvedReferences
        import pypandoc
        with open("README.md") as f:
            # Convert markdown file to rst
            markdown = f.read()
            rst = pypandoc.convert(markdown, "rst", format="md")
            return rst

    except ModuleNotFoundError:
        # If pandoc is not installed, just return the raw markdown text
        with open("README.md") as f:
            return f.read()


def find_scripts():
    """
    Returns a list of scripts in the bin directory
    :return: the list of scripts
    """
    scripts = []

    for file_name in os.listdir("bin"):

        path = os.path.join("bin", file_name)
        if file_name == "__init__.py":
            continue
        elif not os.path.isfile(path):
            continue
        else:
            scripts.append(os.path.join("bin", file_name))

    return scripts


def create_local_config_dir():
    """
    Creates a local configuration directory with default values if none exist
    yet
    :return: None
    """
    toktokkie_dir = os.path.join(os.path.expanduser("~"), ".toktokkie")
    if not os.path.isdir(toktokkie_dir):
        os.makedirs(toktokkie_dir)

    metadata_config_file = os.path.join(toktokkie_dir, "metadata_config.json")
    if not os.path.isfile(metadata_config_file):
        with open(metadata_config_file, 'w') as f:
            f.write(json.dumps({"media_directories": []}))


create_local_config_dir()
setup(
    name="toktokkie",
    version=version,
    description="A personal media manager program",
    long_description=readme(),
    classifiers=[
        "Environment :: Other Environment",
        "Natural Language :: English",
        "Intended Audience :: End Users/Desktop",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],
    url="https://gitlab.namibsun.net/namboy94/toktokkie",
    download_url="https://gitlab.namibsun.net/namboy94/toktokkie/"
                 "repository/archive.zip?ref=master",
    author="Hermann Krumrey",
    author_email="hermann@krumreyh.com",
    license="GNU GPL3",
    packages=find_packages(),
    install_requires=[
        'tvdb_api',
        'beautifulsoup4',
        'typing',
        'requests',
        'urwid',
        'xdcc_dl'
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
    scripts=find_scripts(),
    zip_safe=False
)
