# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import chatbot

class Window(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.Frame1 = tk.Frame(height=10)
        self.Frame1.pack()
        self.about = tk.Label(text='AI Creator: Show De Yang, 2019')
        self.about.pack()
        self.Frame1 = tk.Frame(height=10)
        self.Frame1.pack()

#        self.status = tk.Label(master=self.Frame3, justify='left',wraplength=650)
#        self.status.pack()
        self.T = ScrolledText(root, height=20)
        self.T.pack()
        # quote = "\n"

        # self.T.insert(tk.END, quote)
        # self.T.insert(tk.END, 'Hello')
        self.T.configure(state=tk.DISABLED)
        self.T.see(tk.END)
        self.Frame1 = tk.Frame(height=10)
        self.Frame1.pack()
        self.multilineInput = ScrolledText(self.master, height=10)
        self.multilineInput.pack()
        #print(self.multilineInput)
        root.bind('<Control-Return>', self.func)

        self.submit = tk.Button(text='提交问题', command=self.func)
        self.submit.pack()


        
        
    def func(self, event=5):
        query = self.multilineInput.get("1.0","end-1c")
        #print(query)
        query1 = 'ME: ' + query
        self.multilineInput.delete('1.0',tk.END)
        self.T.configure(state=tk.NORMAL)
        self.T.insert(tk.END, query1)
        self.T.see(tk.END)
        self.T.configure(state=tk.DISABLED)
        root.update()
        answer = chatbot.reply(query1)
        answer1 = '\nLILY: ' + answer +'\n'
        self.T.configure(state=tk.NORMAL)
        self.T.insert(tk.END, answer1)
        self.T.see(tk.END)
        self.T.configure(state=tk.DISABLED)

 
if __name__ == '__main__':

    root = tk.Tk()
    app = Window(root)
    #set window title
    root.wm_title("Lily")
    root.geometry('700x500')
    #show window
    root.mainloop()

