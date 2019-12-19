from bisect import bisect
import sys
import random

class Simulation:
    def __init__(self, runTime, startRate, finishRate, Pvec):
        self.runTime = runTime
        self.startRate = startRate
        self.finishRate = finishRate
        self.Pvec = Pvec
        self.numberInSystem = 0
        self.clock = 0.0
        self.numberOfArrival = 0

        self.arrival = random.expovariate(startRate)

        self.departs = float('inf')

        self.totalWait = 0.0
        self.totalService = 0.0

        self.dumps = 0

        self.success = 0

        self.Ti = [0 for i in range(len(Pvec))]

    def simulate(self):
        while True:
            # takes the minimum/max from all the arrivals/departures
            minArrival = self.arrival
            minDeparts = self.departs
            if minArrival > self.runTime:
                if self.numberInSystem == 0:
                    # end of simulation - prints all the data
                    self.printResults()
                    return
                minArrival = float('inf')
            eventTime = min(minArrival, minDeparts)
            self.totalWait += (eventTime - self.clock) * self.numberInSystem
            self.Ti[self.numberInSystem] += (eventTime - self.clock)
            self.clock = eventTime
            # choose if a package is coming or leaving
            if minDeparts < minArrival:
                self.departsHandle()
            else:
                self.arrivalsHandle()

    def arrivalsHandle(self):
        pGetIn = Pvec[self.numberInSystem]
        if pGetIn <= random.random():
            self.dumps += 1
        else:
            self.numberInSystem += 1
            self.numberOfArrival += 1
            if self.numberInSystem <= 1:
                next_show = random.expovariate(self.finishRate)
                self.departs = self.clock + next_show
                self.totalService += next_show
        self.arrival = self.clock + random.expovariate(self.startRate)

    def departsHandle(self):
        self.success += 1
        self.numberInSystem = self.numberInSystem - 1
        if self.numberInSystem <= 0:
            self.departs = float('inf')
        else:
            rate = self.finishRate
            nextFrame = random.expovariate(rate)
            self.departs = nextFrame + self.clock
            self.totalService = nextFrame + self.totalService

    def printResults(self):
        if self.success == 0:
            avgWaitTime = 0.0
            avgService = 0.0
        else:
            avgWaitTime = (self.totalWait - self.totalService)
            avgWaitTime /= self.success
            avgService = self.totalService / self.success

        printSTR = str(self.success) + " "

        printSTR += str(self.dumps) + " "

        printSTR += str(self.clock) + " "

        for time in self.Ti:
             printSTR += str(time) + " "

        for time in self.Ti:
             printSTR += str(time/self.clock) + " "

        printSTR += str(avgWaitTime) + " " + str(avgService) + " " 

        printSTR += str(self.numberOfArrival/self.clock) + " "

        print(printSTR)

    ##starting the simulation

if __name__ == "__main__":
    runTime = int(sys.argv[1])
    startRate = float(sys.argv[2])
    finishRate = float(sys.argv[3])
    runningIndex = 4
    # intiallizing the probability matrix from input.
    Pvec = []
    for i in range(4, len(sys.argv)):
        Pvec.append(float(sys.argv[i]))
    # start simulation after getting all the inputs
    s1 = Simulation(runTime, startRate, finishRate, Pvec)
    s1.simulate()