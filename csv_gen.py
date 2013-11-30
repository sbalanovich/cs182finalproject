# Run this file to generate the large test file that can be used for testing.
# Might have to run "sudo pip install names" before being able to run this.

import csv
import names
import random

output = open("test.csv", "wb")
writer = csv.writer(output)

writer.writerow(["Name", "Computer", "Sorting", "Counting", "Making Coffee"])

for e in xrange(100):
	row = []
	name = names.get_full_name()
	row.append(name)
	for i in xrange(4):
		row.append(random.choice(["T","F"]))
	writer.writerow(row)
output.close()