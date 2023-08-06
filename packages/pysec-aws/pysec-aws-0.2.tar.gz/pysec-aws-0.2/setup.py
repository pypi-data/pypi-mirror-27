from setuptools import setup
import os
import re
import codecs

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='pysec-aws',
    version=find_version("pysec", "__init__.py"),
    packages=['pysec'],
    entry_points={
        "console_scripts": [
            "pysec = cli:main",
        ]
    },
    long_description=open('README.md').read(),
    install_requires=[
        "troposphere",
        "netaddr",
        "argparse",
        "tabulate",
        "boto3"
    ],
)