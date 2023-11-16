# import libraries
from model.person import *

def setup(par, gv, al):

    # Building agents objects
    for i in range(1, par.n_persons + 1): # This generates the agents needed for the simulation
        new_person = Person(par)
        new_person.who = i
        
        if i <= (par.n_persons * par.strategyOne):
            new_person.strategyType = 1
        if i > (par.n_persons * (1 - par.strategyTwo)):
            new_person.strategyType = 2
        if (i) <= par.num_infected_persons: 
            new_person.initiateContagius(par, gv)
        al.persons_list.append(new_person)

        






