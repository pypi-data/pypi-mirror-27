#! /usr/bin/env python

from setuptools import setup, find_packages
import versioneer
from codecs import open

setup (
    name = "cfgset",
    version = versioneer.get_version (),
    description = "Query interface to prioritised collections of CfgStacks",
    long_description = open ("README.rst", 'r', encoding = 'utf-8').read (),
    cmdclass = versioneer.get_cmdclass (),
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: "
        + "GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Topic :: Utilities",
    ],
    keywords = "config sets, configfile, file stacks, reference trees",
    author = "J C Lawrence",
    author_email = "claw@kanga.nu",
    url = "https://github.com/clearclaw/cfgset",
    license = "LGPL v3.0",
    test_suite = "tests.cfgset_test",
    packages = find_packages (exclude = ["tests",]),
    package_data = {},
    data_files = [],
    zip_safe = False,
    install_requires = [line.strip ()
        for line in open ("requirements.txt", 'r',
                          encoding = 'utf-8').readlines ()],
    entry_points = {
        "console_scripts": [
        ],
    },
)
