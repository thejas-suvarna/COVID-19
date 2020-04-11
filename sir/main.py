import parameters
from parameters import map
from person import Person
from state import State
from status import Status
import csv
import numpy as np
import pickle

people = []


def main():
    file1 = open('data.csv', 'w', newline='')
    mainwriter = csv.writer(file1, delimiter="\t")
    mainwriter.writerow(["time", "Susceptible", "Asymptomatic_Inf", "Symptomatic_Inf", "Total_Inf", "Recovered", "Dead"])

    people_file = open('people.csv', 'w', newline='')
    peoplewriter = csv.writer(people_file, delimiter="\t")
    peoplewriter.writerow(["status", "state", "risk", "environment", "behavior"])
    # define_map()
    setup() #put x number of people in each state



    export_info(0, mainwriter)

    for i in range(parameters.numDays):
        infect() #depending on probability, connect/infect
        export_info(i+1, mainwriter)

    mainwriter.writerow([])
    mainwriter.writerow(["status", "state", "risk", "environment", "behavior"])

    close(mainwriter)


def setup():
    for state_name, state in parameters.map.items():
        for i in range(state.Population):
            person = Person(state_name)
            state.people.append(person)
            # people.append(person)




def infect():
    for state_name, state in map.items():
        if state.Asymptomatic_Inf == 0 and state.Symptomatic_Inf == 0 and state.Dead > 0:
            break
        catch = np.random.binomial(1, parameters.probCatch, size=len(state.people))
        for p, person in zip(catch, state.people):
            if person.becomes_infected(p):
                person.get_infected()
                state.changeStatus(Status.Susceptible, person.status)
            else:
                old_status = person.status
                changed = person.proceed_time()
                if changed:
                    state.changeStatus(old_status, person.status)
            person.update()


def export_info(i, file):
    for state_name, state in map.items():
        array = state.export()
        array.insert(0, i)
        file.writerow(array)

        print(i, state)
        # state.print_info()

def close(writer):
        for state_name, state in map.items():
            for person in state.people:
                # print(person.export())
                writer.writerow(person.export())



main()