#!/usr/bin/env python3

#
# Analyses a hierarchical tab-indented list file and prints out subsection sizes on a requested nesting level
# Subsections with the same name in different subtrees are treated as continutaions of a single section
# The script accepts two command line parameters - file name and indentation level
#

import sys

def get_headings(filename, indentation_level):
	diff = 0
	heading = ''
	headings = {}

	try:
		with open(filename, 'r') as fh:
			for line in fh:
				line = line.rstrip()

				if len(line) == 0:
					continue

				# Include commented out lines
				if line[0] == '#':
					line = line[1:].rstrip()

					if len(line) == 0:
						continue

				if line == "==========EndOfList==========":
					break

				count = 0

				for c in line:
					if c == '\t':
						count += 1
					else:
						break

				line = line.lstrip()

				if count <= indentation_level:
					if len(heading) > 0:
						headings[heading] = headings.get(heading, 0) + diff - 1

					diff = 0

					if count == indentation_level:
						heading = line[:]

				diff += 1
	except EnvironmentError as err:
		print(err)

	if len(heading) > 0:
		headings[heading] = headings.get(heading, 0) + diff - 1

	return headings

def main():
	if len(sys.argv) < 2:
		print("usage: {0} <filename> <nesting level>".format(sys.argv[0]))
		sys.exit(1)

	if len(sys.argv) < 3:
		level = 0
	else:
		level = int(sys.argv[2])

		if level < 0:
			level = 0

	try:
		headings = get_headings(sys.argv[1], level)
	except FileNotFoundError:
		print("Error: unable to process file {0}".format(sys.argv[1]))
		sys.exit(1)

	for heading in sorted(headings, key = headings.get, reverse = True):
		if headings[heading] > 0:
			print('{0}{1}'.format(heading.ljust(50, ' '), headings[heading]))

if __name__ == '__main__':
    main()
