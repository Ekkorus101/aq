from matplotlib import pyplot as plt
import random
from roulette.game import *


if __name__=='__main__':    
    ## main/test code
    random.seed(0)
    game = AmRoulette()
    total=[]                            ## make data for plot
    nSpins = []                         ## plot data
    for numSpins in range(100000,10000000,1000000):
        a = playRoulette(game, numSpins, genBetSet(1,set([]),1,1,1), 1, False)
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
   
        
        

