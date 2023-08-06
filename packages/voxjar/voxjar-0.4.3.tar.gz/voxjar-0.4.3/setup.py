#!/usr/bin/env python
from __future__ import print_function
import os
import shutil
import glob
import subprocess
import setuptools

package_dir = 'voxjar'


class CustomCleanCommand(setuptools.Command):
    description = 'remove build files'
    user_options = []

    def initialize_options(self):
        """Set default values for options."""
        pass

    def finalize_options(self):
        """Post-process options."""
        pass

    def run(self):
        """Run clean."""

        def respect_dry_run(path, fn):
            if self.dry_run:
                print('would remove {}...'.format(path))
            else:
                if self.verbose > 1:
                    print('removing {}...'.format(path))
                fn(path)

        for d in [
                './dist/', './build/', './__pycache__/',
                './{}.egg-info/'.format(package_dir)
        ]:
            if os.path.isdir(d):
                respect_dry_run(d, shutil.rmtree)

        for f in glob.glob('*.pyc'):
            respect_dry_run(f, os.remove)


class CustomDocsCommand(setuptools.Command):
    description = 'build documentation'
    user_options = []

    def initialize_options(self):
        """Set default values for options."""
        pass

    def finalize_options(self):
        """Post-process options."""
        pass

    def run(self):
        """Run build docs."""
        shutil.rmtree('./docs/_build')
        subprocess.check_output(['make', '-C', 'docs', 'html'])
        subprocess.check_output(['open', './docs/_build/html/index.html'])


with open("README.rst") as readme_file:
    readme = readme_file.read()

setuptools.setup(
    name='voxjar',
    version='0.4.3',
    description='python implementation of the Voxjar API',
    long_description=readme,
    author='William Myers',
    author_email='will@voxjar.com',
    url='https://github.com/voxjar/voxjar',
    install_requires=['requests', 'gql'],
    extras_require={'docs': ['sphinx'],
                    'dev': ['wheel', 'twine']},
    python_requires='>=2.7',
    packages=setuptools.find_packages(exclude=['docs', 'tests*']),
    cmdclass={
        'clean': CustomCleanCommand,
        'docs': CustomDocsCommand,
    },
    license='Apache-2',
    keywords='voxjar voxjar ai requests',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
    ])
