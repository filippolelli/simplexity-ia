import tkinter as tk
from tkinter.font import Font
from PIL import ImageTk, Image  
from simplexity import GameState, Simplexity, heuristic
from ai_player import ai_player
from variables import *
from checkers import *


class Options(tk.Frame):
    def __init__(self,parent,controller):
       tk.Frame.__init__(self,parent)
       self.controller=controller
       self.pixel = tk.PhotoImage(width=1, height=1)
       self.v = tk.IntVar()
       self.v.set(1)
       label=tk.Label(self,text="Game mode:")
       radio1=tk.Radiobutton(self,value=1,padx=10,compound="center",width=50,height=50,image=self.pixel,text="Against IA",variable=self.v)

       radio2=tk.Radiobutton(self,image=self.pixel,padx=10,compound="center",width=50,height=50,value=2,text="2 Humans",variable=self.v)
       button = tk.Button(self,text="Play",image=self.pixel,compound="center",width=50,height=50,command=lambda:  controller.show("Game"))
       label.pack(side="left")

       radio1.pack(side="left")
       radio2.pack(side="left")
       button.pack(side="left")

    def getValue(self):
           return self.v.get()
    
class Game(tk.Frame):
    def __init__(self, parent,controller):
        tk.Frame.__init__(self, parent)
        
        self.pixel = tk.PhotoImage(width=1, height=1)
        self.rc = tk.PhotoImage(file="images/Red_Circle(small).svg.png")
        self.rc=self.rc.subsample(50,50)
        self.rs = tk.PhotoImage(file="images/rs.png")
        
        for row in range(6):
            for col in range(7):
                button = tk.Button(self,image=self.pixel,width=50,height=50,command=lambda: move(col,controller.getOption()))
                button.grid(row=row,column=col)

        label=tk.Label(self,text="Pezzi a disposizione:")
        roundedbutton = tk.Label(self, image=self.rc,border=0,text="10",compound="center")
        squaredbutton = tk.Label(self, image=self.rs,border=0,text="10",compound="center")

        roundedbutton.grid()
        squaredbutton.grid()
class MainView(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames ={}

        self.frames["Options"] = Options(parent=container, controller=self)
        self.frames["Game"] = Game(parent=container, controller=self)

        self.frames["Options"].grid(row=0, column=0, sticky="nsew")
        self.frames["Game"].grid(row=0, column=0, sticky="nsew")

        
        self.show("Options")

    def show(self,page_name):
        frame = self.frames[page_name]
        frame.tkraise()    

    def getOption(self):
        return self.frames["Options"].getValue()



if __name__ == "__main__":
    app= MainView()
    ###app.geometry("600x600")
    app.title("Simplexity")
    app.resizable(False, False)
    app.configure()
    app.mainloop()


def move(col,option):
    return

def startGame(option,controller):
    controller.show("Game")
    game=Simplexity()
    end = False
    state=game.initial  
    