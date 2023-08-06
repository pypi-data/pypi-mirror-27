#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Setup file for pyconrad.

    This file was generated with PyScaffold 2.5.7.post0.dev6+ngcef9d7f, a tool that easily
    puts up a scaffold for your new Python project. Learn more under:
    http://pyscaffold.readthedocs.org/
"""

import os
import sys
from setuptools import setup
from setuptools.command.install import _install

# post install hint from:
# https://stackoverflow.com/questions/17806485/execute-a-python-script-post-install-using-distutils-setuptools


def _post_install(dir):
    cwd = os.path.join(dir, 'pyconrad')
    #os.path.append(os.path.join( os.path.dirname(__file__), 'pyconrad'))
    sys.path.append(cwd)
    import _download_conrad
    _download_conrad.download_conrad(cwd)
    print("CONRAD has been installed to %s" %
          _download_conrad.conrad_jar_dir())


class install(_install):
    def run(self):
        _install.run(self)
        self.execute(_post_install, (self.install_lib,),
                     msg="Installing Java dependencies...")


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def setup_package():
    needs_sphinx = {'build_sphinx', 'upload_docs'}.intersection(sys.argv)
    sphinx = ['sphinx'] if needs_sphinx else []
    setup(name='pyconrad',
          version='0.0.7',
          packages=['pyconrad', 'pyconrad._autocomplete_files',
                    'pyconrad.utils'],
          author='Andreas Maier',
          author_email='andreas.maier@fau.de',
          license='GPL 3.0',
          install_requires=[
               'jpype1', 'numpy', 'pathlib', 'urllib3', 'pyevtk', 'setuptools'
          ],
          cmdclass={'install': install},
          url='https://git5.cs.fau.de/PyConrad/pyCONRAD/',
          description='Python wrapper for CONRAD (https://www5.cs.fau.de/conrad/), a framework for cone beam radiography',
          long_description=read('README.md'),
          entry_points={
              'gui_scripts': [
                  'conrad = pyconrad._scripts:start_pyconrad',
                  'conrad_imagej = pyconrad._scripts:start_conrad_imagej',
              ]
          },
          setup_requires=['pytest-runner', 'install_freedesktop'],
          tests_require=['pytest']
          )
    #setup_requires=['six', 'pyscaffold>=2.5a0,<2.6a0'] + sphinx,
    # use_pyscaffold=True)


if __name__ == "__main__":
    setup_package()
