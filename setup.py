from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='random_name',

    version='0.1.2',

    description='Generate random names',

    long_description="Generate random names based on US Census data, or files that you provide.",

    url='https://github.com/fitnr/random_name',

    author='Neil Freeman',

    author_email='contact@fakeisthenewreal.org',

    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='names development random',

    packages=['random_name', 'random_name/utils'],

    package_data={
        'random_name': ['data/*.csv'],
    },

    entry_points={
        'console_scripts': [
            'random_name=random_name.random_name:main',
        ],
    },

)