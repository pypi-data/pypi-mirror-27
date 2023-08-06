# -*- coding: utf-8 -*-

from setuptools import setup


setup(
    name="float2words",
    version='0.6.0',
    author="Focusate",
    author_email="dev@focusate.eu",
    url='https://github.com/focusate/extra-tools',
    license='MIT',
    long_description=open('README.rst').read(),
    py_modules=['float2words', ],
    install_requires=[
        'num2words',
    ],
)
