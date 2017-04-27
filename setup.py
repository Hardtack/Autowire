import sys

import setuptools
from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='Autowire',
    packages=setuptools.find_packages(exclude=['tests']),
    version='0.1.2',
    description="Simple dependency injection.",
    author='Geonu Choi',
    author_email='6566gun@gmail.com',
    url='https://github.com/hardtack/autowire',
    license='MIT LICENSE',
    keywords=['dependency-injection'],
    # Cmd
    cmdclass={
        'test': PyTest,
    }
)
