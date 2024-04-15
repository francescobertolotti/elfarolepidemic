# import libraries
import random

def go(par, gv, al, pm):
    
    gv.t += 1
    gv.t_history.append(gv.t)

    random.shuffle(gv.present_agents)

    # 1 - initialize global variables
    gv.initialize_gv()



    # 2 - calculating how many agents are going to the bar
    for person in al.persons_list: person.getContagiousLevel(par, gv, gv.t)
    for person in al.persons_list: person.decisionAttendingBar(gv, par) 

    
    # 3 - Updating strategy of the present agents
    gv.update_present_agents_strategy(par)
    for person in gv.present_agents: person.updateLastStrategy(gv)
    

    random.shuffle(gv.present_agents)

    
    
    # 4 - Agents get infected
    person.infection_dynamics(gv, par, al)

    # 5 - Update output
    gv.compute_globals(al, par)
    gv.calculate_value(par)

    if par.enablePM:
        pm.operationForDay(par, gv)



