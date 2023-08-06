from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='assurest',
    version='0.2',
    description='Nice looking tests for REST servers',
    long_description='''Assurest is a library that wraps http requests and validation,
                        you allowing to write it in a single line of chained methods.''',
    url='https://github.com/staudt/assurest',

    author='Ricardo Staudt',
    author_email='ricardost@gmail.com',
    license='MIT',

    classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Build Tools',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
    ],
    
    keywords='test setuptools development',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    
    install_requires=['requests'],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
)