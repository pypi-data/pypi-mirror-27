#!/usr/bin/env python

from setuptools import setup, find_packages

__version__ = '0.1.1'
__program__ = 'karamel'

setup(
    name=__program__,
    version=__version__,
    description='Karamel is a library let you build powerful Package Manager based on Git and other Version Control System.',
    author='Noel Martignoni',
    author_email='noel@martignoni.fr',
    url='https://gitlab.com/{0}/{0}'.format(__program__),
    scripts=['scripts/{}'.format(__program__)],
    install_requires=['future', 'pyyaml'],
    packages=find_packages(exclude=['tests*']),
)
