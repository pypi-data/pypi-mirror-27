import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "hangman_sk",
    version = "0.1.0",
    author = "Sylwiusz Kosacz",
    author_email = "sylwiusz.kosacz@gmail.com",
    description = ("Init python project"),
    license = "BSD",
    keywords = "structure template",
    url = "",
    packages=['hangman_sk', 'tests'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
