import matplotlib.pyplot as plt #pip install matplotlib
import reactor
import chromosome
from itertools import *
import random
import math
import numpy as np

react_list = []
timePeriod : int
requirement = {}
all_state = {}
acceptable_value = [] 
chromosome_list = []
parentList = []
drowList = []
fakeName = 0


h_printFitnessList = []
h_bestChromosomeList = []
h_reactListSelectedNum = []


s_printFitnessList = []
s_selectedNeighbers = []
s_temp = 0
s_CurrentState ={}

def read_from_input1():
	file1 = open('input1.txt', 'r')
	Lines = file1.readlines()
	
	count = 0
	global react_list 
	for line in Lines:
		count += 1	
		x=line.strip().split(",")
		react=reactor.Reactor(x[0],x[1],x[2], [])
		react_list.append(react)

def read_from_input2():
    file = open('input2.txt' , 'r')
    lines = file.readlines()
    global timePeriod
    global requirement
    timePeriod = int(lines[0])
    lines.pop(0)
    count = 0
    for line in lines: 
        if(count < timePeriod):
            x=line.strip().split(",") 
            requirement[int(x[0])] = int(x[1])
        count += 1
#  create each reactor perms
def set_perm(): 
    global react_list
    global timePeriod
    for react in react_list:
        react.generate_all_permutations(timePeriod)
        print(react.permutations_list)




def all_perm():
    lenlist = []
    for react in react_list:
        print(len(react.permutations_list))
        s = ""
        
        for i  in range(len(react.permutations_list)):
            i=i+1
            s+=str(i)
        print(s)
        
        lenlist.append(s)

    print(lenlist)
    global all_state
    all_state= product(*lenlist, repeat=1)    
#    for i in list(all_state): 
#        print (i) 
    
def generate_states():
#    for i in list(all_state): 
#        print (i[1]) 
    global react_list
    global timePeriod
    global requirement
    for state in list(all_state):
        counter = 0
        state_list = []
        for i in list(state):
#            print (i)
            state_list.append(react_list[counter].permutations_list[int(i)-1])
            counter+=1
        for i in range(timePeriod):
            counter = 0
            sumMW = 0
            for item in state_list :
                if item[i] == 0:
                    sumMW += int(react_list[counter].MW)

def create_random_chromosome(chromNum):
    global react_list
    global chromosome_list
    count = 0
    while count < chromNum:
        chromosome_detail = []
        for react in react_list:
            rand = random.randint(0,len(react.permutations_list)-1)
            chromosome_detail.append(react.permutations_list[rand])
        fitness = acceptable_chromosome(chromosome_detail)
        if fitness != -1:
            count +=1
            chrom = chromosome.Chromosome(count,chromosome_detail,fitness , 0)
            chromosome_list.append(chrom)
    calc_fitness_ratio()
    

def acceptable_chromosome(chromosome):
    global react_list
    global timePeriod
    worst = 9000000
    allSeason = 0
    oneSeason = 0
    for i in range(timePeriod):
        sumMW = 0
        count = 0
        for item in chromosome:
            if item[i] == 0 :
                sumMW += int(react_list[count].MW)
            count+=1
        fitness = sumMW - requirement[i+1]
        if fitness < 0:
            return -1
        else:
            allSeason += fitness
            
            if worst > fitness:
                worst = fitness
    return worst

def calc_fitness_ratio():
    global chromosome_list
    sumFitness = 0
    for item in chromosome_list:
        sumFitness += item.fitness;
    for item in chromosome_list:
        item.fitness_ratio = round((item.fitness / sumFitness) *100, 2)

def crosover(Pc):
    global chromosome_list
    global parentList
    parentList = select_parent(chromosome_list)
    parentList = make_child(Pc , parentList , chromosome_list)

def make_child(Pc ,parentList , chromosome_list):
    readyParent = math.floor((len(parentList)*Pc) /2.)*2
    changeParentNum = 0
    tempList1 = []
    tempList2 = []
    acceptCount = 0
    fitness1 = 0
    fitness2 = 0
    while changeParentNum < readyParent and acceptCount < 10:
        acceptCount+=1
        if parentList[changeParentNum].name != parentList[changeParentNum+1].name :
            tempList1.clear()
            tempList2.clear()
            lenthChromosome = len(parentList[0].chromosome_detail)
            randNum = random.randint(1 , lenthChromosome)
            c =0
            while c < lenthChromosome:
                if lenthChromosome-c > randNum:
                    tempList1.append(parentList[changeParentNum].chromosome_detail[c])
                    tempList2.append(parentList[changeParentNum+1].chromosome_detail[c])
                else:
                    tempList1.append(parentList[changeParentNum+1].chromosome_detail[c])
                    tempList2.append(parentList[changeParentNum].chromosome_detail[c])

                c+=1
            c = 0
            fitness1 = acceptable_chromosome(tempList1)
            fitness2 = acceptable_chromosome(tempList2)
            if fitness1 != -1 and fitness2 != -1:
                parentList[changeParentNum].chromosome_detail.clear()
                parentList[changeParentNum+1].chromosome_detail.clear()
                while c < lenthChromosome:
                    parentList[changeParentNum].chromosome_detail.append(tempList1[c])
                    parentList[changeParentNum+1].chromosome_detail.append(tempList2[c])
                    c+=1
        if fitness1 != -1 and fitness2 != -1:
            changeParentNum +=2
    return parentList



def select_parent(chromosome_list):
    fitness_ratio = []
    parentNameList = []
    for item in chromosome_list:
        fitness_ratio.append(item.fitness_ratio)
    parentList= random.choices(chromosome_list, weights=fitness_ratio, k=len(chromosome_list))
    return parentList


def mutation(pm):
    cont = 0
    chromosome_broke = []
    global parentList     
    while cont<len(parentList):
        mut= random.choices((1,0), weights=(pm,1-pm), k=1)
        if mut[0] == 1 :
            for i in parentList[cont].chromosome_detail :
                chromosome_broke.append(i)
            broke_gen( parentList[cont].chromosome_detail)
        cont+=1


def broke_gen(chromosome ):
    global react_list
    situ = True
    unit = random.randint(0,len(react_list)-1)
    while situ :
        per = random.randint(0,len(react_list[unit].permutations_list)-1)
        if react_list[unit].permutations_list[per] == chromosome[unit] :
            situ = True 
        else: 
            situ = False
    chromosome.pop(unit)
    chromosome.insert(unit , react_list[unit].permutations_list[per])


def drow_all_charts():
    global h_printFitnessList
    global s_printFitnessList
    fig, (ax1, ax2 , ax3) = plt.subplots(3)
#    fig.suptitle('Vertically stacked subplots')
    ax1.set(ylabel = "Hill Climbing")
    ax2.set(ylabel = "Simulated Anealimg")
    ax3.set(ylabel = "Generation Algorithm")
    ax1.set_title(' \n')
    ax2.set_title(' \n')
    ax3.set_title(' \n\n\n\n\n\n\n')

    ax1.plot(h_printFitnessList)
    ax2.plot(s_printFitnessList)
    ax3.plot(drowList)
    plt.show()


def set_drow_list(inputList):
    global drowList
    global fakeName
    c = 0
    for  item in inputList:
        fakeName+=1
        item.name = fakeName
        fitness = acceptable_chromosome(item.chromosome_detail)
        # if fitness > item.fitness:
        item.fitness = fitness
    for item in inputList:
        drowList.append(item.fitness)



def get_input():
    read_from_input1()
    read_from_input2()
    set_perm()



def main():
    get_input()

    N = 20
    Pc = 0.4
    Pm = 0.1
    generationAlgorithm(N , Pc , Pm )
    
    hill_climbing()

    temp = 0.9
    simulated_annealing(temp)
    drow_all_charts()


def generationAlgorithm(N , Pc , Pm ):
    # all_perm()
    # generate_states()
    create_random_chromosome(N)
    set_drow_list(chromosome_list)
    c = 0
    while c < 10 :
        crosover(Pc)
#        mutation(Pm)
        set_drow_list(parentList)
        c+=1


def simulated_annealing(temp):
    global h_reactListSelectedNum 
    global react_list
    global s_selectedNeighbers
    global s_CurrentState
    global s_printFitnessList
    global s_temp
    s_temp = temp
    s_CurrentState = h_create_random_chromosome()
    s_printFitnessList.append(s_CurrentState.fitness) 
    while s_temp > 0.00001:
        s_findNeighborhood(s_CurrentState , h_reactListSelectedNum , react_list)
        s_selectNeighborhood(s_selectedNeighbers)
        s_printFitnessList.append(s_CurrentState.fitness) 


def s_selectNeighborhood(s_selectedNeighbers):
    global s_CurrentState
    global s_temp
    boltzman = 0
    rand = random.randint(0,len(s_selectedNeighbers)-1)
    selected = s_selectedNeighbers[rand]
    if selected.fitness > s_CurrentState.fitness :
        s_CurrentState = selected
    else:
        boltzman = s_calcBoltzman(int(selected.fitness))
        randNum = random.randint(0,100)/100
        if randNum < boltzman:
            s_CurrentState = selected
        else :
            s_selectedNeighbers.pop(rand)
            s_selectNeighborhood(s_selectedNeighbers)
    s_temp *= 0.9



def s_calcBoltzman(selectedChromosomeFitness):
    global s_CurrentState
    global s_temp
    result = -((abs(s_CurrentState.fitness- selectedChromosomeFitness))/s_temp)
    return math.exp(result)



def s_findNeighborhood(first_chromosome , h_reactListSelectedNum , react_list):
    global s_printFitnessList
    global s_selectedNeighbers
    changeItemNum =0 
    s_selectedNeighbers.clear()
    while changeItemNum < len(react_list):
        tempChromosome = chromosome.Chromosome(0,[],0 , 0)
        for i in first_chromosome.chromosome_detail :
            tempChromosome.chromosome_detail.append(i)
        if h_reactListSelectedNum[changeItemNum]+1 < len(react_list[changeItemNum].permutations_list):
            num = h_reactListSelectedNum[changeItemNum]+1
        else :
            num = 0
        tempChromosome.chromosome_detail[changeItemNum] = react_list[changeItemNum].permutations_list[num]
        tempChromosome.fitness = s_calcFitness(tempChromosome.chromosome_detail)
        s_selectedNeighbers.append(tempChromosome)
        changeItemNum+=1
        



def s_calcFitness(chromosome):
    global react_list
    global timePeriod
    worst = 9000000
    for i in range(timePeriod):
        sumMW = 0
        count = 0
        for item in chromosome:
            if item[i] == 0 :
                sumMW += int(react_list[count].MW)
            count+=1
        fitness = sumMW - requirement[i+1]
        if worst > fitness:
            worst = fitness
    return worst


def hill_climbing():
    global h_reactListSelectedNum 
    global react_list
    global h_printFitnessList


    global timePeriod
    global requirement
    for i in range(10):
        chromosome = h_create_random_chromosome()
        h_findNeighborhood(chromosome , h_reactListSelectedNum , react_list)

    
    h_findBestChromosome()

def h_create_random_chromosome():
    global react_list
    global h_reactListSelectedNum
    count = 0
    chrom = chromosome.Chromosome(0 , [],0,0)
    while chrom.chromosome_detail == []:
        chromosome_detail = []
        for react in react_list:
            rand = random.randint(0,len(react.permutations_list)-1)
            h_reactListSelectedNum.append(rand)
            chromosome_detail.append(react.permutations_list[rand])
        fitness = acceptable_chromosome(chromosome_detail)
        if fitness != -1:
            count +=1
            chrom = chromosome.Chromosome(count,chromosome_detail,fitness , 0)
        else:
            h_reactListSelectedNum.clear()
    return chrom

def h_findNeighborhood(chromosome , h_reactListSelectedNum , react_list):
    changeItemNum =0 
    changeChromosomItem = []
    global h_printFitnessList
    global h_bestChromosomeList 
    while changeItemNum < len(react_list):
        if h_reactListSelectedNum[changeItemNum]+1 < len(react_list[changeItemNum].permutations_list):
            num = h_reactListSelectedNum[changeItemNum]+1
        else :
            num = 0
        changeChromosomItem.append(chromosome.chromosome_detail[changeItemNum]) 
        chromosome.chromosome_detail[changeItemNum] = react_list[changeItemNum].permutations_list[num]
        fitness = acceptable_chromosome(chromosome.chromosome_detail)
        if fitness > chromosome.fitness :
            chromosome.fitness = fitness
        else :
            chromosome.chromosome_detail[changeItemNum] = changeChromosomItem[0]
        changeChromosomItem.clear()
        h_printFitnessList.append(fitness)
        h_bestChromosomeList.append(chromosome)
        changeItemNum+=1


def h_findBestChromosome():
    global h_printFitnessList
    global h_bestChromosomeList 
    maximum = max(h_printFitnessList)
    for item in h_bestChromosomeList:
        if item.fitness == maximum :
            best = item.chromosome_detail
    print("best")
    print(best)
    print("max")
    print(maximum)
    return best


if __name__ == "__main__":	
    main()