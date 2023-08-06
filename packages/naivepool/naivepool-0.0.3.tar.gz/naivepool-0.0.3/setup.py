#!/usr/bin/env python
#-*- coding:utf-8 -*-


from setuptools import setup, find_packages

setup(
    name = "naivepool",
    version = "0.0.3",
    keywords = ("threadpool", "naivepool", "thread", "myvyang"),
    description = "naive thread pool of python",
    long_description = "naive thread pool of python, support fetch output",
    license = "MIT Licence",

    url = "https://github.com/myvyang/threadpool",
    author = "myvyang",
    author_email = "myvyang@gmail.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = []
)
