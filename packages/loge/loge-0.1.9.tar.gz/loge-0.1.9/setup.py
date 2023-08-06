# -*- coding: utf-8 -*-

from glob import glob
from distutils.core import setup
from setuptools import find_packages
from os.path import splitext, basename

setup(
    name='loge',
    version='0.1.9',
    description='Easy and fast dynamic report generation with Python3',
    long_description = open("README.rst").read(),
    author='Lukasz Laba',
    author_email='lukaszlab@o2.pl',
    url='https://loge.readthedocs.io',
    license = 'GNU General Public License (GPL)',
    keywords = 'notebook ,script, report',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        ],
    python_requires='>=3.5, <4',
    package_dir={'': 'src'},  # tell distutils packages are under src
    packages=find_packages('src'),  # include all packages under src
    include_package_data=True, # include everything in source control
    # ...but exclude README.txt from all packages
    exclude_package_data={'': ['README.txt']},
    install_requires=['pyqt5>=5.6','mistune>=0.7.4'],        
    entry_points={
        'console_scripts':['loge = loge.__main__:main']
        }
    )
