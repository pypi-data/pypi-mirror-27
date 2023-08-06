#!/usr/bin/env python

import versioneer
from setuptools import setup, find_packages

tests_require = ['pytest', 'pytest-cov', 'mock', 'pep8', 'pylint==1.6.4', 'hypothesis', 'compliance-checker']

extras_require = {
    'performance': ['ciso8601', 'bottleneck'],
    'interactive': ['matplotlib', 'fiona'],
    'distributed': ['distributed', 'dask[distributed]'],
    'analytics': ['scipy', 'pyparsing', 'numexpr'],
    'doc': ['Sphinx', 'setuptools'],
    'replicas': ['paramiko', 'sshtunnel', 'tqdm'],
    'celery': ['celery>=4', 'redis'],
    'test': tests_require,
}
# An 'all' option, following ipython naming conventions.
extras_require['all'] = sorted(set(sum(extras_require.values(), [])))

setup(
    name='datacube',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),

    url='https://github.com/opendatacube/datacube-core',
    author='AGDC Collaboration',
    maintainer='AGDC Collaboration',
    maintainer_email='',
    description='An analysis environment for satellite and other earth observation data',
    long_description=open('README.rst').read(),
    license='Apache License 2.0',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: BSD",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],

    packages=find_packages(
        exclude=('tests', 'tests.*',
                 'integration_tests', 'integration_tests.*')
    ),
    package_data={
        '': ['*.yaml', '*/*.yaml'],
    },
    scripts=[
        'datacube_apps/scripts/pbs_helpers.sh'
    ],
    setup_requires=[
        'pytest-runner'
    ],
    install_requires=[
        'affine',
        'cachetools',
        'click>=5.0',
        'dask[array]',
        'jsonschema',
        'netcdf4',
        'numpy',
        'pathlib',
        'psycopg2',
        'pypeg2',
        'python-dateutil',
        'pyyaml',
        'rasterio>=0.9',  # required for zip reading, 0.9 gets around 1.0a ordering problems
        'singledispatch',
        'sqlalchemy',
        'xarray>=0.9',  # >0.9 fixes most problems with `crs` attributes being lost
    ],
    extras_require=extras_require,
    tests_require=tests_require,

    entry_points={
        'console_scripts': [
            'datacube-search = datacube.scripts.search_tool:cli',
            'datacube = datacube.scripts.cli_app:cli',
            'datacube-stacker = datacube_apps.stacker:main',
            'datacube-worker = datacube.execution.worker:main',
            'datacube-fixer = datacube_apps.stacker:fixer_main',
            'datacube-ncml = datacube_apps.ncml:ncml_app',
            'pixeldrill = datacube_apps.pixeldrill:main [interactive]',
            'movie_generator = datacube_apps.movie_generator:main',
            'datacube-simple-replica = datacube_apps.simple_replica:replicate'
        ]
    },
)
