
from setuptools import setup, find_packages


REQUIREMENTS = [
    'Django>=1.7.10,<1.8',
    'pytz>=2011n',
    'django-hitcounter>=0.1.1',

    # Search
    'django-haystack>=2.2',
    'Whoosh>=2.7.0',

    # revproxy
    'django-revproxy[diazo]>=0.9.9',

    # Async Signals
    'celery[redis]>=3.1.2',

    # Acceptance tests
    'selenium>=2.53.1',
    'behave_django>=0.3.0',

    ### Move out of colab (as plugins):

    # Deps for super_archives
    'etiquetando==0.1',
    'django-taggit>=0.12.1',
    'html2text>=3.200.3',
    'chardet>=2.3.0',
    'requests>=2.7.0'
]

TEST_REQUIREMENTS = [
    'coverage>=3.7.1',
    'coveralls>=0.5',
    'flake8>=2.3.0',
    'mock==1.0.1',
]


EXCLUDE_FROM_PACKAGES = []


setup(
    name='colab',
    version='1.13.5',
    url='https://github.com/colab-community/colab',
    author='Sergio Oliveira',
    author_email='sergio@tracy.com.br',
    description='Collaboration platform for communities',
    license='LICENSE.txt',
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    include_package_data=True,
    entry_points={'console_scripts': [
        'colab-admin = colab.utils.runner:execute_from_command_line',
    ]},
    zip_safe=False,
    long_description=open('README.rst').read(),
    install_requires=REQUIREMENTS,
    tests_require=TEST_REQUIREMENTS,
    test_suite="tests.run.runtests",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
    ],
)
