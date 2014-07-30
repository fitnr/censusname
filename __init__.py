from os.path import abspath, join, dirname
import random
import csv

__title__ = 'random_names'
__version__ = '0.1'
__author__ = 'Neil Freeman'
__license__ = 'MIT'

full_path = lambda filename: abspath(join(dirname(__file__), filename))

# Name files should have at least the following columns:
# name (string)
# cumul_frequency (float) number from 0 to 100
SURNAME2000 = full_path("data/dist.all.last.2000.csv")
SURNAME1990 = full_path("data/dist.all.last.1990.csv")
MALEFIRST1990 = full_path("data/dist.male.first.1990.csv")
FEMALEFIRST1990 = full_path("data/dist.female.first.1990.csv")

# Name files don't contain every name, so hard coding the maximum frequency here.
# This way we don't over-pick the least common names
MAX_FREQUENCIES = {
    SURNAME2000: 89.75356,
    SURNAME1990: 90.483,
    MALEFIRST1990: 90.040,
    FEMALEFIRST1990: 90.024
}

GIVENNAMEFILES = {
    'male': MALEFIRST1990,
    'female': FEMALEFIRST1990
}

# 1990 is commented out because it's (a) out of date (b) not based on a random sample anyway
# Feel free to use it by doing something like:
# import random_names
# my_surnamefiles = { 1990: random_names.SURNAME1990 }
SURNAMEFILES = {
    2000: SURNAME2000,
    # 1990: SURNAME1990
}

NAMEFILES = {
    'given': GIVENNAMEFILES,
    'surname': SURNAMEFILES
}


class random_name(object):

    """Generate a random name from an arbitary set of files"""

    def __init__(self, namefiles=None, max_frequencies=None, nameformat='{given} {surname}', **kwargs):
        self.namefiles = namefiles or NAMEFILES

        if self.namefiles == NAMEFILES:
            self.max_frequencies = MAX_FREQUENCIES

        # If no max frequencies given, assume they go to 100 for each file
        if max_frequencies is None:
            max_frequencies = dict((self.namefiles[k][x], 100) for k in self.namefiles.keys() for x in self.namefiles[k])

        self.nameformat = nameformat

        if 'csv_args' in kwargs:
            self.csv_args = kwargs['csv_args']
        else:
            self.csv_args = {'delimiter': ','}

    def generate(self, nameformat=None, capitalize=True, **kwargs):
        '''Pick a random name form a specified list of name parts'''
        if nameformat is None:
            nameformat = self.nameformat

        lines = self._get_lines(kwargs)
        names = dict((k, v['name']) for k, v in lines.items())

        if capitalize:
            names = dict((k, n.capitalize()) for k, n in names.items())

        return nameformat.format(**names)

    def _get_lines(self, nametypes):
        datafile, frequency, lines = '', 0.0, {}

        for namepart in self.namefiles.keys():
            datafile = self._pick_file(namepart, nametypes.get(namepart, None))
            frequency = random.uniform(0, self.max_frequencies[datafile])
            lines[namepart] = self.pick_frequency_line(datafile, frequency)

        return lines

    def _pick_file(self, namepart, namekeys=None):
        result = None

        if type(namekeys) == str:
            namekeys = [namekeys]

        if namekeys:
            key = random.choice(namekeys)
            result = self.namefiles[namepart].get(key)

        if result is None:
            return random.choice(self.namefiles[namepart].values())
        else:
            return result

    def pick_frequency_line(self, datafile, frequency, cumulativefield='cumulative_frequency'):
        '''Given a frequency, pick a line from a csv with a cumulative frequency field'''
        with open(datafile, 'r') as f:
            reader = csv.DictReader(f, **self.csv_args)

            for line in reader:
                if float(line[cumulativefield]) >= frequency:
                    return line

if __name__ == '__main__':
    # In the absence of tests, as least make sure specifying arguments doesn't break anything:
    rn = random_name(NAMEFILES, MAX_FREQUENCIES, '{given} {surname}', csv_args={'delimiter': ','})
    print rn.generate()
