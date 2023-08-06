#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages


def main():
    description = 'gdwrap is wrapper libs for Google Drive Rest API.'

    setup(
        name='gdwrap',
        version='0.0.1',
        author='nabeen',
        author_email='watanabe_kenichiro@hasigo.co.jp',
        url='https://github.com/nabeen/gdwrap',
        description=description,
        long_description=description,
        zip_safe=False,
        include_package_data=True,
        packages=find_packages(),
        install_requires=[],
        tests_require=[],
        setup_requires=[],
    )


if __name__ == '__main__':
    main()
