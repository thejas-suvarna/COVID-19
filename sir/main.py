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
    mainwriter.writerow(["time", "State", "Susceptible", "Asymptomatic_Inf", "Symptomatic_Inf", "Recovered", "Dead"])
    # define_map()
    setup() #put x number of people in each state



    export_info(0, mainwriter)

    for i in range(parameters.numDays):
        infect() #depending on probability, connect/infect
        export_info(i+1, mainwriter)

    close()


def setup():
    for state_name, state in parameters.map.items():
        for i in range(state.Population):
            person = Person(state_name)
            state.people.append(person)
            # people.append(person)




def infect():
    for state_name, state in map.items():
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
        array.insert(0, state_name)
        array.insert(0, i)
        file.writerow(array)

        print(i, state_name, state)
        # state.print_info()

def close():
    with open('people.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter="\t")
        for state_name, state in map.items():
            for person in state.people:
                # print(person.export())
                spamwriter.writerow(person.export())



main()