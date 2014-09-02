#!/usr/bin/env python

import os
import re
import platform
import subprocess
import urllib

from distutils.version import StrictVersion
from shutil import copyfile

try:
    from pkg_resources import parse_requirements, to_filename
except ImportError:
    # Import local version if not installed
    from pkg_resources_local import parse_requirements, to_filename

PUPPET_TARGET_VERSION = "3.6.2"
PUPPET_DIR = os.path.join(os.path.dirname(__file__))
HIERA_FILE = os.path.join(PUPPET_DIR, 'hiera.yaml')
MODULES_FILE_PATH = os.path.join(PUPPET_DIR, 'modules.txt')

DIST_CMD = {
    'ubuntu': {
        'pkg_manager': 'apt-get',
        'pkg_flags': '-y',
        'rep_manager': 'dpkg',
        'rep_flags': '-i',
        'puppet_repo': 'https://apt.puppetlabs.com/',
        'puppet_pkg': 'puppetlabs-release-%s.deb',
    },
    'centos': {
        'pkg_manager': 'yum',
        'pkg_flags': '-y',
        'rep_manager': 'rpm',
        'rep_flags': '-ivh',
        'puppet_repo': 'http://yum.puppetlabs.com/',
        'puppet_pkg': 'puppetlabs-release-el-%s.noarch.rpm',
    },
}


def add_puppet_repository():
    distro, release = get_release_name()
    cmd_dict = DIST_CMD[distro]
    rep_manager = cmd_dict['rep_manager']
    flags = cmd_dict['rep_flags']
    puppet_repo = cmd_dict['puppet_repo']
    puppet_pkg = cmd_dict['puppet_pkg'] % (release)

    # Download repository file
    tmp_file = '/tmp/%s' % (puppet_pkg)
    download(puppet_repo + puppet_pkg, tmp_file)

    # Add repository
    cmd = [rep_manager, flags, tmp_file]
    if subprocess.call(cmd) != 0:
        print('Repository %s already set' % puppet_pkg)


def package_install(package):
    distro, release = get_release_name()
    cmd_dict = DIST_CMD[distro]
    pkg_manager = cmd_dict['pkg_manager']
    flags = cmd_dict['pkg_flags']
    cmd = [pkg_manager, flags, 'install', package]
    return subprocess.call(cmd)


def distro_update():
    distro, release = get_release_name()
    cmd_dict = DIST_CMD[distro]
    pkg_manager = cmd_dict['pkg_manager']
    flags = cmd_dict['pkg_flags']
    cmd = [pkg_manager, flags, 'update']
    return subprocess.call(cmd)


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
        module_name = to_filename(module.project_name).replace('_', '-', 1)
        if module_name in modules_installed:
            if module.specs:
                compare, version = module.specs[0]

                tmp_version = modules_installed[module_name]
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
            run(current_cmd, module_name, version)
        else:
            if not version_comparison or version_comparison < 0:
                run(current_cmd, module_name)


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

    if not os.path.exists('/usr/bin/puppet'):

        # Add repository
        add_puppet_repository()

        # Install Puppet
        if isubuntu(distro):
            distro_update()

        result = package_install('puppet')
        if result != 0:
            print('Failed installing puppet')
            exit(result)

    if os.path.isfile(HIERA_FILE):
        copyfile(HIERA_FILE, '/etc/puppet/hiera.yaml')

    install_puppet_modules()


if __name__ == '__main__':
    main()
