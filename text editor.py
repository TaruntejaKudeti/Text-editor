from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
import datetime
import os
import time


# Creating and initializing the window
root = Tk()
root.title("TEXT_EDITOR")
root.geometry("800x500")
root.resizable(height=None,width=None)
 
 
# Status bar
statbarb = Label(root, text="Ln", relief=SUNKEN, bd=1, anchor="w")


# Global variables


# Variable for the present file loaded
filvar=None


# Text Area
# Adding the text area
textarea=Text(root,undo=True,wrap=None,height=root.winfo_height(),width=root.winfo_width())
textarea.grid(row=0,sticky= N + E + S + W )
# Making the text area auto resizable
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)


#Scroll Bar
#Creating the vertical scrollbar
scrollbarv=Scrollbar(textarea,command=textarea.yview)
#Adding the scrollbar to textarea window
textarea.config(yscrollcommand=scrollbarv.set)
#Packing the scrollbar
scrollbarv.pack(side=RIGHT, fill=Y)


#Various functions of the text editor
# Function to create a new file
def createnew(*args):
    global root, textarea, filvar
    filvar=None
    root.title("New File")
    textarea.delete(1.0,END)
    
 
# Function to open a locally existing file   
def openfile(*args):
    global root, textarea, filvar, origfilecontents
    filvar = askopenfilename(defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Files","*.txt")])
    if filvar=="":
        filvar=None
        origfilecontents=None
    else:
        try:
            root.title(os.path.basename(filvar))
            textarea.delete(1.0, END)
            file = open(filvar, "r")
            textarea.insert(1.0, file.read())
            origfilecontents=file.read()
            file.close()
        except:
            root.title("NeeruText")
            showerror("ERROR",str("Unable to open "+filvar+"\n"+"Not a .txt file!"))


# Function to save the files
def savefile(*args):
    global root,textarea,filvar, origfilecontents
    if filvar==None:
        saveasfile()
    else:
        file=open(filvar,"w")
        origfilecontents=textarea.get(1.0,END)
        file.write(textarea.get(1.0, END))
        file.close()
        showinfo("Successfully saved","All changes saved")


def saveasfile():
    global root,textarea,filvar
    filvar = asksaveasfilename(defaultextension=".txt",filetypes=[("All Files", "*.*"),("Text Documents", "*.txt")])
    if filvar=="":
        filvar=None
    else:
        file=open(filvar,"w")
        file.write(textarea.get(1.0,END))
        file.close()
        showinfo("Successfully saved", str("Saved as "+filvar+" successfully!"))


# Function to Show the date and time 
def datetimefunc(*args):
    global textarea
    textarea.insert(END,str(datetime.datetime.now()))
    
    
# Function to perform cut operation   
def cutop():
    global textarea
    textarea.event_generate("<<Cut>>")
    
    
# Function to perform copy operation   
def copyop():
    global textarea
    textarea.event_generate("<<Copy>>")
    
    
# Function to perform paste operation   
def pasteop():
    global textarea
    textarea.event_generate("<<Paste>>")
    

# Function to perform delete operation   
def deleteop():
    global textarea
    ranges=textarea.tag_ranges(SEL)
    textarea.delete(*ranges)
    
 
# Display the about    
def about():
    showinfo("About TEXT_EDITOR","This is a text editor built using Tkinter\nDeveloped by Perumalla Dharan\nGithub: https://github.com/PerumallaDharan")


# Function to exit the program
def exitapplication():
    root.quit()
    

# Function to select all the text
def selectall():
    global textarea
    textarea.event_generate("<<SelectAll>>")
    
    
# Function for undo operation
def undofunc():
    global textarea
    try:
        textarea.edit_undo()
    except:
        pass
    
    
# Function for redo operation
def redofunc():
    global textarea
    try:
        textarea.edit_redo()
    except:
        pass
    

# Function to check the number of lines
def findlinecount():
    global textarea,submenu3
    if textarea.compare("end-1c", "!=", "1.0"):
        submenu6.entryconfig(0,label=str(str(int(textarea.index('end').split('.')[0]) - 1)+" Lines"))
        
    
# Function to count the number of words        
def findwordcount():
    global textarea,submenu5
    if textarea.compare("end-1c", "!=", "1.0"):
        submenu5.entryconfig(0,label=str(str(len(textarea.get(0.0,END).replace("\n"," ").split(" "))-1)+" Words"))


# Function to check if user wants to exit without saving the file contents
def exitwithoutsaving():
    global root,textarea,origfilecontents
    if filvar!=None:
        if origfilecontents==textarea.get(1.0,END):
            pass
        else:
            exitapplication()
    result = askquestion(title="Exit", message=str("Do you want to save changes made to "+(os.path.basename(filvar) if filvar!=None else "New File")+" ?"), icon='warning')
    if result == 'yes':
        savefile()
    else:
        exitapplication()


# Binding shortcut keys to functions
textarea.bind("<F5>",datetimefunc)
textarea.bind("<Control-n>" or "<Control-N>",createnew)
textarea.bind("<Control-s>" or "<Control-S>",savefile)
textarea.bind("<Control-o>" or "<Control-O>",openfile)


# Adding the main menu
menu=Menu(root)
root.config(menu=menu)


# Adding the File submenu
submenu1=Menu(menu,tearoff=0)
menu.add_cascade(label="File",menu=submenu1)
submenu1.add_command(label="New    Ctrl+N",command=createnew)
submenu1.add_command(label="Open   Ctrl+O",command=openfile)
submenu1.add_command(label="Save    Ctrl+S",command=savefile)
submenu1.add_command(label="Save as",command=saveasfile)
submenu1.add_separator()
submenu1.add_command(label="Exit",command=exitwithoutsaving)


# Adding the Edit submenu
submenu2=Menu(menu,tearoff=0)
menu.add_cascade(label="Edit",menu=submenu2)
submenu2.add_command(label="Undo        Ctrl+Z",command=undofunc)
submenu2.add_command(label="Redo        Ctrl+Y",command=redofunc)
submenu2.add_separator()
submenu2.add_command(label="Cut          Ctrl+X",command=cutop)
submenu2.add_command(label="Copy       Ctrl+C",command=copyop)
submenu2.add_command(label="Paste       Ctrl+V",command=pasteop)
submenu2.add_command(label="Delete      Del",command=deleteop)
submenu2.add_separator()
submenu2.add_command(label="Select all    Ctrl+A",command=selectall)
submenu2.add_command(label="Date/Time   F5",command=datetimefunc)


# Adding the view submenu
submenu3=Menu(menu,tearoff=0)
submenu5=Menu(submenu3,tearoff=0,postcommand=findwordcount)
submenu6=Menu(submenu3,tearoff=0,postcommand=findlinecount)
menu.add_cascade(label="View",menu=submenu3)
submenu3.add_cascade(label="Word Count",menu=submenu5)
submenu3.add_cascade(label="Line Count",menu=submenu6)
submenu5.add_command(label="0 Words",command=None)
submenu6.add_command(label="0 Lines",command=None)


# Adding the about submenu
submenu4=Menu(menu,tearoff=0)
menu.add_command(label="About",command=about)


# Running the main loop
root.mainloop