#!/usr/bin/env python

import setuptools

readme = open('README.txt').read()
longDescription = open('DESCRIPTION.txt').read()

__version__ = '0.9'

setuptools.setup(
    name='unisos.icm',
    version=__version__,
    namespace_packages=['unisos'],
    packages=setuptools.find_packages(),   
    include_package_data=True,
    zip_safe=False,
    author='Mohsen Banan',
    author_email='http://mohsen.1.banan.byname.net',
    maintainer='Mohsen Banan',
    maintainer_email='http://mohsen.1.banan.byname.net',
    url='http://www.by-star.net/PLPC/180047',
    license='AGPL',
    description=readme,
    long_description=longDescription,
    download_url='http://www.by-star.net/PLPC/180047',
    install_requires=['unisos.ucf',],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: AGPL',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ]
    )
