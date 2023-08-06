import datetime
from codecs import open
from os import path
from setuptools import setup, find_packages
from megalus import __version__


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

install_requires = [
    'buzio',
    'requests',
    'PyYAML',
    'docopt',
    'tabulate',
    'colorama'
]

if 'dev' in __version__:
    now = datetime.datetime.now()
    release_number = (now - datetime.datetime(2017, 12, 16)
                      ).total_seconds() / 60
    version = "{}{}".format(__version__, int(release_number))
else:
    version = __version__

setup(
    name='Megalus',
    version=version,
    description='Command line tools for Docker based projects',
    long_description=long_description,
    author='Chris Maillefaud',
    include_package_data=True,
    # Choose your license
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3.6'
    ],
    keywords='aws deploy docker npm redis memcached bash',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'meg=megalus.run:main'
        ],
    },
)
