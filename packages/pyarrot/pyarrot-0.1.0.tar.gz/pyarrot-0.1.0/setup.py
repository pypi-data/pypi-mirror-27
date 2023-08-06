# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme_txt = f.read()

def _requires_from_file(filename):
    return open(filename).read().splitlines()

setup(
    name='pyarrot',
    version='0.1.0',
    description='Write with interactive mode for trial and error, Get the batch mode for cron or other automation.',
    long_description=readme_txt,
    author='yuuki miyoshi',
    author_email='yuuki.miyo@gmail.com',
    url='https://github.com/yuukimiyo/PyArrot',
    license="MIT",
    keywords="interactive batch",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
