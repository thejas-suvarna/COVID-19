import parameters
from parameters import map
from person import Person
from state import State
from status import Status
import csv
import numpy as np

people = []


def main():
    # define_map()
    setup() #put x number of people in each state

    export_info(0)

    for i in range(parameters.numDays):
        infect() #depending on probability, connect/infect
        export_info(i+1)


def setup():
    for state_name, state in parameters.map.items():
        for i in range(state.Population):
            person = Person(state_name)
            state.people.append(len(people))
            people.append(person)
    print("State", "Susceptible", "Asymptomatic_Inf", "Symptomatic_Inf", "Recovered", "Dead")



def infect():
    for state_name, state in map.items():
        catch = np.random.binomial(1, parameters.probCatch, size=len(state.people))
        for p, i in zip(catch, state.people):
            if people[i].becomes_infected(p):
                people[i].get_infected()
                state.changeStatus(Status.Susceptible, people[i].status)
            else:
                old_status = people[i].status
                changed = people[i].proceed_time()
                if changed:
                    state.changeStatus(old_status, people[i].status)
        for p, i in zip(catch, state.people):
            people[i].update()

def export_info(i):
    for state_name, state in map.items():
        print(i, state_name, state)
        # state.print_info()


main()