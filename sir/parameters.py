from state import State
# probMeetImmune
# probMeetAsymptomatic
# probMeetSymptomatic
#
# probability meet someone immune or asymptomatic
# probability meat someone symptomatic
# These should also vary by location and type.because we want locations to represent cities or rural areas and types to by how much people sequester.
#
# probCatch
# timeAsymptomatic
# timeSymptomatic

probCatch = 0.3
timeAsymptomatic = 14
timeSymptomatic = 10

symptomDeathRate = 0.015
percentSymptomatic = 0.4

numDays = 100

behaviorLow = 5
percentageHigh = 0



map = {
    "MI": State(80000),
}