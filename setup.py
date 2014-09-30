
from setuptools import setup, find_packages
from pip.req import parse_requirements
 
reqs = [str(req.req) for req in parse_requirements('requirements.txt') if req]


EXCLUDE_FROM_PACKAGES = []


setup(
    name='colab',
    version='2.0a1',
    url='https://github.com/colab-community/colab',
    author='Sergio Oliveira',
    author_email='sergio@tracy.com.br',
    description='Collaboration platform for communities',
    license='LICENSE.txt',
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    include_package_data=True,
    zip_safe=False,
    long_description=open('README.rst').read(),
    install_requires=reqs,
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
