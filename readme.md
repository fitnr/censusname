Random Names
============

Generate random names based on US Census data, or files that you provide.

Basic use:

````python
from random_name import random_name

rn = random_name(nameformat='{given}')
rn.generate()
````

To generate just first names:

````python
from random_name import random_name

first = random_name(nameformat='{given}')

# Returns a first name
first.generate()

# Returns a male first name 
first.generate(given='male')
````

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

# Specify arguments for how you want csv.DictReader to read your files.
my_csv_args = {
	delimiter = "\t"
}
````

The US Census names files don't contain every name, only those that cover about 90% of the population. With that in mind, `random_name` can take a `max_frequencies` argument to give these maximums. We specify these maximum with a dictionary whose keys are the file names.
If you give custom files but no `max_frequencies`, 100 will be used. (The max frequencies are hard coded for the default files.)

````python
maximums = {
	'given-male.txt': 89.75356,
	'maternal-sevilla.txt': 90.483,
	# etc
}

# Or, you may have a file where frequencies go from 0 to 1:
maximums = {
	'given-male.txt': 0.8975356,
	'maternal-sevilla.txt': 0.90483,
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

my_generator = random_name(my_files, maximums, my_format, csv_args=my_csv_args)

# Generate a name of the format 'Given Paternal y Maternal'
my_generator.generate()

# Use a different format:
my_generator.generate(nameformat='{given} {paternal} de {maternal}')

# Pick a name from the Sevilla files:
my_generator.generate(maternal='sevilla', paternal='sevilla')

# Pick a female name from the Toledo files:
# Note that any of the keys in my_files can be used as keyword arguments. The values should be sections
my_generator.generate(given='female', maternal='toledo', paternal='toledo')

# Pick a name using the capitalization in the files:
my_generator.generate(capitalize=False)

# By default, there's an equal probability of producing a name with a part from the Sevilla or Toledo lists.
# You have to do a little extra to weight that probability.
# Specify an 60% chance of a sevilla name, 40% chance of a toledo name:
province = random.choice(['sevilla'] * 6 + ['toledo'] * 4)
my_generator.generate(paternal=province, maternal=province)
````

### Example: Middle Names

Use the built-in data to fake middle names by randomly picking either a first or last name. It's unusual to :

````python

import random_name

namefiles = random_name.NAMEFILES

# Add a middle name entry to the name files
namefiles['middle'] = {
	'last': random_name.SURNAME2000,
	'female': random_name.FEMALEFIRST1990,
	'male': random_name.MALEFIRST1990
}

middle = random_name.random_name(namefiles, random_name.MAX_FREQUENCIES, '{given} {middle} {surname}')

# Generate a name in the format "given, middle, surname"
# However, this might return "John Mary Smith", which is probably an unlikely name
middle.generate()

# Generated name will have a male first name and either a male given or a surname as a middle name
middle.generate(given='male', middle=['male', 'last'])

# Generated name will have a female first name and either a male given or a surname as a middle name
middle.generate(given='female', middle=['female', 'last'])

````