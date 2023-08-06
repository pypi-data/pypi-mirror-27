# -*- coding: utf-8 -*-
"""
    setup
    ~~~~
    KI-Hosting est un module développé pour automatiser les services d'hébergment
    du club informatique des Ponts et Chaussées
    :copyright: (c) 2017 by KI Clubinfo
    :license: MIT, see LICENSE for more details.
"""

from setuptools import setup
from os.path import join, dirname

def readme():
    with open('README.md') as f:
        return f.read()

with open(join(dirname(__file__), 'ki_hosting/version.py'), 'r') as f:
    exec(f.read())

with open (join(dirname(__file__), 'requirements.txt'), 'r') as f:
    install_requires = f.read().split("\n")

setup(
    name='KI-Hosting',
    version=__version__,
    description='Manage hosting at KI Ecole Des Ponts',
    long_description=readme(),
    keywords='generate ki clubinfo fiche club asso',
    url='http://github.com/KIClubinfo/ki-hosting',
    author='Philippe Ferreira De Sousa',
    author_email='philippe@fdesousa.fr',
    license='MIT',
    packages=['ki_hosting'],
    install_requires=install_requires,
    scripts=[
        'bin/fi:generate',
        'bin/fi:remove',
        'bin/req:handle'
    ],
    zip_safe=False
)
