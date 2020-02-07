import os
import sqlite3 as sql
from tkinter import ttk
from tkinter import *
from tkinter import Menu
from tkinter import filedialog as fd
from tkinter.filedialog import askdirectory 
from tkinter import scrolledtext
from tkinter import messagebox

from tabulate import tabulate

from modules.sqlite import sqlite

path_gif = os.path.dirname(os.path.realpath(__file__)) + '/res/database-settings-icon.gif'
path_ico = os.path.dirname(os.path.realpath(__file__)) + '/res/database-settings-icon.ico'


def clear_widgets(name):
    '''
    ###############################

    this function will delete all widgets from a window

    ###############################
    '''

    list = name.grid_slaves()
    for l in list:
        l.destroy()

def center_window(page,width=300, height=200):
    '''
    ###############################

    this function will get screen width and height and 
    calculate position x and y coordinates then set the window 
    geometry

    ###############################
    '''

    # get screen width and height
    screen_width = page.winfo_screenwidth()
    screen_height = page.winfo_screenheight()
    # calculate position x and y coordinates
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    page.geometry('%dx%d+%d+%d' % (width, height, x, y))

    
def pageDesign(page,height,width):
    '''
    ###############################

    this function will set defualt page settings 

    ###############################
    '''
    center_window(page,height,width)
    if "nt" == os.name:
        page.iconbitmap(bitmap = path_ico)
    page.title('SQLite Browser')
    page.configure(background= '#DCDCDC')
    page.resizable(0,0)

def get_tables(database):
    '''
    ###############################

    this function will dump tables from database file 

    ###############################
    '''
    tables = database.show_tables()
    result = []
    for table_t in tables:
        for table_l in table_t:
            if table_l not in result:
                result.append(table_l)

    return result
    




def main():
    '''
    ###############################

    this function is the main page configuration functaion

    ###############################
    '''
    window = Tk()

    def btnBrowse():
        '''
    ###############################

    this function will appear a page and ask you for opening
    your database file and check if it is a sqlite file or
    not

    ###############################
        '''
        fileName = fd.askopenfilenames()
        ext = os.path.splitext(fileName[0])[-1].lower()
        if ext == '.db':
            window.destroy()
            desk(fileName)
        else:
            messagebox.showerror('file is not a database', 'please choose a database file')            


    def btnCreateDB():
        '''
    ###############################

    this function will appear a page and ask you to choose
    the database path and then create a page and ask
    for database name

    ###############################
        '''
        def btnCreate():
            name = inp.get()
            db_path = dirName + '/' + name + '.db'
            if os.path.exists(db_path) == False:
                with open(db_path , 'w') as f:
                    create.destroy()
                    window.destroy()
                desk((db_path,))
            else:
                messagebox.showerror('file is already exist', 'please choose another name')
                create.destroy()

                
                
        dirName = askdirectory()
        create = Tk()
        pageDesign(create,300,100)
        lbl=Label(create,text='Database name:',font=('Times' , '11','italic'),fg='#17202a',bg='#DCDCDC')
        lbl.place(relx=0.01, rely=0.03 , anchor=NW)
        inp = Entry(create,width=20)
        inp.place(relx=0.7, rely=0.15, anchor=CENTER)
        btn_browse = Button(create,text='Create',width=20,command=btnCreate)
        btn_browse.place(relx=0.5, rely=0.8, anchor=CENTER)
        create.mainloop()


    pageDesign(window,520,420)    
    img = PhotoImage(file=path_gif)
    panel = Label(window, image = img , bg='#DCDCDC')
    panel.place(relx=0.5, rely=0.33, anchor=CENTER)
    btn_browse = Button(window,text='Open Database...',width=27,command=btnBrowse)
    btn_browse.place(relx=0.5, rely=0.7, anchor=CENTER)
    btn_browse = Button(window,text='Create New Database',width=27,command=btnCreateDB)
    btn_browse.place(relx=0.5, rely=0.795, anchor=CENTER)
    btn_exit = Button(window,text='Exit',width=27,command= lambda : exit())
    btn_exit.place(relx=0.5, rely=0.89, anchor=CENTER)
    window.mainloop()

def desk(fp):
    '''
    ###############################

    this function is the second page of program
    contained database tools

    ###############################
    '''

    def combobx():
        '''
    ###############################

    combobox configuraion function

    ###############################
        '''
        table = combo.get()
        sctext.delete(1.0,END)
        sctext.insert(INSERT,tabulate(db.selectAll(table)) + '\n')

    def execute():
        '''
    ###############################

    this function will get user sqlite command and
    check if its correct or not

    ###############################
        '''
        input_sql = inp.get()
        print(input_sql)
        if input_sql == '':
             messagebox.showerror('the input is empty !', 'please fill the input box and try again')
        try:
            db.execute_manuall(input_sql)
        except  sql.Error as error:
            print(error)
            messagebox.showerror('Wrong Command', 'wrong command executed try again !\nerror info : {}'.format(error))
        tables = get_tables(db)
        combo['values']= tables
        combo.current(0)
        combo.update()
         

    def Clear():
        inp.delete(0,END)
        inp.update()

    db = sqlite(fp[0])
    tables = get_tables(db)
    window = Tk()
    pageDesign(window,520,420)
    lbl=Label(window,text='choose the table that you want to browse :',font=('Times' , '11','italic'),fg='#17202a',bg='#DCDCDC')
    lbl.place(relx=0.01, rely=0.03 , anchor=NW)
    combo = ttk.Combobox(window,width=23)
    combo['values']= tables
    if len(tables) != 0 :
        combo.current(0)
    combo.place(relx=0.54, rely=0.03 , anchor=NW)
    sctext = scrolledtext.ScrolledText(window,height=17,width=55)
    sctext.place(relx=0.485 , rely=0.45 ,anchor=CENTER)
    inp = Entry(window,width=37)
    inp.place(relx=0.3305, rely=0.85, anchor=CENTER)
    btn_execute = Button(window,text='Execute',width=8,command=execute)
    btn_execute.place(relx=0.72, rely=0.85, anchor=CENTER)
    btn_clear = Button(window,text='Clear',width=8,command=Clear)
    btn_clear.place(relx=0.88, rely=0.85, anchor=CENTER)
    btn_exit = Button(window,text='Exit',width=15,command= lambda : exit())
    btn_exit.place(relx=0.67, rely=0.94, anchor=CENTER)
    btn_browse = Button(window,text='Browse',width=15,command= combobx)
    btn_browse.place(relx=0.33, rely=0.94, anchor=CENTER)
    window.mainloop()
    

main()
