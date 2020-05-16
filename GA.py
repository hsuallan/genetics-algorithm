import math 
import random
import sys
class cfg():
    def __init__(self,rangeX,rangeY,populationLen,dnaLen):
        self.rangeX = rangeX
        self.rangeY = rangeY
        self.populationLen = populationLen
        self.dnaLen = dnaLen
    pass
def getfitness(x,y):
    return 21.5+(x*math.sin(4*math.pi*x))+(y*math.sin(20*math.pi*y))

def randomDNA(len):
    arr = []
    for i in range(0,len):
        arr.append(random.randrange(2))
    return arr
def geneToNumber(cfg,gene):
    x = 0
    y = 0
    for index,item in enumerate(gene):
        if index < len(gene)/2:
            x += item*math.pow(2,index)
        else:
            y += item*math.pow(2,index-len(gene)/2)
    x = cfg.rangeX[0]+((cfg.rangeX[1]-cfg.rangeX[0])/math.pow(2,len(gene)/2)*x)
    y = cfg.rangeY[0]+((cfg.rangeY[1]-cfg.rangeY[0])/math.pow(2,len(gene)/2)*y)
    return [x,y]
def population(cfg):
    pop = []
    for item in range(0,cfg.populationLen):
        pop.append(randomDNA(cfg.dnaLen))
    return pop
def crossover(f,m):
    # f/m is gene
    child= []
    for index in range(0,len(f)):
        if random.randrange(2) == 1:
            child.append(f[index])
        else:
            child.append(m[index])
    return child
def mutate(gene):
    rate = 25
    for index in range(0,len(gene)):
        if random.randrange(1,100) < rate:
            gene[index] = 1 if  gene[index] == 0 else 1
    return gene
def findMax(d1):
    d2 = d1.copy()
    v = list(d2.values())
    k = list(d2.keys())
    return k[v.index(max(v))]
def selection(cfg,pop,times,上一次結果):
    all = dict(上一次結果)
    for index,item in enumerate(pop):
        if index in all:
            # 已做過的跳過
            pass
        else:
            gene = geneToNumber(cfg,item)
            x = gene[0]
            y = gene[1]
            all[index] = getfitness(x,y)
    maxIndex = findMax(all)
    father = pop[maxIndex]
    return [father,all]    
if __name__ == "__main__":
    if  len(sys.argv) == 1 or sys.argv[1] == "help":
        print('python GA.py {{ population }} {{ genelength }} {{ generation }}')
    else:
        最近的最好結果 = []
        cfg = cfg([-3.0,12.1],[4.1,5.8],int(sys.argv[1]),int(sys.argv[2]))
        pop = population(cfg)
        best = [000,{}]
        for times in range(int(sys.argv[3])):
            best = selection(cfg,pop,times,best[1])
            pop.append(mutate(crossover(best[0],pop[random.randrange(0,len(pop))])))
            #print ans
            gene = geneToNumber(cfg,best[0])
            x = gene[0]
            y = gene[1]
            ans = getfitness(x,y)
            最近的最好結果.append(ans)
            if len(最近的最好結果) == 1000:
                最近的最好結果 = set(最近的最好結果)
                if len(最近的最好結果) == 1:
                    print("最近1000次都沒變 第",times-1000,"~",times,"的結果",'---->',x,y,ans)
                    exit()
                最近的最好結果 = []
            if times%1000 == 0:
                gene = geneToNumber(cfg,best[0])
                x = gene[0]
                y = gene[1]
                ans = getfitness(x,y)
                print(times,'---->',x,y,ans)
