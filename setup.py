from setuptools import setup

__version__ = '0.0.1a'

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

extra_setuptools_args = dict(
    tests_require=['pytest']
    )

setup(
    name='abbreviations',
    version=__version__,
    description='Abbreviation detection for raw APA-format text in Python',
    maintainer='Taylor Salo',
    maintainer_email='tsalo006@fiu.edu',
    install_requires=['nltk'],
    packages=['abbreviations'],
    license='MIT',
    **extra_setuptools_args
)
