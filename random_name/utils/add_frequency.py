import csv

last2000 = "../data/dist.all.last.2000.csv"

with open('../data/new.last.2000.csv', 'w+') as out:
	with open(last2000, 'r') as inp:
		reader = csv.DictReader(inp, delimiter=',')

		fnames = reader.fieldnames + ['frequency', 'cumulative_frequency']
		writer = csv.DictWriter(out, fieldnames=fnames)
		writer.writeheader()

		for line in reader:
			line['frequency'] = '{:.5f}'.format(float(line['prop100k']) / 1000)
			line['cumulative_frequency'] = '{:.5f}'.format(float(line['cum_prop100k']) / 1000)

			writer.writerow(line)