from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3

root = Tk()
root.title('CRM - Gestor de clientes')

# creamos conexión con bbdd
conn = sqlite3.connect('crm.db')
c = conn.cursor()

# creamos tabla en bbdd, la última línea no lleva coma al final
c.execute("""
    CREATE TABLE if not exists cliente (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        telefono TEXT NOT NULL,
        empresa TEXT NOT NULL
    );
""")

# aquí vamos colocando las funciones a medida que las vamos necesitando
def insertar(cliente):
    c.execute("""
        INSERT INTO cliente (nombre, telefono, empresa) VALUES (?, ?, ?)
    """, (cliente['nombre'], cliente['telefono'], cliente['empresa']))
    conn.commit()

def render_clientes():
    # función para actualizar la vista de la tabla
    # eliminamos todo y después se vuelve a pintar
    tree.delete(*tree.get_children())
    rows = c.execute("SELECT * FROM cliente").fetchall()
    for row in rows:
        tree.insert('', END, row[0], values=(row[1], row[2], row[3]))
        

def nuevo_cliente():
    # abrir nueva ventana
    # construir interfaz de la nuevc ventama
    # incluimos la función guardar cliente aquí porque si lo hacemos fuera habría que definir las variables como globales y como su uso va a estar limitado a este scope, no merece la pena
    # colocamos el mainloop a la ventana para que se quede escuhando
    

    def guardar_cliente():
        # creamos un diccionario de nuestro cliente
        # agregar validación para que los entry NO estén vacíos
        # llamamos a función que inserta registro en bbdd
        # cerramos ventana
        if not nombre.get():
            messagebox.showerror('Error', 'El nombre es obligatorio')
            # cortamos la función para que no continúe ejecutando el resto de cosas ya que no ha pasado la validación. Lo hacemos con un return
            return
        if not telefono.get():
            messagebox.showerror('Error', 'El teléfono es obligatorio')
            # cortamos la función para que no continúe ejecutando el resto de cosas ya que no ha pasado la validación. Lo hacemos con un return
            return
        if not empresa.get():
            messagebox.showerror('Error', 'La empresa es obligatoria')
            # cortamos la función para que no continúe ejecutando el resto de cosas ya que no ha pasado la validación. Lo hacemos con un return
            return

        cliente = {
            'nombre': nombre.get(),
            'telefono': telefono.get(),
            'empresa': empresa.get()
        }
        insertar(cliente)
        render_clientes()
        top.destroy()

    top = Toplevel()
    top.title('Nuevo cliente')

    lnombre = Label(top, text='Nombre')
    nombre = Entry(top, width=40)
    lnombre.grid(row=0, column=0)
    nombre.grid(row=0, column=1)

    ltelefono = Label(top, text='Teléfono')
    telefono = Entry(top, width=40)
    ltelefono.grid(row=1, column=0)
    telefono.grid(row=1, column=1)

    lempresa = Label(top, text='Empresa')
    empresa = Entry(top, width=40)
    lempresa.grid(row=2, column=0)
    empresa.grid(row=2, column=1)

    guardar = Button(top, text='Guardar', command=guardar_cliente)
    guardar.grid(row=3, column=1)

    top.mainloop()

def eliminar_cliente():
    # saber qué elemento está seleccionado para eliminar
    # seleccionamos el id del primer elemento en caso de que hubiera varios
    # agregamos validación, pregunta de seguridad
    id = tree.selection()[0]
    cliente = c.execute("SELECT * FROM cliente WHERE id = ?", (id, )).fetchone()
    respuesta = messagebox.askokcancel('Estás seguro?', '¿Quieres eliminar el cliente ' + cliente[1] + ' ?')
    if respuesta:
        c.execute("DELETE FROM cliente WHERE id = ?", (id, ))
        conn.commit()
        render_clientes()
    else:
        pass

# cremamos elementos de la interfaz y empezamos a asignar comportamiento a cada uno de ellos
# botones
btn = Button(root, text='Nuevo cliente', command=nuevo_cliente)
btn.grid(column=0, row=0)

btn_eliminar = Button(root, text='Eliminar cliente', command=eliminar_cliente)
btn_eliminar.grid(column=1, row=0)

# creamos nuestro arbol (ocultamos directamente columna #0)
tree = ttk.Treeview(root)
tree['columns'] = ('Nombre', 'Teléfono', 'Empresa')
tree.column('#0', width=0, stretch=NO)
tree.column('Nombre')
tree.column('Teléfono')
tree.column('Empresa')
tree.heading('Nombre', text='Nombre')
tree.heading('Teléfono', text='Teléfono')
tree.heading('Empresa', text='Empresa')
tree.grid(column=0, row=1, columnspan=2)

render_clientes()
root.mainloop()