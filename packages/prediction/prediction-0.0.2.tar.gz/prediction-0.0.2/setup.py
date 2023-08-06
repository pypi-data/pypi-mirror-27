
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os


with open('README.rst') as f:
    README = f.read()


def get_packages(packages):
    """
    Return root package and all sub-packages.
    """
    packages_list = []
    for package in packages:
        packages_list += [dirpath
                for dirpath, dirnames, filenames in os.walk(package)
                if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_packages_data(packages):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    packages_data = {}
    for package in packages:
        walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
                for dirpath, dirnames, filenames in os.walk(package)
                if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

        filepaths = []
        for base, filenames in walk:
            filepaths.extend([os.path.join(base, filename)
                              for filename in filenames])
        packages_data.update({package: filepaths})

    return packages_data

def get_data_files(directories):
    """
    TODO.
    """
    data_files = []
    for directory in directories:
        data_files.append((directory, [os.path.join(r,file) for r,d,f in os.walk(directory) for file in f]))

    return data_files


def read_requirements(filename):
    with open(filename, 'r') as file:
        return [line for line in file.readlines() if not line.startswith('-')]

setup(
    name='prediction',
    version='0.0.2',
    url='http://github.com/omritoptix/django-skeleton',
    license='MIT',
    long_description=README,
    description='Django skeleton project',
    author='Omri Dagan',
    author_email='omritoptix@gmail.com',
    packages=find_packages(),
    package_data=get_packages_data(['scoring','prediction']),
    # data_files=get_data_files(['templates']),
    # data_files=[('templates', ['templates/emails/test.html'])],
    zip_safe=False,
    include_package_data=True,
    install_requires=read_requirements('requirements.txt'),
    # data_files=[('bitmaps', ['bm/b1.gif', 'bm/b2.gif']),
    #             ('config', ['cfg/data.cfg']),
    #             ('/etc/init.d', ['init-script'])],
)