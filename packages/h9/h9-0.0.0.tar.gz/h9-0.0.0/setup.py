from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='h9',
    version='0.0.0',
    description='h9 utils library',
    long_description=long_description,
    url='https://github.com/sq8kfh/pyh9',
    #download_url = 'https://github.com/sq8kfh/hamutils/tarball/v0.2.0',
    author='SQ8KFH',
    author_email='sq8kfh@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='h9',
    packages=find_packages(),
    python_requires='>=3.5',
    install_requires=[
        'lxml',
    ],
)
