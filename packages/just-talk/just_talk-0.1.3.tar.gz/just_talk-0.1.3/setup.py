'''
Created on 22Jun.,2017

@author: Matt
'''
import os
from setuptools import setup

setup(
    name="just_talk",
    version="0.1.3",
    author="Matthew Rademaker",
    author_email="matthew@acctv.com.au",
    description="Python package to use the TOA comms protocol",
    license="LICENSE",
    keywords="tools on air toa just play video tv",
    url="https://github.com/magarnicle/just_talk",
    download_url="https://github.com/magarnicle/just_talk/archive/00.01.01.tar.gz",
    packages=['just_talk'],
    package_data={'just_talk': ['xml/*']},
    classifiers=["Development Status :: 4 - Beta",
        "Environment :: MacOS X",
        "Intended Audience :: Telecommunications Industry",
        "License :: Public Domain",
        "Natural Language :: English",
        "Programming Language :: Python :: 2.7",
        "Topic :: Multimedia :: Video"]
)
