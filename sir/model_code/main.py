import parameters
from parameters import map
from person import Person
from state import State
from status import Status
import csv
import numpy as np
import pickle
import pandas as pd


# This file is used to run two scenarios. The first is used to run sensitivity on low risk individual behavior. The file is currently configured to run that case.
# The second case is to run sensitivty on population that is High Risk. To run that:
# Uncomment lines: 31, 39
# Comment lines: 30, 38 


def main():
    file1 = open('data.csv', 'w', newline='')
    mainwriter = csv.writer(file1, delimiter="\t")
    mainwriter.writerow(["time", "LowBehavior", "Susceptible", "Asymptomatic_Inf", "Symptomatic_Inf", "Total_Inf", "Recovered", "Dead"])

    people_file = open('people.csv', 'w', newline='')
    peoplewriter = csv.writer(people_file, delimiter="\t")
    peoplewriter.writerow(["status", "state", "risk", "environment", "behavior"])
    # define_map()
    setup() #put x number of people in each state

    behaviorList = [5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10]
    # percentageList = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

    stateData = pd.DataFrame()
    peopleData = pd.DataFrame()

    for behavior in percentageList:
        print(behavior)
        parameters.behaviorLow = behavior
        # parameters.percentageHigh = behavior

    
        #set column names
        stateNames = ["time", "LowBehavior", "Susceptible", "Asymptomatic_Inf", "Symptomatic_Inf", "Total_Inf", "Recovered", "Dead"]
        for i, name in enumerate(stateNames):
            stateNames[i] = str(behavior) + "-" + name

        peopleNames = ["status", "state", "risk", "environment", "behavior"]
        for i, name in enumerate(peopleNames):
            peopleNames[i] = str(behavior) + "-" + name


        stateDatatemp = pd.DataFrame()
        peopleDatatemp = pd.DataFrame()

        stateDatatemp = export_info(0, mainwriter, stateDatatemp)

        # Run the model 
        for i in range(parameters.numDays):
            infect() #depending on probability, connect/infect
            stateDatatemp = export_info(i+1, mainwriter, stateDatatemp)

        #Write data to the dataframe
        stateDatatemp.columns = stateNames[1:]

        mainwriter.writerow([])
        mainwriter.writerow(["status", "state", "risk", "environment", "behavior"])

        peopleDatatemp = close(mainwriter, peopleDatatemp)
        peopleDatatemp.columns = peopleNames

        stateData = pd.concat([stateData, stateDatatemp], axis=1)
        peopleData = pd.concat([peopleData, peopleDatatemp], axis=1)

        #re-initialize each state
        reset()

    stateData.to_csv('statedata.csv')
    peopleData.to_csv('peopledata.csv')


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


def reset():
    for state_name, state in parameters.map.items():
        state.Population = len(state.people)
        state.people = []
        state.Asymptomatic_Inf = 0
        state.Symptomatic_Inf = 0
        state.Recovered = 0
        state.Dead = 0
        state.Susceptible = state.Population
        for i in range(state.Population):
            person = Person(state_name)
            state.people.append(person)


def export_info(i, file, infoarray):
    for state_name, state in map.items():
        array = state.export()
        array.insert(0, parameters.behaviorLow)
        array.insert(0, i)

        file.writerow(array)

        infoarray = pd.concat([infoarray, pd.DataFrame([array[1:]]) ], ignore_index=True)

        print(i, state)
        return infoarray
        # state.print_info()
    

def close(writer, dataframe):
    for state_name, state in map.items():
        for person in state.people:
            # print(person.export())
            writer.writerow(person.export())
            dataframe = pd.concat([dataframe, pd.DataFrame([person.export()]) ], ignore_index=True)
    return dataframe


main()