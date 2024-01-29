#import libraries

class PM:

    def __init__(self, par) -> None:
        
        # Parameters
        self.operationsArr = []
        if par.enableA1:
            self.operationsArr.append("a1InitCheck")
        if par.enableA2:
            self.operationsArr.append("a2InitCheck")
        if par.enableA3:
            self.operationsArr.append("a3InitCheck")
        
        # States
        self.a1OldCapacity = 0
        self.a1StartingDayReduction = par.a1_reductionDuration

        self.a2StartingDayReduction = par.a2_reductionDuration

        self.a3StartingDayReduction = par.a2_reductionDuration

        # Output
        self.PM_interactionCounter = 0 # Indentifies a conunter that indicates the number of times the PM interacts with the system

    def a1Init_capacityReductionInit(self, par, gv):
        if gv.infected_attendance >= (par.a1_InfectedTreshold * par.n_persons):
            self.operationsArr.remove("a1InitCheck")
            self.PM_interactionCounter += 1
            self.a1StartingDayReduction = gv.t
            gv.actualCapacity = par.capacity * (1 - par.a1_reductionPerc)
            self.operationsArr.append("a1EndCheck")
    
    def a1Init_capacityReductionEnd(self, par, gv):
        if gv.t > (self.a1StartingDayReduction + par.a1_reductionDuration):
            self.a1StartingDayReduction = gv.t
            if gv.infected_attendance < (par.a1_InfectedTreshold * par.n_persons):
                self.operationsArr.remove("a1EndCheck")
                self.a1StartingDayReduction = 0
                gv.actualCapacity = par.capacity
                self.operationsArr.append("a1InitCheck")
    
    def a2Init_faceMaskInit(self, par, gv):
        if gv.infected_attendance >= (par.a2_InfectedTreshold * par.n_persons):
            self.a2StartingDayReduction = gv.t
            self.operationsArr.remove("a2InitCheck")
            self.operationsArr.append("a2EndCheck")
            gv.a2_is_active = True
    
    def a2Init_faceMaskEnd(self, par, gv):
        gv.a2History_x.append(gv.t)
        gv.a2History_y.append(- (par.n_persons * 0.05))
        if gv.t > (self.a2StartingDayReduction + par.a2_reductionDuration):
            self.a2StartingDayReduction = gv.t
            if gv.infected_attendance < (par.a2_InfectedTreshold * par.n_persons):
                self.operationsArr.remove("a2EndCheck")
                self.operationsArr.append("a2InitCheck")
                gv.a2_is_active = False

    def a3Init_entranceTestInit(self, par, gv):
        if gv.infected_attendance >= (par.a3_InfectedTreshold * par.n_persons):
            self.a3StartingDayReduction = gv.t
            self.operationsArr.remove("a3InitCheck")
            self.operationsArr.append("a3EndCheck")
            gv.a3_is_active = True
    
    def a3Init_entranceTestEnd(self, par, gv):
        gv.a3History_x.append(gv.t)
        gv.a3History_y.append(- (par.n_persons * 0.1))
        if gv.t > (self.a3StartingDayReduction + par.a3_reductionDuration):
            self.a3StartingDayReduction = gv.t
            if gv.infected_attendance < (par.a3_InfectedTreshold * par.n_persons):
                self.operationsArr.remove("a3EndCheck")
                self.operationsArr.append("a3InitCheck")
                gv.a3_is_active = False


    def operationForDay(self, par, gv):
        if "a1InitCheck" in self.operationsArr:
            self.a1Init_capacityReductionInit(par, gv)
        if "a1EndCheck" in self.operationsArr:
            self.a1Init_capacityReductionEnd(par, gv)
        if "a2InitCheck" in self.operationsArr:
            self.a2Init_faceMaskInit(par, gv)
        if "a2EndCheck" in self.operationsArr:
            self.a2Init_faceMaskEnd(par, gv)
        if "a3InitCheck" in self.operationsArr:
            self.a3Init_entranceTestInit(par, gv)
        if "a3EndCheck" in self.operationsArr:
            self.a3Init_entranceTestEnd(par, gv)

        if gv.t == 1:
            print(self.operationsArr)
