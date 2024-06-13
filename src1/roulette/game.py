import queue
from time import time
import random, pylab
from matplotlib import pyplot as plt

#set line width
pylab.rcParams['lines.linewidth'] = 4
#set font size for titles 
pylab.rcParams['axes.titlesize'] = 20
#set font size for labels on axes
pylab.rcParams['axes.labelsize'] = 20
#set size of numbers on x-axis
pylab.rcParams['xtick.labelsize'] = 16
#set size of numbers on y-axis
pylab.rcParams['ytick.labelsize'] = 16
#set size of ticks on x-axis
pylab.rcParams['xtick.major.size'] = 7
#set size of ticks on y-axis
pylab.rcParams['ytick.major.size'] = 7
#set size of markers, e.g., circles representing points
#set numpoints for legend
pylab.rcParams['legend.numpoints'] = 1

class FairRoulette():
    def __init__(self):
        self.pockets = []
        for i in range(1,37):
            self.pockets.append(i)
        self.ball = None
    def spin(self):
        self.ball = random.choice(self.pockets)
    def betPocket(self, pocket, amt):
        if self.ball in pocket:
            return amt*((36-len(pocket))/len(pocket))
        else: return -amt
    def __str__(self):
        return 'Fair Roulette'

def playRoulette(game, numSpins, pocket, bet, toPrint):
    totPocket = 0
    for i in range(numSpins):
        game.spin()
        totPocket += game.betPocket(pocket, bet)
    if toPrint:
        print(numSpins, 'spins of', game)
        print('Expected return betting', pocket, '=',\
              str(100*totPocket/numSpins) + '%\n')
    return (totPocket/numSpins)


class EuRoulette(FairRoulette):
    def __init__(self):
        FairRoulette.__init__(self)
        self.pockets.append(37)         # 37 -> 0
    def __str__(self):
        return 'European Roulette'

class AmRoulette(EuRoulette):
    def __init__(self):
        EuRoulette.__init__(self)
        self.pockets.append(38)         # 38 -> 00
    def __str__(self):
        return 'American Roulette'
        
def findPocketReturn(game, numTrials, trialSize, betSet,toPrint):
    pocketReturns = []
    for t in range(numTrials):
        trialVals = playRoulette(game, trialSize, betSet, 1, toPrint)
        pocketReturns.append(trialVals)
    return pocketReturns

def getMeanAndStd(X):
    mean = sum(X)/float(len(X))
    tot = 0.0
    for x in X:
        tot += (x - mean)**2
    std = (tot/len(X))**0.5
    return mean, std


def genBetSet(genType:int,manualBet:set,oddEven:int=0,redBlack:int=0,numArea:int=0,store=[]):
    """
    this func generate a bet list
    
    param:
        genType: 
            0:manual
            1:area bet
        manualBet: 
            vaild only when genType==0 , choose manual param
        oddEven: 
            valid only when genType==1, below too. choose area odd or even: 
            0:not choose
            1:odd 
            2:even
        redBlack:
            0:not choose
            1:red
            2:black
        numArea:
            0:not choose
            1:1-18
            2:19-36
            3:1-12
            4:13-24
            5:25-36
        store:
            dont use this

    return:
        set: betList eg set([1])
    """
    if len(store)==0:
        setList=[[set([i for i in range(1,37)]),
                  set([i for i in range(1,37,2)]),
                  set([i for i in range(2,37,2)])],
                 [set([i for i in range(1,37)]),
                  set([3,12,7,18,9,14,1,16,5,23,30,36,27,34,25,21,19,32]),
                  set([i for i in range(1,37)])-set([3,12,7,18,9,14,1,16,5,23,30,36,27,34,25,21,19,32])],                  
                 [set([i for i in range(1,37)]),
                  set([i for i in range(1,19)]),
                  set([i for i in range(19,37)]),
                  set([i for i in range(1,13)]),
                  set([i for i in range(13,25)]),
                  set([i for i in range(25,37)])
                 ]]    
        store.append(setList)
    
    if 0==genType:
        return manualBet
    elif 1==genType:
        return store[0][0][oddEven].intersection(store[0][1][redBlack].intersection(store[0][2][numArea]))
    else:
        raise ValueError('genType error')


if __name__=='__main__':
    
    ## main/test code
    random.seed(0)
    game = FairRoulette()
    total=[]                            ## make data for plot
    nSpins = []                         ## plot data
    for numSpins in range(10,1000,50):
        a = playRoulette(game, numSpins, 1, 1)                  ## attention: bet and pocket canbe different
        total.append(a)                 
        nSpins.append(numSpins)    
        
    ## Data print
    print("BetPocket =",total)         
    print() 
    print("Play times =",nSpins)
    
    ## plot
    plt.plot(nSpins,total)                                          ## plot(x,y) in figure  
    
    temp =int(sum(total)*1000)/10
    print(temp)
    
    plt.title("Fair Roullet Simulation: "+str(temp)+"%",fontsize=14,color="g")      ## title
    
    plt.xlabel("play times:"+str(sum(nSpins)),fontsize=15,color="red")  ## X-axis label
    plt.ylabel("Win Rate" ,fontsize=16,color="b")                       ## Y-axis label
    
    ## plt.text(10,0.6,str(temp)+"%",fontsize=14,color="b")## text in figure
    
    plt.scatter(nSpins,total)                       ## scatter 
    plt.plot([0,max(nSpins)],[0,0],color="r")       ## baseline
    plt.show()
    
    ## hist
    ##plt.stairs(total)
    ##plt.show()
   
    exit(0) 
        
        
    # simulate eg: single num bet
    t1=time()
    random.seed(0)
    game = FairRoulette()
    iter = 10000000
    betSet=genBetSet(0,set([1]))
    playRoulette(game, iter ,betSet , 1, True)
    print("time spend:"+str(round(time()-t1,2))+"s\n")
        
    # simulate eg: odd + red + 1-18 bet
    t1=time()
    random.seed(0)
    game = FairRoulette()
    iter = 10000000
    playRoulette(game, iter , genBetSet(1,set([]),1,1,1), 1, True)
    print("time spend:"+str(round(time()-t1,2))+"s\n")
    
    #simulate eg: single num bet
    random.seed(0)  
    numTrials = 20
    resultDict = {}
    games = (FairRoulette, EuRoulette, AmRoulette)
    for G in games:
        resultDict[G().__str__()] = []
    for numSpins in (10,1000,100000):         ##  , 10000, 100000, 1000000):
        print('\nSimulate', numTrials, 'trials of',numSpins, 'spins each')
        for G in games:
            pocketReturns = findPocketReturn(G(), numTrials, numSpins,genBetSet(0,set([1])), False)
            expReturn = 100*sum(pocketReturns)/len(pocketReturns)
            print('Exp. return for', G(), '=', str(round(expReturn, 4)) + '%')
    
    #simulate eg: odd + red + 1-18 bet
    random.seed(0)  
    numTrials = 20
    resultDict = {}
    games = (FairRoulette, EuRoulette, AmRoulette)
    for G in games:
        resultDict[G().__str__()] = []
    for numSpins in (10,1000,100000):         ##  , 10000, 100000, 1000000):
        print('\nSimulate', numTrials, 'trials of',numSpins, 'spins each')
        for G in games:
            pocketReturns = findPocketReturn(G(), numTrials, numSpins,genBetSet(1,set([]),1,1,1), False)
            expReturn = 100*sum(pocketReturns)/len(pocketReturns)
            print('Exp. return for', G(), '=', str(round(expReturn, 4)) + '%')
                 
    