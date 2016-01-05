#!/usr/bin/env python
"""
{{ app_name_verbose }} Colab plugin
===================================
"""
from setuptools import setup, find_packages

install_requires = ['colab']

tests_require = ['mock']


setup(
    name="{{ app_name_dash }}",
    version='0.1.0',
    author='<<Author Name>>',
    author_email='<<Author email>>',
    url='<< project url/repo url >>',
    description='{{ app_name_verbose }} Colab plugin',
    long_description=__doc__,
    license='<< project license >>',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    zip_safe=False,
    install_requires=install_requires,
    test_suite="tests.runtests.run",
    tests_require=tests_require,
    extras_require={'test': tests_require},
    include_package_data=True,
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
