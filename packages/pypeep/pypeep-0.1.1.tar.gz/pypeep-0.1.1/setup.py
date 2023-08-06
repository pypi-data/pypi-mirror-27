import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass into py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ['--cov=pypeep']

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


install_requirements = [
    "paramiko",
    "docker",
    "colorama",
    "psutil",
]

test_requirements = [
    "pytest",
    "pytest-cov",
    "coveralls",
]

setup(
    name="pypeep",
    version="0.1.1",
    keywords=("PyCharm", "debug", "remote debug"),
    description="debug configurator",
    long_description="Configure Pycharm for remote debugging",
    license="MIT",

    url="https://github.com/cuyu/pypeep",
    author="cuyu",
    author_email="cuyu@splunk.com",

    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 2.7'
    ],
    platforms="any",
    install_requires=install_requirements,
    cmdclass={
        'test': PyTest,
    },
    extras_require={
        'test': test_requirements,
    },
    entry_points={
        'console_scripts': ['pypeep = pypeep.main:main']
    }
)
