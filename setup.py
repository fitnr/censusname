from setuptools import setup

try:
    readme = open('README.rst').read()
except IOError:
    try:
        readme = open('README.md').read()
    except IOError:
        readme = ''

setup(
    name='censusname',

    version='0.2.2',

    description='Generate random names',

    long_description=readme,

    url='https://github.com/fitnr/censusname',

    author='Neil Freeman',

    author_email='contact@fakeisthenewreal.org',

    license='GPL',

    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],

    keywords='names development random',

    packages=['censusname',],

    package_data={
        'censusname': ['data/*.csv'],
    },

    zip_safe=True,

    use_2to3=True,

)
