#!/usr/bin/env python2.7

import os
import apt
import apt_pkg
import locale
import platform
import subprocess
import urllib

from apt import debfile
from distutils.version import StrictVersion
from pkg_resources import parse_requirements
from shutil import copyfile
from subprocess import check_output


PUPPET_TARGET_VERSION="3.4.3-1"
PUPPET_DIR = os.path.join(os.path.dirname(__file__))
MODULES_FILE_PATH = os.path.join(PUPPET_DIR, 'modules.txt')


def get_package(name):
    cache = apt.cache.Cache()
    if name in cache:
        return cache[name], cache

    return None, None


def pkg_available(name):
    pkg = get_package(name)[0]
    if pkg and pkg.versions.get(PUPPET_TARGET_VERSION):
        return True

    return False


def config_puppetlabs_repo():
    dist = platform.dist()[-1]

    url = 'http://apt.puppetlabs.com/puppetlabs-release-{}.deb'.format(dist)
    filename = '/tmp/puppet_apt.deb'
    try:
        urllib.urlretrieve(url, filename)
    except IOError:
        print "Could not install puppet"
        raise

    deb_pkg = debfile.DebPackage(filename)
    if deb_pkg.check():
        deb_pkg.install()
        cache = apt.cache.Cache()
        cache.update()
        cache.open()


def install_puppet(upgrade=False):
    pkg, cache = get_package('puppet')

    pkg.candidate = pkg.versions.get(PUPPET_TARGET_VERSION)
    if upgrade:
        pkg.mark_upgrade()
    else:
        pkg.mark_install()

    cache.commit()


def get_modules_installed():
    modules_list = check_output(['puppet', 'module', 'list']).split('\n')
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
        version = ' --version {}'.format(version)

    cmd = 'puppet module {} {}{}'.format(cmd, module, version)
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
                version_comparison = apt_pkg.version_compare(
                    modules_installed[module.project_name],
                    version
                )
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

def main():
    # If the package not found or if the version is outdated, install puppet
    if not pkg_available('puppet'):
        config_puppetlabs_repo()

    pkg = get_package('puppet')[0]
    if not pkg.is_installed:
        install_puppet()
    elif apt_pkg.version_compare(pkg.installed.version,
                                 PUPPET_TARGET_VERSION) < 0:
        install_puppet(upgrade=True)

    if os.path.isfile('/vagrant/puppet/hiera.yaml'):
        copyfile('/vagrant/puppet/hiera.yaml', '/etc/puppet/hiera.yaml')

    locale.setlocale(locale.LC_ALL, '')

    install_puppet_modules()


if __name__ == '__main__':
    main()
