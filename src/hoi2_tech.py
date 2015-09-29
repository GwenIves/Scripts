#!/bin/env python3

#
# Generate a report of different research teams performances for all available technologies in the Paradox Interactive's game Hearts of Iron 2
# usage: tech.py <country's research teams definition csv file> <list of all technology definition files>
#

import sys

def calc_research_time(team, tech):
    length = 0

    skill, specialisations = team

    for type_val, difficulty_val, double_time_val in tech:
        base_len = 0

        if difficulty_val == 3:
            base_len = 37
        elif difficulty_val == 4:
            base_len = 40
        elif difficulty_val == 5:
            base_len = 42
        elif difficulty_val == 6:
            base_len = 44
        elif difficulty_val == 7:
            base_len = 46
        elif difficulty_val == 8:
            base_len = 47
        elif difficulty_val == 9:
            base_len = 49
        else:
            base_len = 50

        diff = skill - difficulty_val

        if diff == -7:
            base_len += 42
        elif diff == -6:
            base_len += 33
        elif diff == -5:
            base_len += 25
        elif diff == -4:
            base_len += 18
        elif diff == -3:
            base_len += 12
        elif diff == -2:
            base_len += 7
        elif diff == -1:
            base_len += 3
        elif diff == 1:
            base_len -= 3
        elif diff == 2:
            base_len -= 6
        elif diff == 3:
            base_len -= 8
        elif diff == 4:
            base_len -= 10
        elif diff == 5:
            base_len -= 12
        elif diff == 6:
            base_len -= 14

        if double_time_val == True:
            base_len *= 2

        if type_val in specialisations:
            base_len /= 2

        length += base_len

    return length

def get_teams(filename):
    teams = {}

    try:
        with open(filename, encoding="ISO8859") as fh:
            for lineno, line in enumerate(fh):
                if lineno < 1:
                    continue

                line = line.strip()

                fields = line.split(";")

                name = fields[1]
                skill = int(fields[3])

                specialisations = []

                for s in fields[6:]:
                    if len(s) > 1:
                        specialisations.append(s)

                teams[name] =(skill, specialisations)
    except EnvironmentError as err:
        print(err)

    return teams

def get_technologies(filename):
    techs = {}

    components = []
    prev_line = None
    name = None

    try:
        with open(filename, encoding="ISO8859") as fh:
            for line in fh:
                line = line.strip()

                if line == "application =":
                    if name is not None:
                        techs[name] = components
                        components = []

                    name = prev_line[2:].title()

                if line.startswith("component"):
                    type_start = line.find("type = ")
                    type_end = line.find(" ", type_start + 7)

                    difficulty_start = line.find("difficulty =")
                    difficulty_end = line.find(" ", difficulty_start + 13)

                    double_time_start = line.find("double_time =")

                    type_val = line[type_start + 7:type_end]
                    difficulty_val = int(line[difficulty_start + 13:difficulty_end])
                    double_time_val = double_time_start != -1

                    components.append((type_val, difficulty_val, double_time_val))

                prev_line = line
    except EnvironmentError as err:
        print(err)

    if name is not None:
        techs[name] = components

    return techs

def main():
    if len(sys.argv) <= 2:
        print("usage: {0} <teams definition file> <technology definition files list>".format(sys.argv[0]))
        sys.exit(1)

    teams = get_teams(sys.argv[1])

    techs = {}

    for f in sys.argv[2:]:
        techs.update(get_technologies(f))

    for tech in sorted(techs.keys()):
        print(tech)

        team_performances = []

        for team in teams.keys():
            team_performances.append((calc_research_time(teams[team], techs[tech]), team))

        team_performances.sort()

        for perf, team in team_performances:
            print(team, perf)

        print()
        print()

if __name__ == '__main__':
    try:
        main()
    except FileNotFoundError:
        print("Error: unable to process definition files")
        sys.exit(1)
