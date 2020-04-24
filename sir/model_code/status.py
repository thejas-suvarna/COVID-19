from enum import Enum


class Status(Enum):
    Susceptible = 1
    Asymptomatic_Inf = 2
    Symptomatic_Inf = 3
    Recovered = 4
    Dead = 5
