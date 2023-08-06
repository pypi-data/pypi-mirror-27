import os.path as op

from setuptools import setup


with open(op.join(op.dirname(__file__), './README.rst')) as fin:
    long_description = fin.read()

setup(
        name='wcpan.worker',
        version='1.3.0',
        description='A multithread worker for Tornado',
        long_description=long_description,
        author='Wei-Cheng Pan',
        author_email='legnaleurc@gmail.com',
        url='https://github.com/legnaleurc/wcpan.worker',
        packages=[
            'wcpan.worker',
        ],
        install_requires=[
            'tornado >= 5',
            'wcpan.logger',
        ],
        classifiers=[
            'Programming Language :: Python :: 3 :: Only',
            'Programming Language :: Python :: 3.5',
        ])
