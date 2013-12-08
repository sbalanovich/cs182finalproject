# Run this file to generate the large test file that can be used for testing.
# Might have to run "sudo pip install names" before being able to run this.

import csv
import names
import random

skillList = ["Computer", "Sorting", "Counting", "Making Coffee"]

with open("workers.csv", "wb") as workersFile:
	writer = csv.writer(workersFile)
	firstrow = ["Name"]
	firstrow.extend(skillList)

	writer.writerow(firstrow)

	for e in xrange(100):
		row = []
		name = names.get_full_name()
		row.append(name)
		for i in xrange(4):
			row.append(random.choice(["T","F"]))
		writer.writerow(row)

with open("tasks.csv", "wb") as tasksFile:
	writer = csv.writer(tasksFile)
	firstrow = ["Task"]
	firstrow.extend(skillList)

	writer.writerow(firstrow)

	for task in xrange(20):
		row = []
		row.append(task)
		for i in xrange(4):
			row.append(random.choice(["T","F"]))
		writer.writerow(row)