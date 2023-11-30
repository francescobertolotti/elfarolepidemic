# import libraries
from model.person import *

def setup(par, gv, al):
    # Building agents objects
    for i in range(1, par.n_persons + 1): # This generates the agents needed for the simulation
        new_person = Person(par)
        new_person.who = i
        
        # Strategy type
        if i <= (par.n_persons * par.strategyOne):
            new_person.strategyType = 1
        if i > (par.n_persons * (1 - par.strategyTwo)):
            new_person.strategyType = 2
        

        # Mask for PM type
        if i <= (par.n_persons * par.a2_faceMask1Agents):
            new_person.facemaskType = 1
        if i > (par.n_persons * par.a2_faceMask1Agents) and i <= (par.n_persons * (1 - par.a2_faceMask0Agents)):
            new_person.facemaskType = 2
        if i > (par.n_persons * (1 - par.a2_faceMask0Agents)):
            new_person.facemaskType = 0
            


        # Infected
        if (i) <= par.num_infected_persons: 
            new_person.initiateContagius(par, gv)


        al.persons_list.append(new_person)
    

        

