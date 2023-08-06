# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='PyLogStash',
    version='0.0.2',
    url='http://git.fortbrasil.com.br/Dev/PyLogStash.git',
    license='MIT License',
    author='pedro.nascimento',
    author_email='pedro.nascimento@fortbrasil.com.br',
    keywords='logstash fortbrasil',
    description=u'Pacote de integração Http com o logstash',
    packages=['PyLogStash'],
    install_requires=['requests'],
)