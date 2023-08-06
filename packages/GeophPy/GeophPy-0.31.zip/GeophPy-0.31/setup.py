# coding: utf8
"""
    geophpy
    -------

    Tools for sub-surface geophysical survey data processing.

    :copyright: Copyright 2014 Lionel Darras and contributors, see AUTHORS.
    :license: GNU GPL v3.

"""
import os
from setuptools import setup, find_packages
from setuptools.command.install import install

here = os.path.abspath(os.path.dirname(__file__))

README = ''
CHANGES = ''
try:
    README = open(os.path.join(here, 'README.rst')).read()
    CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()
except:
    pass

REQUIREMENTS = [
    'netcdf4',    # depends on linux packages libhdf5-dev, libnetcdf-dev
    'matplotlib', # depends on ???
    'numpy',
    'scipy',      # depends on ???
    'pillow',     # depends on linux packages libjpeg ...
    'pyshp',
    'simplekml',
    'utm',
    'Sphinx>=1.4.3' # depends on linux packages latexmk, dvipng
]

## Custom setuptool install command class ----------------------------
class CustomInstallCommand(install):
    '''
    Custom command that builds the package html documentation before
    installing it.
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
        # Recommended call to 'install.run(self)' will ignores the
        # install_requirements.
        # The underlying bdist_egg is called instead.
        self.do_egg_install()
        ##install.run(self)  # ignores install_requirements
        
setup(
    name='GeophPy',
    version='0.31',
#    url='https://github.com/LionelDarras/GeophPy',
    license='GNU GPL v3',
    description='Tools for sub-surface geophysical survey data processing',
    long_description=README + '\n\n' + CHANGES,
    author='Lionel Darras, Philippe Marty & Quentin Vitale',
    author_email='lionel.darras@mom.fr',
    maintainer='Lionel Darras, Philippe Marty & Quentin Vitale',
    maintainer_email='lionel.darras@mom.fr',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS,
    cmdclass={
        'install': CustomInstallCommand,  # custom install command
    }
)
