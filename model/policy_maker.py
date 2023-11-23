#import libraries

class PM:

    def __init__(self, par) -> None:
        
        # Parameters
        self.operationsArr = ["a1InitCheck"]
        
        # States
        self.a1OldCapacity = 0
        self.a1StartingWeekReduction = par.a1_reductionDuration

        # Output
        self.PM_interactionCounter = 0 # Indentifies a conunter that indicates the number of times the PM interacts with the system

    def a1Init_capacityReductionInit(self, par, gv):
        if gv.infected_attendance >= par.a1_InfectedTreshold:
            self.operationsArr.remove("a1InitCheck")
            self.PM_interactionCounter += 1
            self.a1StartingWeekReduction = gv.t
            gv.actualCapacity = par.capacity * (1 - par.a1_reductionPerc)
            self.operationsArr.append("a1EndCheck")
    
    def a1Init_capacityReductionEnd(self, par, gv):
        if gv.t > (self.a1StartingWeekReduction + par.a1_reductionDuration):
            self.a1StartingWeekReduction = gv.t
            if gv.infected_attendance < par.a1_InfectedTreshold:
                
                self.operationsArr.remove("a1EndCheck")
                self.a1StartingWeekReduction = 0
                gv.actualCapacity = par.capacity
                self.operationsArr.append("a1InitCheck")

    def operationForWeek(self, par, gv):
        if "a1InitCheck" in self.operationsArr:
            self.a1Init_capacityReductionInit(par, gv)
        if "a1EndCheck" in self.operationsArr:
            self.a1Init_capacityReductionEnd(par, gv)
