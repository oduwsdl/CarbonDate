import tkinter as tk 

LARGE_FONT= ("Verdana", 12)


class Gui(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top",expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in ([StartPage]):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


#FORMATTING FUNCTION FOR THE TKINTER ENTRY BOX 

             
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        def on_entry_click(event):
            """function that gets called whenever entry is clicked"""
            if URIentry.get() == 'https://cs.odu.edu/':
                URIentry.delete(0, "end") # delete all the text in the entry
                URIentry.insert(0, '') #Insert blank for user input
                URIentry.config(fg = 'black')
        def on_focusout(event):
            if URIentry.get() == '':
                URIentry.insert(0, 'https://cs.odu.edu/')
                URIentry.config(fg = 'grey')   
        def startlocal(uri): 
            print (uri)
            
        tk.Frame.__init__(self,parent)
        
        label = tk.Label(self, text="CarbonDate", font=LARGE_FONT)
        label.pack(pady=20,padx=50)

        label = tk.Label(self, text="Enter Uri:")
        label.pack()
        URIentry = tk.Entry(self)
        URIentry.insert(0, 'https://cs.odu.edu/')
        URIentry.config(fg = 'grey')
        URIentry.bind('<FocusIn>', on_entry_click)
        URIentry.bind('<FocusOut>', on_focusout)
        URIentry.pack()

        button = tk.Button(self, text="Estimate birthdate",
                            command=lambda: controller.show_frame(startlocal(URIentry.get())))
        button.pack()

    
    

