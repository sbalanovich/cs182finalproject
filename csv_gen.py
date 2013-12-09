# Run this file to generate the large test file that can be used for testing.
# Might have to run "sudo pip install names" before being able to run this.

import csv
import names
import random

NUM_WORKERS = 10
NUM_TASKS = 4

skillList = ["Computer", "Sorting", "Counting", "Making Coffee"]

with open("workers.csv", "wb") as workersFile:
	writer = csv.writer(workersFile)
	firstrow = ["Name"]
	firstrow.extend(skillList)
	firstrow.append("Number of tasks")

	writer.writerow(firstrow)

	for e in xrange(NUM_WORKERS):
		row = []
		name = names.get_full_name()
		row.append(name)
		for i in xrange(4):
			row.append(random.choice(["T","F"]))
		num_tasks = int(random.random() * NUM_TASKS / 10 + 1)
		row.append(num_tasks)
		writer.writerow(row)

with open("tasks.csv", "wb") as tasksFile:
	writer = csv.writer(tasksFile)
	firstrow = ["Task"]
	firstrow.extend(skillList)
	firstrow.append("Number of workers")

	writer.writerow(firstrow)

	for task in xrange(NUM_TASKS):
		row = []
		row.append(task)
		for i in xrange(4):
			row.append(random.choice(["T","F"]))
		num_workers = int(random.random() * NUM_WORKERS / 5 + 1)
		row.append(num_workers)
		writer.writerow(row)