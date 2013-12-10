# Run this file to generate the large test file that can be used for testing.
# Might have to run "sudo pip install names" before being able to run this.

import csv
import names
import random
import sys

NUM_WORKERS = 30
NUM_TASKS = 10

skillList = ["Make copies", "Make GIFs", "Photoshop", "Write AI code"]

with open("workers.csv", "wb") as workersFile:
	writer = csv.writer(workersFile)
	firstrow = ["Name"]
	firstrow.extend(skillList)
	firstrow.append("Number of tasks")

	writer.writerow(firstrow)

	total = 0

	for worker in xrange(NUM_WORKERS):
		row = []
		name = names.get_full_name()
		row.append(name)
		
		# # each skill has increasing difficulty
		# for i in xrange(4):
		# 	if random.random() <= float(1) / (2**i):
		# 		row.append("T")
		# 	else:
		# 		row.append("F")
		
		# each worker is randomly assigned skills
		for i in xrange(4):
			row.append(random.choice(["T","F"]))
		
		num_tasks = int(random.random() * NUM_TASKS / 5 + 1)
		total += num_tasks
		row.append(num_tasks)
		writer.writerow(row)
	print total

with open("tasks.csv", "wb") as tasksFile:
	writer = csv.writer(tasksFile)
	firstrow = ["Task"]
	firstrow.extend(skillList)
	firstrow.append("Number of workers")

	writer.writerow(firstrow)

	total = 0
	for task in xrange(NUM_TASKS):
		row = []
		row.append(task)

		# # each skill has increasing rareness
		# for i in xrange(4):
		# 	if random.random() <= float(1) / (2**i):
		# 		row.append("T")
		# 	else:
		# 		row.append("F")

		# # each task needs one skill
		# randnum = random.choice([0,1,2,3])
		# for i in xrange(4):
		# 	if i == randnum:
		# 		row.append("T")
		# 	else:
		# 		row.append("F")

		# each task is randomly assigned skills
		for i in xrange(4):
			row.append(random.choice(["T","F"]))

		num_workers = int(random.random() * NUM_WORKERS / 4 + 1)
		total += num_workers
		row.append(num_workers)
		writer.writerow(row)
	print total