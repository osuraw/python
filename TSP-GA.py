import random
import numpy as np

def CreateDataSet (_numberofCities):
            
    cityMatrix = np.random.randint(25,size=(_numberofCities, _numberofCities))
    cityMatrix = (cityMatrix + cityMatrix.T)
    cityMatrix = cityMatrix - np.diag(cityMatrix.diagonal())
    
    citylist = list(range(0,_numberofCities))

    return cityMatrix,citylist

#create a child doing crossover 
def CreateChild(parent1,parent2):
    parent1 = parent1[1:-1]
    parent2 = parent2[1:-1]

    c1=c2=[]
    geneA = int(random.random() * len(parent1))
    geneB = int(random.random() * len(parent2))
    
    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    for i in range(startGene, endGene):
        c1.append(parent1[i])
        
    c2 = [item for item in parent2 if item not in c1]
    
    child = [0]
    child += c1 + c2
    child.append(0)
    

    return child

def GenerateCrossovers(parentPopulation):
    crossovers = []
    index = 0

    while index< len(parentPopulation)-1:
        
        p1 = parentPopulation[index:index+1][0]
        p2 = parentPopulation[index+1:index+2][0]        
        crossovers.append(CreateChild(p1,p2))
        index += 1

    #crossover between first and last instance in the population
    p1 = parentPopulation[0]
    p2 = parentPopulation[-1] 

    crossovers.append(CreateChild(p1,p2))

    return crossovers

def CrossoverFunction(parentPopulation,fromCrossovers):

    crossoverPopulation = GenerateCrossovers(parentPopulation)

    selectedpopulation = crossoverPopulation[:]
        
    for childNode in selectedpopulation:
        crossoverPopulation.append(MutationFunction(childNode))

    # select best set from the crossover
    return SelectionFunction(crossoverPopulation,fromCrossovers)

def SelectionFunction(population,populatioSize):
    selectedPopulation = []
    polulationFitness = CalculateFitness(population)
    
    templist = []
    for i,v in enumerate(polulationFitness):
        templist.append((population[i],v))

    templist.sort(key=lambda x: x[1],reverse=True)

    for i in range(0,populatioSize):
        selectedPopulation.append(templist[i][0])

    return selectedPopulation

def MutationFunction(childNode):
    return SwapCities(childNode)

#calculate cost of the given path
def PathCost(path): 
    cost = 0
    for i in range(0,CityCount-1):
        cityA = path[i]
        cityB = path[i+1]
        cost +=  CityMtrix[cityA,cityB]
    cost += CityMtrix[path[CityCount-1],0]
    return cost

def CalculateFitness(population):
    sum = 0
    fitness = []
    for path in population:
        cost =  PathCost(path)
        fitness.append(cost)
        sum += cost
    #get the inverse of the fitness
    for i,path in enumerate(population):
        fitness[i] = sum/fitness[i] 

    return fitness

def SwapCities(childNode):
    indexa = random.randint(1,CityCount-1)
    indexb = random.randint(1,CityCount-1)
    copy = childNode[:]
    temp = copy[indexa]
    copy[indexa] = copy[indexb]
    copy[indexb] = temp
    return copy

def FindBestPath(populationFitness):
    bestCost = 0
    bestCostIndex = 0
    for i,v in enumerate(populationFitness):
        if bestCost < v :
            bestCost = v
            bestCostIndex = i
    return bestCostIndex

def GeneratePopulation(CityList,populationSize):
    population = []
    for i in range(0,populationSize):
        path = SwapCities(CityList)
        path.append(0)
        population.append(path)
    return population


#control parameters
CityCount = 100
PopulationSize = 500
generationLimit = 100


#next generation selection criteria
fromOldpopulation = (int)(PopulationSize*0.3)
fromCrossovers = (int)(PopulationSize*0.5)
fromNewAdded = (int)(PopulationSize*0.2)

CityList = []
CityMtrix = []
Population = []
PopulationFitness = []

bestPath = []
bestCost = 99999999

CityMtrix , CityList = CreateDataSet(CityCount)

# create initial population
Population = GeneratePopulation(CityList,PopulationSize)


for i in range(0,generationLimit):

    newpupulation = []
    newpupulation = SelectionFunction(Population,fromOldpopulation) # select fittest for old population
    crossover = CrossoverFunction(newpupulation,fromCrossovers) # Crossvoce fittest from old populationa and mutate
    newlyAdded = GeneratePopulation(CityList,fromNewAdded) # newly created random instances 

    #crate new population
    newpupulation += crossover
    newpupulation += newlyAdded

    Population = newpupulation    

    #Calculate fitness of the population
    PopulationFitness = CalculateFitness(Population)
    # select best instance from population
    topIndex = FindBestPath(PopulationFitness)

    #get best path and path cost
    populationBestPath = Population[topIndex]
    populationBestCost = PathCost(populationBestPath)

    # compare with previous best values
    if(bestCost > populationBestCost):
        bestCost = populationBestCost
        bestPath = populationBestPath
        print("New best Cost Reached at Generation: {} with cost: {}".format(i,populationBestCost))

print("Best Path Cost: ",bestCost)
print("Best Path:      ",bestPath)