#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst', encoding='utf-8') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst', encoding='utf-8') as history_file:
    history = history_file.read()

with open('requirements.txt', encoding='utf-8') as requirements_file:
    requirements = requirements_file.read().split('\n')

setup_requirements = [
    # TODO(ali--): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='snap_studio',
    version='0.0.2',
    description="SparklineData SNAP Studio",
    long_description=readme + '\n\n' + history,
    scripts=['snap_studio/bin/snap-studio'],
    author="Ali Rathore",
    author_email='ali1rathore@gmail.com',
    url='https://gitlab.com/SparklineData/Public/snap-studio',
    packages=find_packages(include=['snap_studio']),
    include_package_data=True,
    install_requires=requirements,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='snap_studio',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
