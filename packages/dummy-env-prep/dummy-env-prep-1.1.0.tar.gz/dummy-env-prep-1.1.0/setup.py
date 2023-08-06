"""package control"""
from codecs import open

from setuptools import setup

__package_name__ = 'dummy-env-prep'
__version__ = '1.1.0'

with open('README.rst', 'r', 'utf-8') as fh:
    README = fh.read()

with open('requirements.txt', 'r', 'utf-8') as fh:
    REQUIREMENTS = fh.read()

def make_readme():
    """generate README and append `requirements.txt` into it"""
    tabbed_requirements = ['\t' + line for line in REQUIREMENTS.splitlines()]
    return """
{readme}

Includes
========

.. code-block::

    {requirements}

""".format(
        readme=README,
        requirements='\n'.join(tabbed_requirements)
    )

setup(
    name=__package_name__,
    description='A handy template for including requirements in an environment',
    long_description=make_readme(),
    version=__version__,
    author='John Purcell',
    author_email='jpurcell.ee@gmail.com',
    url='https://github.com/lockefox/' + __package_name__,
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Build Tools',
    ],
    keywords='environment setup requirements packaging automation',
    package_data={
        '': ['LICENSE', 'README.rst', 'requirements.txt']
    },
    install_requires=REQUIREMENTS.splitlines()
)
