from roulette.game import *
from time import time
import random

if __name__=='__main__':
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
                 
    