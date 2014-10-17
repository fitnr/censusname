Random Names
============

Generate random names based on US Census data, or files that you provide.

### Basic use

````python
from random_name import random_name

rn = random_name()

rn.generate()
'Jane Smith'
````

### Functions and Objects

#### `random_name`

The `random_name` object is the meat of the module. The formatting of the names it generates can be easily customized.

The simplest way to customize random_name is with the name_format argument
It takes a string with two formatting keys: 'given' and 'surname' (The format should look familiar from Python's [str.format](https://docs.python.org/2/library/stdtypes.html#str.format) builtin).

````python
from random_name import random_name

# Generate first names
first = random_name(nameformat='{given}')

# Generate names in last, first format
last_first = random_name(nameformat='{surname}, {given')

first.generate()
'Linda'

last_first.generate()
'Nguyen, Pamela'
````

#### `random_name.generate`

The `generate` function can be further customized. It also takes the nameformat argument, which overrides the default passed to `random_name`:

````python
rn.generate()
'Michael Fox'

# Add the same middle initial to all names
rn.generate(nameformat='{given} J. {surname}')
'Michael J. Fox'
````

Each part of the name is also a keyword argument. The default data set includes given name files broken up into male and female names. The module can be told to always use a certain file:

````python

rn.generate(given='female')
'Caroline Dippold'
````

Since the argument to `nameformat` is passed to Str.format, use any string formatting options, like padding:

````python

rn.generate(nameformat='{given:10}', given='male')
'Charles   '
````

The default dataset in random_names gives all names totally capitalized, and random_name changes them to title case. This can be turned off with a the capitalize argument, which works for both `random_name` and `random_name.generate`:

````python
rn = random_name(capitalize=False)
rn.generate()
'JOSE PETRIE'

rn2 = random_name()
rn2.generate(capitalize=False)
'WES REAVES'
````

Yes, it's a bit strange for `capitalize=False` to result in uppercase names. The false omits [str.capitalize](https://docs.python.org/2/library/stdtypes.html#str.capitalize), so the default capitalization from the raw data shines through, which happens to be all uppercase. You can customize the module arbitrary reformatting functions. Read on!

### Advanced

You can pass your own names file to `random_name` to generate names with arbitary formatting. For each section of a name, a different sets of files can be used. This could be useful if you have name data broken down by time, geography, or any other variable. By default, male and female first name data from 1990 are combined with last name data from 2000.

Files must have two fields: `name` and `cumulative_frequency`. By default, the package expects comma-delimited files, buy you can pass in `csv.DictReader` arguments with the paramenter `csv_args`.

The `cumulative_frequency` field should be calculated based on ascending frequency, and should be a number between from 0 to and some maximum - see the discussion of `max_frequencies` below.

By default, the name generator looks at separate lists of male and female names. You can specify lists for arbitrary groupings of names. Let's say you have name distribution data for two provinces in Spain. In Spain, two surnames are used: the paternal and maternal, so you have four files total for surnames, as well as general files for male and female first names.


````python
my_files = {
	'given': {
		'male': 'given-male.txt',
		'female': 'given-female.txt'
	},
	'paternal': {
		'sevilla': 'paternal-sevilla.txt',
		'toledo': 'paternal-toledo.txt'
	},
	'maternal': {
		'sevilla': 'maternal-sevilla.txt',
		'toledo': 'maternal-toledo.txt'
	}
}

# Perhaps you want to specify arguments to csv.DictReader, which will be reading the files
my_csv_args = {
	# Any arguments that can be passed to DictReader
}
````

The US Census names files don't contain every name, only those that cover about 90% of the population. With that in mind, `random_name` can take a `max_frequencies` argument to give these maximums. We specify these maximum with a dictionary whose keys are the file names.
If you give custom files but no `max_frequencies`, 100 will be used. (The max frequencies are hard coded for the default files.)

````python
# These are made-up numbers. Perhaps you prefer percentages:
maximums = {
	'given-male.txt': 89.7,
	'maternal-sevilla.txt': 90.4,
	# etc
}

# Or, you have a file where frequencies go from 0 to 1:
maximums = {
	'given-male.txt': 0.897,
	'maternal-sevilla.txt': 0.904,
	# etc
}
````

Also, we want to use a standard conjuction in the name:

````python
my_format = '{given} {paternal} y {maternal}'
````

Generating names with these examples:

````python
from random_name import random_name

my_generator = random_name(nameformat=my_format, namefiles=my_files, max_frequencies=maximums, csv_args=my_csv_args)

# Generate a name of the format 'Given Paternal y Maternal'
my_generator.generate()
'Luis de Góngora y Argote'

# Use a different format:
my_generator.generate(nameformat='{given} {paternal} de {maternal}')
'Pedro López de Ayala'

# Pick a name from the Sevilla files:
my_generator.generate(maternal='sevilla', paternal='sevilla')

# Pick a female name from the Toledo files:
# Note that any of the keys in my_files can be used as keyword arguments. The values should be keys from the respective dictionary.
my_generator.generate(given='female', maternal='toledo', paternal='toledo')

# By default, names are capitalized (title case).
# Generate a name using given capitalization in the files:
my_generator.generate(capitalize=False)

# By default, there's an equal probability of producing a name with a part from the Sevilla or Toledo lists.
# You have to do a little extra to weight that probability.
# Specify an 75% chance of a sevilla name, 25% chance of a toledo name:
province = random.choice(['sevilla'] * 3 + ['toledo'])
my_generator.generate(paternal=province, maternal=province)
````

### Example: Middle Names

Use the built-in data to fake middle names by randomly picking either a first or last name:

````python

import random_name

namefiles = random_name.NAMEFILES

# Add a middle name entry to the name files
namefiles['middle'] = {
	'last': random_name.SURNAME2000,
	'female': random_name.FEMALEFIRST1990,
	'male': random_name.MALEFIRST1990
}

rn_middle = random_name.random_name(namefiles, random_name.MAX_FREQUENCIES, '{given} {middle} {surname}')

# Generate a name in the format "given, middle, surname"
# However, this might return unlikely names
rn_middle.generate()
'John Mary Smith'

# Generated name will have a male first name and either a male given name or a surname as a middle name
rn_middle.generate(given='male', middle=['male', 'last'])
'Charles Michael Brescia'

# Generated name will have a female first name and either a female given name or a surname as a middle name
rn_middle.generate(given='female', middle=['female', 'last'])
'Mildred Hoang Hutton'
````

#### Formatters

You can specify arbitary reformatting functions that are run on each part of the name before they are returned. By default, the package includes a surname formatter that tries to intelligently format names like in the raw data like OHALLORAN (to O'Halloran).

You can specify formatters with a dict that targets each part of a name. The formatters should be a list of functions.

````python

my_formatters = {
	'given': [lambda x: x[::-1]], # reverse a string
	'surname': [lambda x: "De " + x],
}

rn = random_name(formatters=my_formatters)
rn.generate()
'ekiM De Morgan'
````

Additional formatters can be added to `random_name.generate`, they will be run in addition to any formatters included in the object.

````python
more_formatters = {
	'given': [lambda x: x.replace('a', 'b')]
}

rn.generate(formatters=more_formatters)
'nbhtbN De Scardino'
````

Note that passing a formatters argument to `random_name` will exclude the default surname formatter. It's easy enough to keep it, though:

````python
import random_name

my_formatters = {
	'surname': [random_name.formatters.recapitalize_surnames, custom_fuction]	
}
````