# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup


setup(
    name='econfig',
    version='1.0.1',
    description='Env variable configuration management',
    long_description=(open('README.rst').read() + '\n' +
                      open('CHANGES.rst').read()),
    keywords=['envronment', 'config'],
    author='Nathan Van Gheem',
    author_email='nathan@onna.com',
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    url='https://github.com/onna/envconfig',
    license='BSD',
    setup_requires=[
        'pytest-runner',
    ],
    zip_safe=True,
    include_package_data=True,
    packages=find_packages(),
    install_requires=[
    ],
    extras_require={
        'test': [
            'pytest'
        ]
    }
)
