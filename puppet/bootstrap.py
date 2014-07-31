#!/usr/bin/env python

import os
import re
import locale
import platform
import subprocess
import urllib

from distutils.version import StrictVersion
from shutil import copyfile

try:
    from pkg_resources import parse_requirements
except ImportError:
    # Needed dependency for import pkg_resources
    pkg_res = ['apt-get', 'install', 'python-pkg-resources', '-y']
    subprocess.call(pkg_res)
    from pkg_resources import parse_requirements

PUPPET_TARGET_VERSION = "3.6.2"
PUPPET_DIR = os.path.join(os.path.dirname(__file__))
MODULES_FILE_PATH = os.path.join(PUPPET_DIR, 'modules.txt')


def get_release_name():
    distro = platform.dist()[0].lower()
    if distro == 'centos':
        with open('/etc/centos-release') as release_file:
            regex = r'CentOS release (\d)'
            release = re.search(regex, release_file.read()).group(1)
            return 'centos', release
    elif distro == 'ubuntu':
        with open('/etc/lsb-release') as release_file:
            regex = r'DISTRIB_CODENAME=([a-z]+)'
            release = re.search(regex, release_file.read()).group(1)
            return 'ubuntu', release
    else:
        return '', ''


def get_modules_installed():
    modules_list = os.popen('puppet module list').read().split('\n')
    modules_list = [line for line in modules_list if 'no modules' not in line]
    modules_list = [item.split()[1:] for item in modules_list]
    modules_list = [item for item in modules_list if item]
    modules_dict = {}
    for name, version in modules_list:
        modules_dict[name] = version.split('v')[1].replace(
            '\x1b[0m)',
            ''
        )
    return modules_dict


def run(cmd, module, version=''):
    if version:
        version = ' --version %s' % (version)

    cmd = 'puppet module %s %s%s' % (cmd, module, version)
    process = subprocess.Popen(cmd, shell=True, executable='/bin/bash')
    process.wait()


def install_puppet_modules():
    modules_installed = get_modules_installed()

    with open(MODULES_FILE_PATH) as modules_file:
        modules_requirements = modules_file.read().replace('/', '-')

    for module in parse_requirements(modules_requirements):
        current_cmd, compare, version, version_comparison = '', '', '', None
        if module.project_name in modules_installed:
            if module.specs:
                compare, version = module.specs[0]

                tmp_version = modules_installed[module.project_name]
                installed_version = StrictVersion(tmp_version)
                required_version = StrictVersion(version)

                if installed_version >= required_version:
                    version_comparison = 0
                else:
                    version_comparison = -1
            else:
                continue

            if version_comparison == 0 and compare is not '>':
                # module version installed is equal version
                continue
            else:
                # module version installed is smaller or bigger than version
                current_cmd = 'upgrade'
        else:
            current_cmd = 'install'

        if version and compare and '>' not in compare:
            run(current_cmd, module.project_name, version)
        else:
            if not version_comparison or version_comparison < 0:
                run(current_cmd, module.project_name)


def iscentos(distro):
    return distro == 'centos'


def isubuntu(distro):
    return distro == 'ubuntu'


def download(url, filename):
    try:
        urllib.urlretrieve(url, filename)
    except IOError:
        print "Could not install puppet"
        raise


def main():
    distro, release = get_release_name()
    print('Distro %s, release %s' % (distro, release))

    if iscentos(distro):
        cmd = 'rpm'
        flags = '-ivh'
        url = 'http://yum.puppetlabs.com/'
        pkg = 'puppetlabs-release-el-%s.noarch.rpm' % (release)
        update = ['yum', 'update', '-y']
        install = ['yum', 'install', 'puppet', '-y']
    elif isubuntu(distro):
        cmd = 'dpkg'
        flags = '-i'
        url = 'https://apt.puppetlabs.com/'
        pkg = 'puppetlabs-release-%s.deb' % (release)
        update = ['apt-get', 'update', '-y']
        install = ['apt-get', 'install', 'puppet', '-y']

    else:
        print('This distribuition is currently not supported!')
        print('exiting...')
        exit(1)

    tmp_file = '/tmp/%s' % (pkg)
    download(url + pkg, tmp_file)
    args = [cmd, flags, tmp_file]

    # Add repository
    result = subprocess.call(args)
    if result != 0:
        print('Repository %s already set' % pkg)

    # Install Puppet
    subprocess.call(update)
    result = subprocess.call(install)
    if result != 0:
        print('Failed installing puppet')
        exit(result)

    if os.path.isfile('/vagrant/puppet/hiera.yaml'):
        copyfile('/vagrant/puppet/hiera.yaml', '/etc/puppet/hiera.yaml')

    locale.setlocale(locale.LC_ALL, '')

    install_puppet_modules()


if __name__ == '__main__':
    main()
