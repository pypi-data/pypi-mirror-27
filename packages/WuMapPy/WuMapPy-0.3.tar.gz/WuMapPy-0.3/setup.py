# coding: utf8
"""
    wumappy
    -------

    Graphical user interface for sub-surface geophysical survey data processing

    :copyright: Copyright 2014 Lionel Darras and contributors, see AUTHORS.
    :license: GNU GPL v3.

"""
import re
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
from setuptools.command.install import install

README = ''
CHANGES = ''
try:
    README = open(os.path.join(here, 'README.rst')).read()
    CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()
except:
    pass

REQUIREMENTS = [
   'matplotlib', # depends on linux package libfreetype6-dev libpng12-0-dev
   'PySide',      # depends on linux package qt4-dev-tools 
   'geophpy==0.3'
]

with open(os.path.join(os.path.dirname(__file__), 'wumappy',
                       '__init__.py')) as init_py:
    release = re.search("VERSION = '([^']+)'", init_py.read()).group(1)
# The short X.Y version.
version = release.rstrip('dev')


## Custom setuptool install command class ----------------------------
class CustomInstallCommand(install):
    '''
    Customized setuptools install command

    Builds the package html documentation before installing it
    '''
    def run(self):
        # Building html doc
        print('Building package documentation')
        docspath= os.path.join(here, 'docs')
        os.chdir(docspath)
        os.system('make html')
        os.system('make clean')
        
        # Installing package
        print('Installing package')
        os.chdir(here)
        install.run(self)

        
setup(
    name='WuMapPy',
    version='0.3',
    license='GNU GPL v3',
    description='Graphical user interface for sub-surface geophysical survey data processing',
    long_description=README + '\n\n' + CHANGES,
    author='Lionel Darras, Philippe Marty & Quentin Vitale',
    author_email='lionel.darras@mom.fr',
    maintainer='Lionel Darras, Philippe Marty & Quentin Vitale',
    maintainer_email='lionel.darras@mom.fr',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS,
    data_files=[
        ('resources', ['wumappy/resources/wumappy.png'])
    ],
    entry_points={
        'console_scripts': [
            'wumappy = wumappy.__main__:main'
        ]
    },
    cmdclass={
        'install': CustomInstallCommand, # custom install command class
    }
)
