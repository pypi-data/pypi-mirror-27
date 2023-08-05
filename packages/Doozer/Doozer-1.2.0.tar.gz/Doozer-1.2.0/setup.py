from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand
import sys


class PyTest(TestCommand):
    def finalize_options(self):
        super().finalize_options()
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        sys.exit(pytest.main(self.test_args))


def read(filename):
    with open(filename) as f:
        return f.read()


setup(
    name='Doozer',
    version='1.2.0',
    author='Andy Dirnberger, Jon Banafato, and others',
    author_email='andy@dirnberger.me',
    url='https://doozer.readthedocs.io',
    description='A framework for running a Python service driven by a consumer',
    long_description=read('README.rst'),
    license='MIT',
    packages=find_packages(exclude=['tests']),
    zip_safe=False,
    install_requires=[
        # TODO: determine minimum versions for requirements
        'argh',
        'watchdog>=0.8.3',
    ],
    extras_require={
        'sphinx': [
            'sphinxcontrib-autoprogram>=0.1.3',
        ],
    },
    tests_require=[
        'pytest',
        'pytest-asyncio',
    ],
    cmdclass={
        'test': PyTest,
    },
    entry_points='''
        [console_scripts]
        doozer=doozer.cli:main
    ''',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ]
)
