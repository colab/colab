
from setuptools import setup, find_packages
 

REQUIREMENTS = [
    'Django>=1.7',
    'South==1.0.0',
    'psycopg2==2.5.1',
    'django-piston==0.2.3',
    'pytz==2011n',
    'chardet==1.0.1',
    'python-dateutil==1.5',
    'django-cliauth==0.9.1',
    'django-mobile==0.3.0',
    'django-haystack==2.1',
    'pysolr==2.1',
    'poster==0.8.1',
    'etiquetando==0.1',
    'html2text==3.200.3',
    'django-taggit==0.12.1',
    'python-memcached==1.53',
    'django-hitcounter==0.1.1',
    'Pillow==2.5.1',
    'django-i18n-model==0.0.7',
    'django-tastypie==0.11.0',
    'gunicorn==19.1.0',
    'eventlet==0.15.2',
    'PyYAML==3.11',

    # Deps for sentry client (raven)
    'raven==3.5.2',
    'tornado==3.1.1',

    # Deps for Single SignOn (SSO) - Replaced with django-browserid==0.9
    'django-browserid==0.11',
    'django-revproxy==0.3.1',

    # Converse.js (XMPP client)
    'django-conversejs==0.3.4',

    # Feedzilla (planet) and deps
    'feedzilla==0.24',
    'django-common==0.1.51',
    'feedparser==5.1.3',
    'lxml==3.2.4',
    'grab==0.4.13',
    'transliterate==1.5',

    # Diazo
    'diazo==1.0.5',

    # Dpaste
    'dpaste==2.8',

    # Mailman 2 REST API
    'mailman-api==0.2.9',
]

TEST_REQUIREMENTS = [
    'Whoosh==2.5.7',
    'coverage==3.7.1',
    'coveralls==0.5',
    'flake8==2.3.0',
]


EXCLUDE_FROM_PACKAGES = []


setup(
    name='colab',
    version='2.0a2',
    url='https://github.com/colab-community/colab',
    author='Sergio Oliveira',
    author_email='sergio@tracy.com.br',
    description='Collaboration platform for communities',
    license='LICENSE.txt',
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    include_package_data=True,
    entry_points={'console_scripts': [
        'colab-admin = colab.management:execute_from_command_line',
        'colab-init-config = colab.management:initconfig',
    ]},
    zip_safe=False,
    long_description=open('README.rst').read(),
    install_requires=REQUIREMENTS,
    tests_require=TEST_REQUIREMENTS,
    test_suite="tests.run.run_with_coverage",
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
