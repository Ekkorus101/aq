from cgitb import text
from http.client import ImproperConnectionState
from ipaddress import _BaseNetwork
from multiprocessing import BufferTooShort
from sys import maxsize
import tkinter as tk
from tkinter import  ttk
from roulette.game import *

class gameUI():
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("roulette")
        self.root.geometry('500x500')
        
        self.gameType=0
        self.game=FairRoulette()
        self.betType=0
        self.varOddEven = tk.IntVar()
        self.varColor = tk.IntVar()
        self.varArea = tk.IntVar()
        self.varBetOne = '1'
        self.assets=0
        
        self.root.grid_rowconfigure(0,weight=1)
        self.root.grid_rowconfigure(1,weight=1)
        self.root.grid_columnconfigure(0,weight=1)
        self.root.grid_columnconfigure(1,weight=1)
        
        self.frame1 = tk.Frame(self.root,padx=5,pady=5,height=390, bg='white')
        self.frame2 = tk.Frame(self.root,padx=5,pady=5,height=50,bg='white')
        self.frame3 = tk.Frame(self.root,padx=5,pady=5,height=50,bg='white')
        self.frame4 = tk.Frame(self.root,padx=5,pady=5,height=50,bg='white')
        self.frame5 = tk.Frame(self.root,padx=5,pady=5,height=50,bg='white')
        self.frame6 = tk.Frame(self.root,padx=5,pady=5,height=50,bg='white')
        
        self.labelAssets=tk.Label(self.frame4)
        self.labelBetInfo=tk.Label(self.frame5)
        self.labelGameType=tk.Label(self.frame6)

        button1 = tk.Button(self.frame2, text="bet one",command=self.betOne)
        button3 = tk.Button(self.frame2, text="bet multi",command=self.betMulti)
        button4 = tk.Button(self.frame3, text="game type",command=self.setGameType)
        button2 = tk.Button(self.frame3, text="spin",command=self.spin)
        
        button1.pack(side=tk.LEFT,padx=20)
        button3.pack(side=tk.LEFT,padx=20)
        button2.pack(side=tk.RIGHT,padx=20)
        button4.pack(side=tk.RIGHT,padx=20)
        self.labelAssets.pack(anchor=tk.CENTER)
        self.labelBetInfo.pack(anchor=tk.CENTER)
        self.labelGameType.pack(anchor=tk.CENTER)
        
        self.frame4.grid(row=1,column=0,rowspan=1,columnspan=1,sticky=tk.NSEW)
        self.frame5.grid(row=1,column=1,rowspan=1,columnspan=1,sticky=tk.NSEW)
        self.frame1.grid(row=2,column=0,rowspan=3,columnspan=2,sticky=tk.NSEW)
        self.frame2.grid(row=5,column=0,sticky=tk.NSEW)
        self.frame3.grid(row=5,column=1,sticky=tk.NSEW)
        self.frame6.grid(row=0,column=0,rowspan=1,columnspan=2,sticky=tk.NSEW)
        self.reFresh()
    
    def reFresh(self):
        self.resetBetInfo()
        self.resetAssets()
        self.resetGameType()

    def mainLoop(self):
        self.root.mainloop()
        
    def resetGameType(self):
        self.labelGameType.config(text='game:'+str(self.game))
        
    def resetAssets(self):
        self.labelAssets.config(text='assets:'+str(self.assets))
    
    def resetBetInfo(self):
        if 0==self.betType:
            self.labelBetInfo.config(text='bet one:'+self.varBetOne)
        else:
            s='bet multi:'
            if self.varOddEven.get() != 0:
                s1=' odd ' if self.varOddEven.get()==1 else ' even '
                s+=s1
            
            if self.varColor.get() != 0:
                s1=' red ' if self.varColor.get()==1 else ' black '
                s+=s1
    
            if self.varArea.get() != 0:
                s1=[' 1-18 ',' 19-36 ',' 1-12 ',' 13-24 ',' 25-36']
                s+=s1[self.varArea.get()-1]
            
            self.labelBetInfo.config(text=s)
    
    def setGameType(self):
        betWindow = tk.Toplevel()
        betWindow.title("choose game")

        frameGame = tk.Frame(betWindow,padx=5,pady=5,bg='white')
        frameButton =tk.Frame(betWindow,padx=5,pady=5,bg='white')
        
        frameGame.grid(row=0,column=0,rowspan=1,columnspan=1,sticky=tk.NSEW)
        frameButton.grid(row=1,column=0,rowspan=1,columnspan=1,sticky=tk.NSEW)
        cb=ttk.Combobox(frameGame)
        cb['value']=['FairRoulette','EuRoulette','AmRoulette']
        cb.pack(anchor=tk.CENTER)
        
        def setGame():
            if cb.get()=='FairRoulette':
                self.gameType=0
                self.game=FairRoulette()
            elif cb.get()=='EuRoulette':
                self.gameType=1
                self.game=EuRoulette()
            else:
                self.gameType=2
                self.game=AmRoulette()
            self.resetGameType()
            betWindow.destroy()
        tk.Button(frameButton,text="confirm",padx=40,command=setGame).pack(side=tk.LEFT)
        tk.Button(frameButton,text="cancel",padx=40,command=betWindow.destroy).pack(side=tk.RIGHT)
    
    def betOne(self):
        betWindow = tk.Toplevel()
        betWindow.title("choose your bet")

        frameBet = tk.Frame(betWindow,padx=5,pady=5,bg='white')
        frameButton =tk.Frame(betWindow,padx=5,pady=5,bg='white')
        
        frameBet.grid(row=0,column=0,rowspan=1,columnspan=1,sticky=tk.NSEW)
        frameButton.grid(row=1,column=0,rowspan=1,columnspan=1,sticky=tk.NSEW)
        cb=ttk.Combobox(frameBet)
        l=self.game.pockets[:]
        if len(l)>=37:
            l[36]='0'
        if len(l)>=38:
            l[37]='00'
        cb['value']=l
        
        cb.pack(anchor=tk.CENTER)
        
        def resetInfo():
            self.betType=0
            self.varBetOne=cb.get()
            self.resetBetInfo()
            betWindow.destroy()
        tk.Button(frameButton,text="bet",padx=40,command=resetInfo).pack(side=tk.LEFT)
        tk.Button(frameButton,text="cancel",padx=40,command=betWindow.destroy).pack(side=tk.RIGHT)
    
    def betMulti(self):
        betWindow = tk.Toplevel()
        betWindow.title("choose your bet")
    
        frameOdd = tk.Frame(betWindow,padx=5,pady=5, bg='white')
        frameColor = tk.Frame(betWindow,padx=5,pady=5, bg='white')
        frameArea = tk.Frame(betWindow,padx=5,pady=5,bg='white')
        frameButton =tk.Frame(betWindow,padx=5,pady=5,bg='white')
    
        frameOdd.grid(row=0,column=0,rowspan=1,columnspan=1,sticky=tk.NSEW)
        frameColor.grid(row=0,column=1,rowspan=1,columnspan=1,sticky=tk.NSEW)
        frameArea.grid(row=0,column=2,rowspan=1,columnspan=1,sticky=tk.NSEW)
        frameButton.grid(row=1,column=0,rowspan=1,columnspan=3,sticky=tk.NSEW)
    
        tk.Radiobutton(frameOdd, text = "not choose", variable = self.varOddEven, value = 0).pack(anchor=tk.W)
        tk.Radiobutton(frameOdd, text = "odd", variable = self.varOddEven, value = 1).pack(anchor=tk.W)
        tk.Radiobutton(frameOdd, text = "even", variable = self.varOddEven, value = 2).pack(anchor=tk.W)
        self.varOddEven.set(0)
    
        tk.Radiobutton(frameColor, text = "not choose", variable = self.varColor, value = 0).pack(anchor=tk.W)
        tk.Radiobutton(frameColor, text = "red", variable = self.varColor, value = 1).pack(anchor=tk.W)
        tk.Radiobutton(frameColor, text = "black", variable = self.varColor, value = 2).pack(anchor=tk.W)
        self.varColor.set(0)
    
        tk.Radiobutton(frameArea, text = "not choose", variable = self.varArea, value = 0).pack(anchor=tk.W)
        tk.Radiobutton(frameArea, text = "1-18", variable = self.varArea, value = 1).pack(anchor=tk.W)
        tk.Radiobutton(frameArea, text = "19-36", variable = self.varArea, value = 2).pack(anchor=tk.W)
        tk.Radiobutton(frameArea, text = "1-12", variable = self.varArea, value = 3).pack(anchor=tk.W)
        tk.Radiobutton(frameArea, text = "13-24", variable = self.varArea, value = 4).pack(anchor=tk.W)
        tk.Radiobutton(frameArea, text = "25-36", variable = self.varArea, value = 5).pack(anchor=tk.W)
        self.varArea.set(0)
    
        def resetInfo():
            self.betType=1
            self.resetBetInfo()
            betWindow.destroy()
        tk.Button(frameButton,text="bet",padx=40,command=resetInfo).pack(side=tk.LEFT)
        tk.Button(frameButton,text="cancel",padx=40,command=betWindow.destroy).pack(side=tk.RIGHT)
        
    def spin(self):
        if 0==self.betType:
            if '0'==self.varBetOne:
                betSet=set([37])
            elif '00'==self.varBetOne:
                betSet=set([38])
            else:
                betSet=set([int(self.varBetOne)])
        else:
            betSet=genBetSet(1,set(),self.varOddEven.get(),self.varColor.get(),self.varArea.get())
        self.game.spin()
        print(betSet)
        print(self.game.ball)
        self.assets+=self.game.betPocket(betSet,1)
        self.reFresh()

gameui=gameUI()
gameui.mainLoop()