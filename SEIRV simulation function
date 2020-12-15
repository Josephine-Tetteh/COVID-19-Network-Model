def simfxn(Time,popul):
    bound1 = 0.025
    bound2 = 0.001
    rate1 = 0.09
    rate2 = 0.04
    midpoint1 = 50
    midpoint2 = 126
    beta = double_smoothlog(Time, bound1 , bound2, rate1 , rate2 , midpoint1 , midpoint2)  # calculate beta(t)
    
    color_dict = {"S": "blue", "I": "red", "R": "green", "V":"orange"}
    g=ig.Graph.Erdos_Renyi(popul, m=5*popul)  # generate ER network
    pop = popul
    g.vs["state"] = "S"
    g.vs["duration"] = 0
  
    perc_vac = int(40*pop) # randomly select % of the population to be vaccinated. This is 0 for no vaccination scenario 
    vac_eff = 40  # vaccine efficacy  # This is 0 for no vaccination scenario 
    init_vac_grp = random.sample(list(range(pop)), perc_vac)  # initial vaccinated nodes prior to infection
    g.vs[init_vac_grp]["state"] = "V"

    #randomly select an infected node to start epidemic
    i = rd.randint(0, pop-1)
    if g.vs[i]["state"] != 'V':   # if initial node is not vaccinated, then set it as exposed
        g.vs[i]["state"] = "E"
    nb_S = [pop-perc_vac]
    nb_E = [1]
    nb_I = [0]
    nb_R = [0]
    nb_V = [len(init_vac_grp)]
    exposed_vac = []
    Time = Time 
    count = 0 
    for time in range(Time): #no. of days     
        for n in g.vs.select(state_eq = "E"): #iterates through each exposed node
            g.vs[n.index]["duration"] += 1 
            if g.vs[n.index]["duration"] in range(7,17):  # if exposure duration is reached, the node's state is infected I
                g.vs[n.index]["state"] = 'I'
                count = count + 1
            for nb in g.neighbors(n): #iterates through neighbours of the node n
                if g.vs[nb]["state"] == "S": #if node is susceptible conduct binomial trial
                    s=np.random.binomial(1, beta[time],1)
                    if s == 1:
                        g.vs[nb]["state"] = "E" 
                if g.vs[nb]["state"] == "V": #if node is vaccinated conduct binomial trial
                    u=np.random.binomial(1, (1-vac_eff)*beta[time],1)
                    if u == 1:
                        g.vs[nb]["state"] = "E" 
                        exposed_vac.append(nb)
                          
        for m in g.vs.select(state_eq = "I"): #iterates through each node in the network
            g.vs[m.index]["duration"] += 1 #from day 0 to infect_len this node continues to infect                                
            for nbm in g.neighbors(m): #iterates through neighbours of that node
                if g.vs[nbm]["state"] == "S": #if node is infected...

                    j=np.random.binomial(1, beta[time],1)
                    if j == 1:
                        g.vs[nbm]["state"] = "E"
            if g.vs[m.index]["duration"] in range(17,Time):
                g.vs[m.index]["state"] = 'R'
                
        nb_S.append(len(g.vs.select(state_eq = "S"))) #no. of susceptibles in population
        nb_E.append(len(g.vs.select(state_eq = "E"))) #no. of recovereds in population
        nb_I.append(len(g.vs.select(state_eq = "I"))) #no. of infecteds in population
        nb_R.append(len(g.vs.select(state_eq = "R"))) #no. of recovereds in population
        nb_V.append(len(g.vs.select(state_eq = "V"))) #no. of recovereds in population

    return(nb_S,nb_E,nb_I,nb_R,nb_V,count)

