from setuptools import find_packages, setup

setup(
    name = 'with_fixture',
    version = '0.1',
    packages = find_packages(),

    # metadata for upload to PyPI
    author = 'Austin Bingham',
    author_email = 'austin.bingham@gmail.com',
    description = 'An experiment in using context-managers in unittest fixtures.',
    license = 'MIT',
    keywords = 'testing',
    url = 'http://github.com/abingham/with_fixture',

    install_requires=[
        'nose',
    ],
)
