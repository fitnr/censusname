Census Name
============

Generate random names based on US Census data, or files that you provide.

### Basic use

The simplest way to use censusname is with the `generate` method. It generates a names based on last and first name distributions in the 2000 Census. It has a 50/50 chance of providing a first name from either the `female` or `male` lists.

````python
import censusname
censusname.generate()
'Jane Smith'
````

Or, on the command line, run:
````
python -m censusname
````

The simplest way to customize Censusname is with the name_format argument
It takes a string with two formatting keys: 'given' and 'surname' (The format should look familiar from Python's [str.format](https://docs.python.org/2/library/stdtypes.html#str.format) builtin).

````python
import censusname

# Generate first names
censusname.generate(nameformat='{given}')
'Linda'

# Generate names in last, first format
censusname.generate(nameformat='{surname}, {given')
'Nguyen, Pamela'
````

### Methods and Objects

#### `generate`

Generates random names. See below for details on valid arguments.

#### `Censusname`

The `generate` method is called on a default instance of the `Censusname` object. `Censusname` is the meat of the module, and instances a can be created with custom formatting and custom lists of names.

Keyword arguments: `nameformat`, `namefiles`, `max_frequencies`, `formatters`, `capitalize`. 

````python
from censusname import Censusname

last_first = Censusname(nameformat='{surname}, {given}')
last_first.generate()
'Lashley, Emily'
````

#### `Censusname.generate`

````python
C = Censusname()
C.generate()
'Michael Fox'

# Add the same middle initial to all names
C.generate(nameformat='{given} J. {surname}')
'Michael J. Fox'
````

Each part of the name is also a keyword argument. The default data set includes given name files broken up into male and female names. The module can be told to always use a certain file:

````python
C.generate(given='female')
'Caroline Dippold'
````

Since the argument to `nameformat` is passed to Str.format, one can use any string formatting options, like padding:

````python
C.generate(nameformat='{given:10}', given='male')
'Charles   '
````

The default dataset in censusname gives all names totally capitalized, and censusname changes them to title case. This can be turned off with a the capitalize argument, which works for both `Censusname` and `Censusname.generate`:

````python
C.generate(capitalize=False)
'WES REAVES'

# or, create your own Censusname object
from censusname import Censusname
C = Censusname(capitalize=False)
C.generate()
'JOSE PETRIE'
````

Yes, it's a bit strange for `capitalize=False` to result in uppercase names. The false omits [str.capitalize](https://docs.python.org/2/library/stdtypes.html#str.capitalize), so the default capitalization from the raw data shines through, which happens to be all uppercase. You can customize the module arbitrary reformatting methods. Read on!

### Advanced

You can pass your own names file to `Censusname` to generate names with arbitary formatting. For each section of a name, a different sets of files can be used. This could be useful if you have name data broken down by time, geography, or any other variable. By default, male and female first name data from 1990 are combined with last name data from 2000.

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
from censusname import Censusname

espana_nombre = Censusname(nameformat=my_format, namefiles=my_files, max_frequencies=maximums, csv_args=my_csv_args)

# Generate a name of the format 'Given Paternal y Maternal'
espana_nombre.generate()
'Luis de Góngora y Argote'

# Use a different format:
espana_nombre.generate(nameformat='{given} {paternal} de {maternal}')
'Pedro López de Ayala'

# Pick a name from the Sevilla files:
espana_nombre.generate(maternal='sevilla', paternal='sevilla')

# Pick a female name from the Toledo files:
# Note that any of the keys in my_files can be used as keyword arguments. The values should be keys from the respective dictionary.
espana_nombre.generate(given='female', maternal='toledo', paternal='toledo')

# By default, names are capitalized (title case).
# Generate a name using given capitalization in the files:
espana_nombre.generate(capitalize=False)

# By default, there's an equal probability of producing a name with a part from the Sevilla or Toledo lists.
# You have to do a little extra to weight that probability.
# Specify an 75% chance of a sevilla name, 25% chance of a toledo name:
province = random.choice(['sevilla'] * 3 + ['toledo'])
espana_nombre.generate(paternal=province, maternal=province)
````

### Example: Middle Names

Use the built-in data to fake middle names by randomly picking either a first or last name:

````python
import censusname

namefiles = censusname.NAMEFILES

# Add a middle name entry to the name files
namefiles['middle'] = {
	'last': censusname.SURNAME2000,
	'female': censusname.FEMALEFIRST1990,
	'male': censusname.MALEFIRST1990
}

middlenames = censusname.Censusname(namefiles, censusname.MAX_FREQUENCIES, '{given} {middle} {surname}')

# Generate a name in the format "given, middle, surname"
# However, this might return unlikely names
middlenames.generate()
'John Mary Smith'

# Generated name will have a male first name and either a male given name or a surname as a middle name
middlenames.generate(given='male', middle=['male', 'last'])
'Charles Michael Brescia'

# Generated name will have a female first name and either a female given name or a surname as a middle name
middlenames.generate(given='female', middle=['female', 'last'])
'Mildred Hoang Hutton'
````

#### Formatters

You can specify arbitary reformatting methods that are run on each part of the name before they are returned. By default, the package includes a surname formatter that tries to intelligently format raw names like OHALLORAN (to O'Halloran).

You can specify formatters with a dict that targets each part of a name. The formatters should be a list of methods.

````python

my_formatters = {
	'given': [lambda x: x[::-1]], # reverse a string
	'surname': [lambda x: "De " + x],
}

cn = Censusname(formatters=my_formatters)
cn.generate()
'ekiM De Morgan'
````

Additional formatters can be added to `Censusname.generate`, they will be run in addition to any formatters included in the object.

````python
more_formatters = {
	'given': [lambda x: x.replace('a', 'b')]
}

cn.generate(formatters=more_formatters)
'nbhtbN De Scardino'
````

Note that passing a formatters argument to `censusname` will exclude the default surname formatter. It's easy enough to keep it, though:

````python
import censusname

my_formatters = {
	'surname': [censusname.formatters.recapitalize_surnames, custom_fuction]	
}
````