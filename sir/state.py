from status import Status

class State:
    def __init__(self, Population):
        self.Susceptible = Population
        self.Asymptomatic_Inf = 0
        self.Symptomatic_Inf = 0
        self.Recovered = 0
        self.Dead = 0
        self.Population = Population - self.Dead
        self.people = []
        self.unimportant = []

    def __str__(self):
        return "{} {} {} {} {}".format(self.Susceptible, self.Asymptomatic_Inf, self.Symptomatic_Inf, self.Recovered, self.Dead)

    def export(self):
        return [self.Susceptible, self.Asymptomatic_Inf, self.Symptomatic_Inf, self.Recovered, self.Dead]
    # def defined_init(self, Population, Recovered, Dead, Symptomatic_Inf, Asymptomatic_Inf):
    #     self.Asymptomatic_Inf = Asymptomatic_Inf
    #     self.Symptomatic_Inf = Symptomatic_Inf
    #     self.Recovered = Recovered
    #     self.Dead = Dead
    #     self.Population = Population - Dead
    #     self.Susceptible = Population - Asymptomatic_Inf - Symptomatic_Inf - Recovered
    #     self.people = []

    def print_info(self):
        print(self.Susceptible, self.Asymptomatic_Inf, self.Symptomatic_Inf, self.Recovered, self.Dead)

    def Susc_update(self, i):
        self.Susceptible = self.Susceptible + i

    def Asymp_update(self, i):
        self.Asymptomatic_Inf = self.Asymptomatic_Inf + i

    def Symp_update(self, i):
        self.Symptomatic_Inf = self.Symptomatic_Inf + i

    def changeStatus(self, oldStatus, newStatus):
        if oldStatus == Status.Susceptible:
            self.Susc_update(-1)
        elif oldStatus == Status.Asymptomatic_Inf:
            self.Asymp_update(-1)
        elif oldStatus == Status.Symptomatic_Inf:
            self.Symp_update(-1)
        else:
            print("Invalid Old Status")

        if newStatus == Status.Recovered:
            self.Recovered = self.Recovered + 1
        elif newStatus == Status.Asymptomatic_Inf:
            self.Asymp_update(+1)
        elif newStatus == Status.Symptomatic_Inf:
            self.Symp_update(+1)
        elif newStatus == Status.Dead:
            self.Dead = self.Dead + 1
            self.Population = self.Population - 1
        else:
            print("Invalid New Status")

        # switcher_new = {
        #     Status.Recovered: lambda: (self.Recovered := self.Recovered + 1),
        #     Status.Asymptomatic_Inf: lambda: (self.Asymptomatic_Inf := self.Asymptomatic_Inf + 1) ,
        #     Status.Symptomatic_Inf: lambda: (self.Symptomatic_Inf := self.Symptomatic_Inf + 1),
        #     Status.Dead: lambda: [
        #                             self.Dead := self.Dead + 1,
        #                             self.Population := self.Population + 1]
        # }
        #
        # with switch(newStatus) as case, default:
        #     @case(Status.Asymptomatic_Inf)
        #     def _():
        #         self.Asymptomatic_Inf += 1
        #
        #     @case(Status.Symptomatic_Inf)
        #     def _():
        #         self.Symptomatic_Inf += 1
        #
        #     @case(Status.Recovered)
        #     def _():
        #         self.Recovered += 1
        #
        #     @case(Status.Dead)
        #     def _():
        #         self.Dead += 1
        #         self.Population += -1
        #
        #     @default
        #     def _():
        #         print("Invalid New Status!")


