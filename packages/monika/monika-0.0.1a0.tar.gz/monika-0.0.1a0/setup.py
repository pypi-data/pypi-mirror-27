#! /usr/bin/env python

from setuptools import setup, find_packages

DISTNAME = 'monika'
DESCRIPTION = 'Build modular Discord bots with ease.'
MAINTAINER = 'Kira Evans'
MAINTAINER_EMAIL = 'contact@kne42.me'
URL = 'http://just-monika.club'
LICENSE = 'Modified BSD'
DOWNLOAD_URL = 'https://github.com/just-monika/just-monika'
PACKAGES = find_packages()

for line in open('monika/__init__.py'):
    if line.startswith('__version__'):
        VERSION = line.strip().split()[-1][1:-1]
        break

if __name__ == '__main__':
    setup(
        name=DISTNAME,
        description=DESCRIPTION,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        url=URL,
        license=LICENSE,
        download_url=DOWNLOAD_URL,
        version=VERSION,
        packages=PACKAGES
    )
