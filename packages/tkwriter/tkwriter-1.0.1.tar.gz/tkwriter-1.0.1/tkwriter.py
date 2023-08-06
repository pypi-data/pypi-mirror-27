class writerKl(object):
    def __init__(self):  
            import  tkinter
            from    tkinter import messagebox 
            from    tkinter import filedialog 
            from    tkinter import Tk         
            from    tkinter import Menu       
            from    tkinter import END             

            self.fileName = None  
            self.saved    = True
            self.app      = tkinter.Tk() 
            self.app.title("FenInst is another instance of the writerKl class")     

            self.menuBar  = tkinter.Menu(self.app)
            self.fileMenu = tkinter.Menu(self.menuBar, tearoff=0)
            self.fileMenu.add_command(label="New",     command=self.newFile)
            self.fileMenu.add_command(label="Open",    command=self.openFile)
            self.fileMenu.add_command(label="Save",    command=self.saveFile)
            self.fileMenu.add_command(label="Save As", command=self.saveFileAs)
            self.fileMenu.add_separator() ;  self.About = "A selfish tkinter text editor in 100 lines of python3 code.\n\n In fact this very ''About window'' also was modded using the selfish editor himself.\n\n Open the source ''writer.py'' to find out why this editor is seen as so 105x self-obsessed."
            self.fileMenu.add_command(label=     "About", command=lambda: tkinter.messagebox.showinfo("About", self.About))
            self.fileMenu.add_separator()
            self.fileMenu.add_command(label="Exit", command=self.onExit)
            self.menuBar.add_cascade( label="File", menu   =self.fileMenu)
            self.app.config(menu=self.menuBar)

            self.app.bind('<Control-n>', self.newFile )           # key Bindings
            self.app.bind('<Control-o>', self.openFile)
            self.app.bind('<Control-s>', self.saveFile)
            self.app.bind('<Key>',       self.setsavedFalse )
            self.app.protocol("WM_DELETE_WINDOW", self.onExit)    # save before exit?

            self.textf  = tkinter.Text(self.app)                  # initializing text container
            self.textf.pack(expand=True, fill='both')             # deploying text container
            self.textf.focus()         
            self.app.mainloop()

    def newFile(self):
        import  tkinter
        if not self.saved:
            save = self.promptToSave()
            if save:   self.saveFile()
            elif self.save is None:    return
        self.fileName = None
        self.textf.delete(0.0, tkinter.END)
        self.saved = True

    def openFile(self):
        import  tkinter
        if not self.saved:
            self.save = self.promptToSave()
            if self.save:
                self.saveFile()
            elif self.save is None:
                return
        try:
            self.f = tkinter.filedialog.askopenfile( filetypes=[  ('all files', '*') , ('py files', '.py')  ] )
            if self.f:
                self.fileName = self.f.name
                self.t = self.f.read()
                self.textf.delete(0.0, tkinter.END)
                self.textf.insert(tkinter.END, self.t)
                self.saved = True
        except:         tkinter.messagebox.showerror("Error", "Unable to open file.")

    def saveFile(self):
        import  tkinter
        self.t = self.textf.get(0.0, tkinter.END)
        if  self.fileName:
            self.f = open(self.fileName, "w")
            self.f.write(self.t)
            self.f.close()
            self.saved = True
        else:            self.saveFileAs()

    def saveFileAs(self):         
        import  tkinter
        self.f = tkinter.filedialog.asksaveasfile(defaultextension=".txt", filetypes=[ ('all files', '*'),('py files', '.py')  ])
        self.t = self.textf.get(0.0, tkinter.END)
        if self.f:
            try:
                self.f.write(self.t)
                self.f.close(      )
                self.saved = True
                self.fileName=self.f.name
            except: tkinter.messagebox.showwarning("Error", "Unable to save file.")

    def onExit(self):                
        import  tkinter
        if not                self.saved:
            self.save =       self.promptToSave()
            if self.save:     self.saveFile()
            elif self.save is None:    return
        self.app.destroy()

    def setsavedFalse(self, key):                
        import  tkinter
        if (key.keysym.isalpha() or key.keysym.isdigit() or key.keysym in ["Return", "Tab", "Backspace", "Delete"]):   self.saved = False  # any key that changes text    
            
    def promptToSave(self):
        import  tkinter
        return tkinter.messagebox.askyesnocancel(     "Save file?", "Do you want to save the current file?")


if __name__ == '__main__' : 
    import tkinter
    FenInst  =writerKl() 