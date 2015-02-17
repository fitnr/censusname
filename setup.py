from setuptools import setup

try:
    from pypandoc import convert
    def read_md(f):
        try:
            return convert(f, 'rst')
        except IOError:
            return ''

except ImportError:
    print("pypandoc module not found, could not convert Markdown to RST")
    def read_md(f):
        try:
            return open(f, 'r').read()
        except IOError:
            return ''


setup(
    name='censusname',

    version='0.2.1-1',

    description='Generate random names',

    long_description="Generate random names based on US Census data, or other data you provide.",

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
