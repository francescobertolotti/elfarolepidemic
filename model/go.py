# import libraries
from model.person import *

def go(par, gv, al):

    # 1 - initialize global variables
    gv.initialize_gv()

    # 2 - calculating how many agents are going to the bar
    for person in al.persons_list: person.decisionAttendingBar(gv, par) 

    # 3 - Updating strategy of the present agents
    gv.update_present_agents_strategy(par)
    for person in al.persons_list: person.updateLastStrategy(gv)

    # 4 - Agents get infected
    person.infection_dynamics(gv, par, al)

    # 5 - Update output
    gv.compute_globals(al, par)
        





