#!/usr/bin/env python3
#-*-coding:utf-8-*-
# __all__=""
# __datetime__=""
# __purpose__="打包"

from setuptools import find_packages, setup

setup(
    name="pscc",
    version="0.1.0",
    description="Crawler Everything For You By Anyone.",
    author="PSC",
    author_email="pythonscientists@outlook.com",
    url='https://github.com/PythonScientists/Pscc',
    install_requires=[
        'aiohttp',
        'pyquery',
        'aiofiles',
        'colorama',
        'click',
        'pybloom-live',
        'aiofile',
        'aiomysql',
        'aiodns'
    ],
    license='GNU GPL 3',
    packages=find_packages(),
    py_modules=['pscc'],
    include_package_data=True,
    zip_safe=False
)