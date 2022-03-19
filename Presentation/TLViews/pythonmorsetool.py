from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkinter import filedialog
import morseconverter

# Initialise morse code converter class
morse = morseconverter.MorseConverter()

def open_file():
    file_name = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))    
    f = open(file_name, "r")
    morse_text = f.read()
    text.insert(INSERT, morse_text)

def convert():
    label["text"] = morse.to_morse(text.get("1.0",END)) # The first part, "1.0" means that the input should be read from line one, character zero. The END part means to read until the end of the text box is reached.

def about():    
    messagebox.showinfo("About", "Morse Tool")

# Create tkinter GUI
root = Tk() 

# Window size and position
root.title("Morse Tool")
root.geometry("640x480")
root.columnconfigure(0, weight=1)

# Add a menu
menu = Menu(root) 
root.config(menu=menu)

# Create the file menu
filemenu = Menu(menu) 
menu.add_cascade(label="File", menu=filemenu)   
filemenu.add_command(label="Open...", command=open_file)
filemenu.add_separator() 
filemenu.add_command(label="Exit", command=root.quit) 

# Tool menu
toolsmenu = Menu(menu)
menu.add_cascade(label="Tools", menu=toolsmenu)
toolsmenu.add_command(label="Convert", command = convert)

# Create the help menu
helpmenu = Menu(menu) 
menu.add_cascade(label="Help", menu=helpmenu) 
helpmenu.add_command(label="About", command=about)

# Add a text area
root.rowconfigure(0, weight=1) # prioritise this area (grow this row to fill empty space)
text = Text(root, height=20) 
text.grid(row=0, column=0, sticky=N+E+W+S)

# Add a display area
label = Label(root, text="Welcome to python morse tool...")
label.grid(row=1, column=0, sticky=N+E+W+S) 

# Our GUI is complete
mainloop() 