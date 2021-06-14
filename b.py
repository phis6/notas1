import sqlite3
from tkinter import *
from tkinter import messagebox


#Professor, me desculpe mas tive alguns problemas com as validações dos tipos de dados(a validação de campos vazios funciona).


def connect():
    conn = sqlite3.connect("trab/notas.db")
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS notas (id INTEGER PRIMARY KEY, materia TEXT, nota1 INTEGER, nota2 INTEGER, nota3 INTEGER)")
    conn.commit()
    conn.close()


def insert(materia, nota1, nota2, nota3):
    conn = sqlite3.connect("trab/notas.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO notas VALUES (NULL,?,?,?,?)",
                (materia, nota1, nota2, nota3))
    conn.commit()
    conn.close()
    view()


def view():
    conn = sqlite3.connect("trab/notas.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM notas")
    rows = cur.fetchall()
    conn.close()
    return rows


def search(materia="", nota1="", nota2="", nota3=""):
    conn = sqlite3.connect("trab/notas.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM notas WHERE materia=? OR nota1=? OR nota2=? OR nota3=?",
                (materia, nota1, nota2, nota3))
    rows = cur.fetchall()
    conn.close()
    return rows


def delete(id):
    conn = sqlite3.connect("trab/notas.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM notas WHERE id=?", (id,))
    conn.commit()
    conn.close()


def update(id, materia, nota1, nota2, nota3):
    conn = sqlite3.connect("trab/notas.db")
    cur = conn.cursor()
    cur.execute("UPDATE notas SET materia=?, nota1=?, nota2=?, nota3=? WHERE id=?",
                (materia, nota1, nota2, nota3, id))
    conn.commit()
    conn.close()


def Lint2():
    ok = False
    valor = 0
    while True:
        n = e2.get()
        if n.isnumeric():
            valor = int(n)
            ok = True
        else:
            messagebox.showinfo("ERRO! NOTA 1", "Digite o tipo certo.")
            break
        
def Lint3():
    ok = False
    valor = 0
    while True:
        n = e3.get()
        if n.isnumeric():
            valor = int(n)
            ok = True
        else:
            messagebox.showinfo("ERRO! NOTA 2", "Digite o tipo certo.")
            break    

def Lint4():
    ok = False
    valor = 0
    while True:
        n = e4.get()
        if n.isnumeric():
            valor = int(n)
            ok = True
        else:
            messagebox.showinfo("ERRO! NOTA 3", "Digite o tipo certo.")
            break
        
connect()

selected_tuple = 'none'

def get_selected_row(event):
    global selected_tuple
    index = list1.curselection()[0]
    selected_tuple = list1.get(index)
    e1.delete(0, END)
    e1.insert(END, selected_tuple[1])
    e2.delete(0, END)
    e2.insert(END, selected_tuple[2])
    e3.delete(0, END)
    e3.insert(END, selected_tuple[3])
    e4.delete(0, END)
    e4.insert(END, selected_tuple[4])

def view_command():
    list1.delete(0, END)
    for row in view():
        list1.insert(END, row)

def add_command():
    if e1.get() == "" or e2.get() == "" or e3.get() == "" or e4.get() == "":
        messagebox.showinfo("Digite Algo", "Você deixou campos em branco.")
    else:
        insert(materia.get(), nota1.get(), nota2.get(), nota3.get())
        list1.delete(0, END)
        list1.insert(END, (materia.get(), nota1.get(), nota2.get(), nota3.get()))
        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        e4.delete(0, END)
        view_command()

def delete_command():
    delete(selected_tuple[0])
    e1.delete(0, END)
    e2.delete(0, END)
    e3.delete(0, END)
    e4.delete(0, END)
    view_command()

def update_command():
    update(selected_tuple[0], materia.get(), nota1.get(), nota2.get(), nota3.get())
    e1.delete(0, END)
    e2.delete(0, END)
    e3.delete(0, END)
    e4.delete(0, END)
    view_command()

root = Tk()
root.title("NOTAS")
root.geometry("700x270")
root.resizable(False, False)
root.config(bg='light salmon')


l1 = Label(root, text="Materia", bg='light salmon', fg='#660033')
l1.grid(row=0, column=0)
l2 = Label(root, text="AV1", bg='light salmon', fg='#660033')
l2.grid(row=1, column=0)
l3 = Label(root, text="AV2", bg='light salmon', fg='#660033')
l3.grid(row=2, column=0)
l4 = Label(root, text="AVD", bg='light salmon', fg='#660033')
l4.grid(row=3, column=0)

materia = StringVar()
e1 = Entry(root, textvariable=materia)
e1.grid(row=0, column=1)
nota1 = StringVar()
e2 = Entry(root, textvariable=nota1)
e2.grid(row=1, column=1)
nota2 = StringVar()
e3 = Entry(root, textvariable=nota2)
e3.grid(row=2, column=1)
nota3 = StringVar()
e4 = Entry(root, textvariable=nota3)
e4.grid(row=3, column=1)

list1 = Listbox(root, height=8, width=55)
list1.grid(row=6, column=0, rowspan=6, columnspan=2)

sb1 = Scrollbar(root)
sb1.grid(row=6, column=2, rowspan=6)

list1.configure(yscrollcommand=sb1.set)
sb1.configure(command=list1.yview)


list1.bind('<<ListboxSelect>>', get_selected_row)

b1 = Button(root, text="Exibir todos", width=22,
            bg="#66b3ff", command=view_command)
b1.grid(row=6, column=4)

b3 = Button(root, text="Incluir", width=22, bg="#bbff99", command=lambda:[add_command(), Lint2(), Lint3(), Lint4()])
b3.grid(row=5, column=4)

b4 = Button(root, text="Atualizar Selecionado",
            width=22, bg="#66b3ff", command=update_command)
b4.grid(row=5, column=5)

b5 = Button(root, text="Deletar Selecionado",
            bg="#ff6633", width=22, command=delete_command)
b5.grid(row=6, column=5)

b6 = Button(root, text="Fechar", width=22, bg="#d9d9d9", command=root.destroy)
b6.grid(row=8, column=5)

root.mainloop()