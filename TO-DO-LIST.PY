from tkinter import *
from tkinter import messagebox
import sqlite3 as sql 

def add_task():
    task_string = task_filed.get()
    if len (task_string) == 0:
        messagebox.showinfo('error','filed is empty.')
    else :
        tasks.append(task_string)
        the_cursor.execute('insert into tasks values (?)',(task_string,))
        list_update()
        task_filed .delete(0,'end')

def list_update():
    clear_list()
    for task in tasks :
        task_listbox.insert('end',task)

def delete_task():    
    try :
        the_value = task_listbox.get(task_listbox.curselection())
        if the_value in tasks:
            tasks.remove(the_value)    
            list_update()
            the_cursor.execute('delete from tasks where title = ?',(the_value,))
    except : 
        messagebox.showinfo('error','no task selected. cannot delete.')

def delete_all_task():
    message_box = messagebox.askyesno('delete all','are you sure?')
    if messagebox == True:
        while(len(tasks) !=0):
            tasks.pop()
        the_cursor.execute('delete from tasks')
        list_update()

def clear_list():
    task_listbox.delete(0,'end')

def close():
    print(tasks)
    guiwindow.destroy()

def retrieve_database():
    while(len(tasks)!=0):
        tasks.pop()
    for row in the_cursor.execute('select title from tasks '):
        tasks.append(row[0])

if __name__ == "__main__":
    guiwindow = Tk()
    guiwindow.title("To-Do List")
    guiwindow.geometry("665x400+550+250")
    guiwindow.resizable(0,0)
    guiwindow.configure(bg = "#B5E5CF")

    the_connection = sql.connect('listofTasks.db')
    the_cursor = the_connection.cursor()
    the_cursor.execute('create table if not exists tasks (title text)')

    tasks = []

    function_frame = Frame(guiwindow, bg = "#8EE5EE")

    function_frame.pack(side = "top", expand = True , fill = "both")
    
    task_label = Label (function_frame,text="TO-DO-LIST\n  Enter the Task Title:",
                        font =("airal","14","bold "),
                        background = "#8EE5EE",
                        foreground="#FF6103"
    )
    task_label.place(x=20,y=30 )

    task_filed = Entry( 
        function_frame,
        font =("Arial","14"),
        width = 42,
        foreground="black",
        background = "white",
    )
    task_filed.place(x=180, y=30)

    add_button = Button (  
        function_frame,
        text = "Add",
           width = 15 ,
           bg='#D4AC0D', font=("arial","14","bold"),
           command = add_task,

                 )
    del_button = Button(
        function_frame,
        text = "Remove",
        width = 15,
        bg= '#D4AC0D', font=("arial","14","bold"),
        command = delete_task,
    )
    del_all_button = Button(
      function_frame,
      text = "Delete All ",
      width = 15,
      font=("arial","14","bold"),
        bg='#D4AC0D',
        command = delete_all_task
    )

exit_button = Button(
    function_frame,
    text ="exit/close",
    width = 52,
    bg='#D4AC0D',font=("arial","14","bold"),
    command = close
    )
add_button.place(x = 18 , y = 80 )
del_button.place(x = 240 , y = 80 )
del_all_button.place(x = 460 , y = 80)
exit_button.place(x = 17 , y = 330 )

task_listbox = Listbox(
    function_frame,
    width = 70,
    height=9,
    font="bold",
selectmode='SINGLE',
background="WHITE",
foreground="BLACK",
selectbackground= "#FF8C00",
selectforeground="BLACK"
)
task_listbox.place(x = 17 , y = 140)

retrieve_database()
list_update()
guiwindow.mainloop()
the_connection.commit()
the_cursor.close()