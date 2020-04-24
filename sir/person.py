from parameters import map
import parameters
from status import Status
from state import State
from enum import Enum
import numpy as np

class Person:
    def __init__(self, state):
        self.status = Status.Susceptible
        self.state = state
        # self.risk = .15 if np.random.binomial(1, 0.1) == 1 else 0.0001
        self.risk = .10 if np.random.binomial(1, parameters.percentageHigh) == 1 else self.risk_value(parameters.percentageHigh)
        # self.risk = 0.015
        self.environment = np.random.normal(5, 1.0)
        # self.behavior = np.random.normal(parameters.behaviorLow, 1.0) if self.risk == 0.0001 else np.random.normal(2 , 1.0)
        self.behavior = np.random.normal(2, 1.0) if self.risk == 0.1 else np.random.normal(parameters.behaviorLow , 1.0)
        # self.behavior = np.random.normal(5, 1.0)
        self.exposure_multiplier = (self.scale(self.environment) * self.scale(self.behavior))#/(self.scale(self.environment) #+ self.scale(self.behavior)/2)
        self.probMeetImmune = self.calc_prob_meet_Immune()
        self.probMeetAsymptomatic = self.calc_prob_meet_Asymptomatic()
        self.probMeetSymptomatic = self.calc_prob_meet_Symptomatic()
        self.daysLeft = 0

    def __str__(self):
        return "{} {} {} {}".format(self.status, self.state, self.environment,
                                       self.behavior)

    def export(self):
        return [self.status, self.state, self.risk, self.environment, self.behavior]


    def scale(self, var):
        return (var/5)

    def risk_value(self, percentage):
        x = (0.015 - (0.1 * percentage)) / (1 - percentage)
        return 0.000001 if x < 0 else x

    def calc_prob_meet_Immune(self):
        return ((map[self.state].Recovered / map[self.state].Population) * self.exposure_multiplier)

    def calc_prob_meet_Asymptomatic(self):
        return ((map[self.state].Asymptomatic_Inf / map[self.state].Population) * self.exposure_multiplier)

    def calc_prob_meet_Symptomatic(self):
        return ((map[self.state].Symptomatic_Inf / map[self.state].Population) * self.exposure_multiplier)

    def becomes_infected(self, catch):
        prob_meet = 0.1 if not self.probMeetSymptomatic and not self.probMeetAsymptomatic and not self.probMeetImmune else self.probMeetAsymptomatic + self.probMeetSymptomatic
        prob_meet = 1 if prob_meet > 1 else prob_meet
        prob_meet = 0 if prob_meet < 0 else prob_meet
        get_infected = np.random.binomial(1, catch*prob_meet)
        return get_infected and self.status == Status.Susceptible


    ##NEED TO INSERT FUNCTION FOR DECIDING WHETHER ASYMPTOMATIC OR NOT
    def get_infected(self):
        shows_symptoms = np.random.binomial(1, parameters.percentSymptomatic)
        self.status = Status.Symptomatic_Inf if shows_symptoms else Status.Asymptomatic_Inf
        self.daysLeft = parameters.timeSymptomatic if shows_symptoms else parameters.timeAsymptomatic

    def proceed_time(self):
        if(self.status == Status.Symptomatic_Inf or self.status == Status.Asymptomatic_Inf):
            self.daysLeft = self.daysLeft - np.random.normal(1,1)
            if(self.daysLeft < 0 and self.status == Status.Symptomatic_Inf):
                dead = np.random.binomial(1, self.risk)
                # dead = np.random.binomial(1, parameters.symptomDeathRate)
                self.status = Status.Dead if dead else Status.Recovered
                return True
            elif(self.daysLeft < 0 and self.status == Status.Asymptomatic_Inf):
                self.status = Status.Recovered
                return True
        return False

    def update(self):
        self.probMeetImmune = self.calc_prob_meet_Immune()
        self.probMeetAsymptomatic = self.calc_prob_meet_Asymptomatic()
        self.probMeetSymptomatic = self.calc_prob_meet_Symptomatic()

    # status
    # state
    # environment
    # behavior
    #
    # probMeetImmune
    # probMeetAsymptomatic
    # probMeetSymptomatic
    #environment = scale from 0 - 10 (population density)
    #behavior = sequester level 0 - 10





