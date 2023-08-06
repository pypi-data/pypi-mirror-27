#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='Marchines',
    version='1.0.8',
    description=(
        'Marchines'
    ),
    # long_description=open('README.rst').read(),
    author='madeitcwang',
    author_email='1321711107@qq.com',
    maintainer='madeitcwang',
    maintainer_email='1321711107@qq.com',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    url='https://gitee.com/madeitcwang/Machine_Learing_in_Action',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
      'keras >= 2.0.5',
      'tensorflow >= 1.1.0',
      'nltk >= 3.2.3',
      'numpy >= 1.12.1',
      'six >= 1.10.0',
      'tqdm >= 4.19.4']
)
