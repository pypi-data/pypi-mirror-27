import sys
import subprocess
import os
import shutil
# To use a consistent encoding
from codecs import open
# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from setuptools.command.install import install

version_py = open(
    os.path.join(os.path.dirname(__file__), 'version.py')
).read().strip().split('=')[-1].replace('"', '')

class InstallAICS(install):
    """Customized setuptools install command - builds protos on install."""
    def run(self):
        make_cxform_cmd = ["make", "-C", "cxform"]
        if subprocess.call(make_cxform_cmd) != 0:
            sys.exit(-1)
        if sys.platform == 'wind32' or sys.platform == 'cygwin':
            shutil.copy(
                os.path.join("cxform", "cxform-c.dll"),
                os.path.join("src", "ai")
            )
        else:
            shutil.copy(
                os.path.join("cxform", "cxform-c.so"),
                os.path.join("src", "ai")
            )
        install.run(self)

# Get the long description from the README file
with open(
    os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.rst'),
    encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ai.cs',
    version='{ver}'.format(ver=version_py),
    description='Coordinates transformation package for geocentric, heliocentric and geometrical coordinates',
    long_description=long_description,
    url='https://bitbucket.org/isavnin/ai.cs',
    author='Alexey Isavnin',
    author_email='alexey.isavnin@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    keywords='coordinates transformation cxform heliocentric geocentric',
    cmdclass={
        'install': InstallAICS
    },
    packages=find_packages('src', exclude=['tests*']),
    package_dir={'': 'src'},
    package_data={'': ['cxform-c.so', 'cxform-c.dll']},
    include_package_data=True,
    install_requires=['numpy']
)
