# import libraries
from model.person import *

def setup(par, gv, al):

    # Building agents objects
    for i in range(par.n_persons): # This generates the agents needed for the simulation
        new_person = Person()
        new_person.who = i + 1
        if (i + 1) <= par.num_infected_persons: 
            new_person.initiateContagius(par, gv)
        al.persons_list.append(new_person)

        






