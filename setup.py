"""
Pypi setup file
"""

import os

from setuptools import setup, find_packages

import git_dashboard

PATH_ROOT = os.path.dirname(__file__)

def load_requirements():
    """Load requirements.txt with comment support"""
    lines = []
    comment_char = '#'
    with open(os.path.join(PATH_ROOT, 'requirements.txt'), 'r', encoding='utf-8') as file:
        lines += [ln.strip() for ln in file.readlines()]
    reqs = []
    for ln in lines:
        # filter all comments
        if comment_char in ln:
            ln = ln[:ln.index(comment_char)]
        if ln:  # if requirement is not empty
            reqs.append(ln)
    return reqs

def load_readme():
    """Load README.md as string"""
    with open('README.md', encoding='utf-8') as inp:
        return inp.read()

setup(
    name='git_dashboard',
    version=git_dashboard.__version__,
    description="Git dashboard",
    author="Jung Ko",
    author_email="kojung@gmail.com",
    license="GPL",
    platforms=['any'],
    packages=find_packages(exclude=['tests']),
    python_requires='>=3.6',
    install_requires=load_requirements(),
    scripts=[
        'bin/git-dashboard',
    ],
    long_description=load_readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/kojung/git-dashboard',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)"
        "Operating System :: OS Independent",
    ],
)
