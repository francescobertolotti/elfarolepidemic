#import libraries

class PM:

    def __init__(self) -> None:
        
        # Parameters
        self.operationsArr = ["a1InitCheck"]
        
        # States
        self.a1OldCapacity = 0
        self.a1StartingWeekReduction = 0

        # Output
        self.PM_interactionCounter = 0 # Indentifies a conunter that indicates the number of times the PM interacts with the system

    def a1Init_capacityReductionInit(self, par, gv):
        if gv.infected_attendance >= par.a1_InfectedTreshold:
            self.operationsArr.remove("a1InitCheck")
            self.PM_interactionCounter += 1
            self.a1StartingWeekReduction = gv.t
            self.a1OldCapacity = par.capacity
            par.capacity = par.capacity * (1 - par.a1_reductionPerc)
            self.operationsArr.append("a1EndCheck")
    
    def a1Init_capacityReductionEnd(self, par, gv):
        if gv.t > (self.a1StartingWeekReduction + par.a1_reductionDuration) and gv.infected_attendance < par.a1_InfectedTreshold:
            self.operationsArr.remove("a1EndCheck")
            self.a1StartingWeekReduction = 0
            par.capacity = self.a1OldCapacity
            self.operationsArr.append("a1InitCheck")

    def operationForWeek(self, par, gv):
        if "a1InitCheck" in self.operationsArr:
            self.a1Init_capacityReductionInit(par, gv)
        if "a1EndCheck" in self.operationsArr:
            self.a1Init_capacityReductionEnd(par, gv)
