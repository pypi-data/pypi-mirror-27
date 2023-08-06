from setuptools import setup, find_packages
import os

# Utility function to read the README file.
def read(fname):
        return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="embc",
    version="0.1.1",
    author="Martin Sivak",
    author_email="mars@montik.net",
    description='Companion script for embedded cmake',
    url='http://github.com/MarSik/embc',
    license="ASL2",
    keywords="embedded cmake",
    packages=find_packages(),
    package_data={"embedded_cmake": ["templates/*"]},
    scripts=["embc"],
    # TODO add template files from embedded_cmake/templates
    setup_requires=[
        'nose>=1.0',
        'gitpython',
        'docopt',
        'jinja2',
        'requests'
    ],
    test_suite="embc",
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Software Development :: Build Tools"
    ]
)
