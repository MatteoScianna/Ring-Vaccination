from scipy.stats import *
import networkx as nx
import numpy as np

########### create probability distributions ###########
def prob_list_poisson(lambda1,n):
    prob_vec = []
    k = 0
    while k<n:
        prob_vec.append((poisson.pmf(k,lambda1)))
        k+=1
    prob_vec = [i/sum(prob_vec) for i in prob_vec]
    return prob_vec

def prob_list_powerlaw(a,min,n):
    prob_vec = [0]*min
    for k in range(min,int(np.sqrt(n))):
        prob_vec.append(k**(-a))
    prob_vec = [i/sum(prob_vec) for i in prob_vec]
    return prob_vec

### get degree lists

def discrete_inverse_trans(prob_vec):
    U=uniform.rvs(size=1)
    if U<=prob_vec[0]:
        return 1
    else:
        for i in range(1,len(prob_vec)+1):
            if sum(prob_vec[0:i])<U and sum(prob_vec[0:i+1])>U:
                return i

def discrete_samples(prob_vec,n):
    sample=[]
    for i in range(0,n):
        k = discrete_inverse_trans(prob_vec)
        if k == None:
            k = 1
        sample.append(k)

    for i in range(len(sample)):
        if sample[i] == None:
            print(sample[i],i)

    #check if sum is even   
    if sum(sample)%2 != 0:
        sample[0] = sample[0]+1
    return sample

##### get configuration model 

def config_model(degree_list):
    #check if sum is even
    if sum(degree_list)%2 != 0:
        degree_list[0] = degree_list[0]+1
    graph = nx.configuration_model(degree_list)
    graph1= graph.copy()
    for (u,v) in graph1.edges():
        if u == v:
            graph.remove_edge(u,v)
    #remove parallel edges
    graph = nx.Graph(graph)
    return graph

def g_1(x,prob_list,mean_degree):
    sol = 0
    for i in range(0,len(prob_list)-1):
        if prob_list[i] == 0:
            continue
        else:
            sol += ((i+1)*prob_list[i+1]*x**i)/mean_degree
    return sol

def g_0(x,prob_list):
    sol = 0
    for i in range(len(prob_list)-1):
        sol += (prob_list[i]*(x**(i)))
    return sol

###########################

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:.2f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()