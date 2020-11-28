# -*- coding: utf-8 -*-
"""
Integrantes:

    Moisés Díaz Pérez (2019-1864)
    Karen Arias Torres (2019-2365)
    Isaí Vargas Antigua (2020-0472)
    Marlon Peña Peña (2020-0703)
    Cindy Ecker Aybar (2020-0872)
"""

from tkinter import * 
import sqlite3
import tkinter.messagebox
from tkinter import ttk 
import datetime
import requests
import json

class Utilitarios:
    @staticmethod
    def generarTreeview(frame, headers, datos, *metodos):

        
        
        trv = ttk.Treeview(frame, columns=(tuple((i+1) for i in range(len(headers)))), show="headings")
        trv.bind('<ButtonRelease-1>', lambda event, arg=trv: metodos[0](event, arg)) #metodo para obtener datos de row seleccionadoo
        #scrollbar
        #vsb = ttk.Scrollbar(frame, orient="vertical", command=trv.yview)
        #vsb.pack(side='right', fill='y')
        
        for i in range(len(headers)):
            trv.heading(i+1, text=f"{headers[i][0]}")
        
        for d in datos:
            trv.insert('', 'end', values=d)
        trv.pack(fill="x")
    
    
        
    def generarTabla(frame, datosTabla, tablaHeader, *metodos): #genera las tablas con sus datos
        #tabla
        frame = frame
        for fila in range(len(datosTabla)+1):
            for columna in range(len(datosTabla[0])):
                if fila == 0: #para crear los headers
                    label = Label(frame, text=f"{tablaHeader[columna][fila]}", bg="white", fg="black")
                    
                    label.grid(row=fila, column=columna, sticky="nsew", padx=1, pady=1)
                    frame.grid_columnconfigure(columna, weight=1)
                    
                else:
                    
                    label = Label(frame, text=f"{datosTabla[fila-1][columna]}", bg="light grey")
                    
                    label.grid(row=fila, column=columna, sticky="nsew", padx=1, pady=1)
                    frame.grid_columnconfigure(columna, weight=1)
                    
                    if (columna == len(datosTabla[0]) - 1): #seccion de acciones
                        if (len(metodos) == 2): #tablas en las que hay que editar y borrar
                            botonEditar = Button(frame, text="editar",bg="yellow")
                            botonEditar.grid(row=fila, column=columna+1, sticky="nsew", padx=1, pady=1)
                            
                            #valor del campo identificador
                            columnaId = frame.grid_slaves(row=botonEditar.grid_info()["row"], column=0)[0]
                            txtColumnaId = columnaId.cget("text")
                            
                            botonEditar["command"] = lambda id = txtColumnaId : metodos[0](id)
                            
                            botonBorrar = Button(frame, text="borrar",bg="red")
                            botonBorrar.grid(row=fila, column=columna+2, sticky="nsew", padx=1, pady=1)
                            botonBorrar["command"] = lambda id = txtColumnaId : metodos[1](id)
                            
                            frame.grid_columnconfigure(columna, weight=1)
                        else: #en caso de que sea la tabla de generar html
                            botonGenerar = Button(frame, text="Generar HTML",bg="white")
                            botonGenerar.grid(row=fila, column=columna+1, sticky="nsew", padx=1, pady=1)
                            
                            #valor del campo identificador
                            columnaId = frame.grid_slaves(row=botonGenerar.grid_info()["row"], column=0)[0]
                            txtColumnaId = columnaId .cget("text")
                            
                            botonGenerar["command"] = lambda id = txtColumnaId : metodos[0](id)
                            
                            frame.grid_columnconfigure(columna, weight=1)
                            
            
        return frame
                        
class GestionEstudiantes:
    
    def __init__(self):
        
        self.connection = sqlite3.connect("bdPractica4")
        self.cursorSql = self.connection.cursor()
        
        self.top = Toplevel()
        self.top.grab_set()
        self.top.title("Gestion estudiantes")
        self.top.geometry("940x640")
        
        self.wrapper1 = LabelFrame(self.top, text="Datos estudiante")
        self.wrapper2 = LabelFrame(self.top, text="Tabla")
        
        #datos estudiantes
        self.frameEstudiante = Frame(self.wrapper1, padx=10)
        self.frameEstudiante.pack(side = LEFT)
        
        
        self.labelNombre = Label(self.frameEstudiante, text="Nombre del estudiante")
        self.labelNombre.pack()
        
        
        self.textBoxNombre = Entry(self.frameEstudiante, width=30)
        self.textBoxNombre.pack()
        
        self.labelApellido = Label(self.frameEstudiante, text="Apellido del estudiante")
        self.labelApellido.pack()
        
        self.textBoxApellido = Entry(self.frameEstudiante, width=30)
        self.textBoxApellido.pack()
        
        self.labelCedula = Label(self.frameEstudiante, text="Cedula del estudiante")
        self.labelCedula.pack()
        
        self.textBoxCedula = Entry(self.frameEstudiante, width=30)
        self.textBoxCedula.pack()
        
        
        self.labelSexo = Label(self.frameEstudiante, text="Sexo")
        self.labelSexo.pack()
        
        #radio buttons
        self.sexo = StringVar(value="M")
        self.rMasculino = Radiobutton(self.frameEstudiante, text="Masculino", variable=self.sexo, value="M")
        self.rMasculino.pack()
        self.rFemenino = Radiobutton(self.frameEstudiante, text="Femenino", variable=self.sexo, value="F")
        self.rFemenino.pack()
        
        #comboxes
        self.labelComboBoxCarrera = Label(self.frameEstudiante, text="Carrera del estudiante:")
        self.labelComboBoxCarrera.pack()
        
        self.comboBoxCarrera = ttk.Combobox(self.frameEstudiante, width = 27,state="readonly")
        self.comboBoxCarrera.pack()
        
        self.labelComboBoxProvincia = Label(self.frameEstudiante, text="Provincia del estudiante:")
        self.labelComboBoxProvincia.pack()
        
        self.comboBoxProvincia = ttk.Combobox(self.frameEstudiante, width = 27,state="readonly")
        self.comboBoxProvincia.pack()
        
        #matricula del estudiante seleccionado
        self.matEstudianteSeleccionado = 0

        #botones
        self.botonAgregarEstudiante = Button(self.frameEstudiante,text="Agregar➕",command= self.agregarEstudiante)
        self.botonAgregarEstudiante.pack(side = LEFT)
        
        self.botonModificarEstudiante = Button(self.frameEstudiante,text="Modificar",command= self.modificarEstudiante)
        self.botonModificarEstudiante.pack(side = LEFT)
        
        self.botonEliminarEstudiante = Button(self.frameEstudiante,text="Eliminar−",command= self.eliminarEstudiante)
        self.botonEliminarEstudiante.pack(side = LEFT)
        
        
        #datos estudiante API
        self.frameEstudianteUrl = Frame(self.wrapper1, padx=10)
        self.frameEstudianteUrl.pack()
        
        self.labelApiEstudiante = Label(self.frameEstudianteUrl, text="AGREGAR ESTUDIANTE POR API [digite la cedula del estudiante]")
        self.labelApiEstudiante.pack(side = TOP)
        
        self.textBoxApiEstudiante = Entry(self.frameEstudianteUrl, width=30)
        self.textBoxApiEstudiante.pack(side = TOP)
        
        #botones
        self.botonAgregarEstudianteUrl = Button(self.frameEstudianteUrl,text="Agregar por API➕",command= self.agregarEstudiantePorApi)
        self.botonAgregarEstudianteUrl.pack()
        
        #coneccion a tabla estudiantes
        self.estudiantes = []
        self.headerEstudiantes = []
        try:
            #agregamos los datos a los comboboxes
            self.cursorSql.execute("select Id, Nombre from Carrera")
            self.listaDeCarreras = self.cursorSql.fetchall()
            self.comboBoxCarrera["values"] = self.listaDeCarreras
            self.comboBoxCarrera.current(0) #para que seleccione al primero por default
            
            self.cursorSql.execute("select Id, Nombre from Provincia")
            self.listaDeProvincias = self.cursorSql.fetchall()
            self.comboBoxProvincia["values"] = self.listaDeProvincias
            self.comboBoxProvincia.current(0) #para que seleccione al primero por default
            
            self.cursorSql.execute('''
                                   select Matricula, Estudiantes.Nombre, Apellido, Cedula, Sexo, 
                                   Carrera.Nombre as "Carrera", Provincia.Nombre as "Provincia" from Estudiantes 
                                   INNER JOIN Carrera on Estudiantes.IdCarrera = Carrera.Id  INNER JOIN Provincia 
                                   on Estudiantes.IdProvincia = Provincia.Id
                                   ''')
            
            self.headerEstudiantes = self.cursorSql.description #header
            self.estudiantes = self.cursorSql.fetchall() #datos estudiantes
            
        except:
            tkinter.messagebox.showerror(title="Error",message="Ups! error al conectar")
        
        
        #tabla de datos - treeview
        Utilitarios.generarTreeview(self.wrapper2, self.headerEstudiantes, self.estudiantes, self.obtenerDatos)
        
        self.wrapper1.pack(fill="both", expand="yes", padx=10, pady=10)
        self.wrapper2.pack(fill="both", expand="yes", padx=10, pady=10)
        
    #metodo donde se obtiene los datos del row seleccionado seleccionada
    def obtenerDatos(self, event, tree):
        seleccion = tree.item(tree.focus())
        print(seleccion["values"])
        
        #matricula del estudiante seleccionado
        self.matEstudianteSeleccionado = seleccion["values"][0]
            
        #seteamos el textBox
        self.textBoxNombre.delete(0,END) 
        self.textBoxNombre.insert(END, seleccion["values"][1])
        self.textBoxApellido.delete(0,END) 
        self.textBoxApellido.insert(END, seleccion["values"][2])
        self.textBoxCedula.delete(0,END) 
        self.textBoxCedula.insert(END, str(seleccion["values"][3]))
        
        #seteamos el radiobutton
        self.sexo.set(seleccion["values"][4])
        
        #seteamos los combobox
        nuevoValorCarrera = ""
        for i in range(len(self.listaDeCarreras)):
            if self.listaDeCarreras[i][1] == seleccion["values"][5]:
                nuevoValorCarrera = self.listaDeCarreras[i]            
        self.comboBoxCarrera.set(nuevoValorCarrera)
            
        nuevoValorProvincia = ""
        for i in range(len(self.listaDeProvincias)):
            if self.listaDeProvincias[i][1] == seleccion["values"][6]:
                nuevoValorProvincia = self.listaDeProvincias[i]
        self.comboBoxProvincia.set(nuevoValorProvincia)
        
        
    def agregarEstudiante(self):
        if (self.textBoxNombre.get() and self.textBoxNombre.get().strip() 
            and self.textBoxApellido.get() and self.textBoxApellido.get().strip() 
            and self.textBoxCedula.get() and self.textBoxCedula.get().strip()):
            try:
                self.cursorSql.execute(f"INSERT INTO Estudiantes VALUES(null, '{self.textBoxNombre.get()}', '{self.textBoxApellido.get()}', '{self.textBoxCedula.get()}', '{self.sexo.get()}', {self.comboBoxCarrera.get().split(' ')[0]}, {self.comboBoxProvincia.get().split(' ')[0]})")
                self.connection.commit()
                tkinter.messagebox.showinfo("Listo!", "Se ha agregado el estudiante")
                self.actualizarVentana()
            except Exception as e:
                print(e)
                tkinter.messagebox.showerror(title="Error",message="Ups! no se pudo agregar a la base de datos")
        else:
            tkinter.messagebox.showerror(title="Error",message="Ups! no se pudo agregar a la base de datos [debe agregar valores]")
            
                
    def agregarEstudiantePorApi(self):
        info = requests.get(f"https://api.adamix.net/apec/cedula/{self.textBoxApiEstudiante.get()}")
        data = json.loads(info.text)
        try:
            if data["ok"] == True:#agrega un estudiante nuevo
                print(data["Nombres"])
                self.cursorSql.execute(f"INSERT INTO Estudiantes VALUES(null, '{data['Nombres']}', '{data['Apellido1']}', '{data['Cedula']}', '{data['IdSexo']}', {self.comboBoxCarrera.get().split(' ')[0]}, {self.comboBoxProvincia.get().split(' ')[0]})")
                self.connection.commit()
                tkinter.messagebox.showinfo("Listo!", "Se ha agregado el estudiante")
                self.actualizarVentana()
                                
            else: #No se pudo agregar un estudiante nuevo
                 tkinter.messagebox.showerror(title="Error",message="Ups! no se encontro un estudiante con esta cedula")
                    

            #self.actualizarVentana()
        except:
             tkinter.messagebox.showerror(title="Error",message="Ups! no se pudo agregar a la base de datos")
                    
    
    def modificarEstudiante(self):
        if self.matEstudianteSeleccionado != 0:
            try:
                self.cursorSql.execute(f"UPDATE Estudiantes set Nombre = '{self.textBoxNombre.get()}', Apellido = '{self.textBoxApellido.get()}', Cedula = '{self.textBoxCedula.get()}', Sexo = '{self.sexo.get()}', IdCarrera = {self.comboBoxCarrera.get().split(' ')[0]}, IdProvincia = {self.comboBoxProvincia.get().split(' ')[0]}  WHERE Matricula = {self.matEstudianteSeleccionado}")
                self.connection.commit()
                tkinter.messagebox.showinfo("Listo!", "Se ha modificado el estudiante")
                self.actualizarVentana()
            except:
                 tkinter.messagebox.showerror(title="Error",message="Ups! no se pudo modificar de la base de datos")
        else:
            tkinter.messagebox.showerror(title="Error",message="Ups! no se pudo modificar de la base de datos [debe seleccionar]")
        
    def eliminarEstudiante(self):
        if self.matEstudianteSeleccionado != 0:
            try:
                self.cursorSql.execute(f"DELETE from Estudiantes WHERE Matricula = {self.matEstudianteSeleccionado}")
                self.connection.commit()
                tkinter.messagebox.showinfo("Listo!", "Se ha borrado el estudiante")
                self.actualizarVentana()
            except:
                 tkinter.messagebox.showerror(title="Error",message="Ups! no se pudo eliminar de la base de datos")
        else:
            tkinter.messagebox.showerror(title="Error",message="Ups! no se pudo eliminar de la base de datos [debe seleccionar]")
           
    #actualiza la ventana
    def actualizarVentana(self):
        self.top.destroy()
        self.__init__()
        
        

class GestionCarreras:
    
    def __init__(self):
        
        self.connection = sqlite3.connect("bdPractica4")
        self.cursorSql = self.connection.cursor()
        
        #coneccion a tabla estudiantes
        self.carreras = []
        self.headerCarreras = []
        try:
            
            self.cursorSql.execute("SELECT * FROM Carrera")
            
            self.headerCarreras = self.cursorSql.description #header
            self.carreras = self.cursorSql.fetchall() #datos
            
        except:
            tkinter.messagebox.showerror(title="Error",message="Ups! error al conectar")
        
        self.top = Toplevel()
        self.top.grab_set()
        self.top.title("Gestion carreras")
        self.top.geometry("740x440")
        
        self.wrapper1 = LabelFrame(self.top, text="Datos carrera")
        self.wrapper2 = LabelFrame(self.top, text="Tabla")
        
        #datos carrera
        self.frameCarrera = Frame(self.wrapper1, padx=10)
        self.frameCarrera.pack()
        
        
        self.labelCarrera = Label(self.frameCarrera, text="Nombre de la carrera")
        self.labelCarrera.pack()
        
        
        self.textBoxCarrera = Entry(self.frameCarrera, width=30)
        self.textBoxCarrera.pack(padx=10,pady=10)
        
                        
        #id carrera seleccionada
        self.idCarreraSeleccionada = 0

        #botones
        self.botonAgregarCarrera = Button(self.frameCarrera,text="Agregar➕",command= self.agregarCarrera)
        self.botonAgregarCarrera.pack(side = LEFT)
        
        self.botonModificarCarrera = Button(self.frameCarrera,text="Modificar",command= self.modificarCarrera)
        self.botonModificarCarrera.pack(side = LEFT)
        
        self.botonEliminarCarrera = Button(self.frameCarrera,text="Eliminar−",command= self.eliminarCarrera)
        self.botonEliminarCarrera.pack(side = LEFT)
        
        
        
        
        #tabla de datos - treeview
        Utilitarios.generarTreeview(self.wrapper2, self.headerCarreras, self.carreras, self.obtenerDatos)
        
        self.wrapper1.pack(fill="both", expand="yes", padx=10, pady=10)
        self.wrapper2.pack(fill="both", expand="yes", padx=10, pady=10)
        
    #metodo donde se obtiene los datos del row seleccionado seleccionada
    def obtenerDatos(self, event, tree):
        seleccion = tree.item(tree.focus())
        print(seleccion["values"])
        
        #matricula del estudiante seleccionado
        self.idCarreraSeleccionada = seleccion["values"][0]
            
        #seteamos el textBox
        self.textBoxCarrera.delete(0,END) 
        self.textBoxCarrera.insert(END, seleccion["values"][1])
        
        
    def agregarCarrera(self):
        print("agregando")
        if self.textBoxCarrera.get() and self.textBoxCarrera.get().strip():
            try:
                self.cursorSql.execute(f"INSERT INTO Carrera VALUES(null, '{self.textBoxCarrera.get()}')")
                self.connection.commit()
                tkinter.messagebox.showinfo("Listo!", "Se ha agregado la carrera")
                self.actualizarVentana()
            except:
                 tkinter.messagebox.showerror(title="Error",message="Ups! no se pudo agregar a la base de datos")
        else:
            tkinter.messagebox.showerror(title="Error",message="Ups! no se pudo agregar a la base de datos [debe ingresar valores]")
                
    
    def modificarCarrera(self):
        if self.idCarreraSeleccionada != 0:
            try:
                self.cursorSql.execute(f"UPDATE Carrera set Nombre = '{self.textBoxCarrera.get()}'   WHERE Id = {self.idCarreraSeleccionada}")
                self.connection.commit()
                tkinter.messagebox.showinfo("Listo!", "Se ha modificado la carrera")
                self.actualizarVentana()
            except:
                 tkinter.messagebox.showerror(title="Error",message="Ups! no se pudo modificar de la base de datos")
        else:
            tkinter.messagebox.showerror(title="Error",message="Ups! no se pudo modificar de la base de datos [debe seleccionar valores]")
    
    def eliminarCarrera(self):
        if self.idCarreraSeleccionada != 0:
            try:
                self.cursorSql.execute(f"DELETE from Carrera WHERE Id = {self.idCarreraSeleccionada}")
                self.connection.commit()
                tkinter.messagebox.showinfo("Listo!", "Se ha borrado la carrera")
                self.actualizarVentana()
            except:
                 tkinter.messagebox.showerror(title="Error",message="Ups! no se pudo eliminar de la base de datos")
        else:
             tkinter.messagebox.showerror(title="Error",message="Ups! no se pudo eliminar de la base de datos [debe seleccionar valores]")
           
    #actualiza la ventana
    def actualizarVentana(self):
        self.top.destroy()
        self.__init__()
        
     




        
class GestionMaterias:
    def __init__(self):
        
        self.connection = sqlite3.connect("bdPractica4")
        self.cursorSql = self.connection.cursor()
                
        self.top = Toplevel()
        self.top.grab_set()
        self.top.title("Gestion materias")
        self.top.geometry("740x440")
        
        self.wrapper1 = LabelFrame(self.top, text="Datos materia")
        self.wrapper2 = LabelFrame(self.top, text="Tabla")
        
        #datos carrera
        self.frameMateria = Frame(self.wrapper1, padx=10)
        self.frameMateria.pack()
        
        self.label = Label(self.frameMateria, text="Nombre de la materia")
        self.label.pack()
        
        #textbox
        self.textBoxMateria = Entry(self.frameMateria , width=30)
        self.textBoxMateria.pack()
        
        #combox
        self.labelComboBoxCarrera = Label(self.frameMateria , text="Carrera a la que pertenece:")
        self.labelComboBoxCarrera.pack()
        
        self.comboBoxCarrera = ttk.Combobox(self.frameMateria, width = 27,state="readonly")
        self.comboBoxCarrera.pack()
        
        #botones
        self.botonAgregarEstudiante = Button(self.frameMateria,text="Agregar➕",command= self.agregarMateria)
        self.botonAgregarEstudiante.pack(side = LEFT)
        
        self.botonModificarEstudiante = Button(self.frameMateria,text="Modificar",command= self.modificarMateria)
        self.botonModificarEstudiante.pack(side = LEFT)
        
        self.botonEliminarEstudiante = Button(self.frameMateria,text="Eliminar−",command= self.eliminarMateria)
        self.botonEliminarEstudiante.pack(side = LEFT)
        
        #id de la materia seleccionada
        self.idMateriaAEditar = 0
        
        #coneccion a tabla materias
        self.materias = []
        self.headerMaterias = []
        try:
            
            self.cursorSql.execute("SELECT Materia.Id, Materia.NombreMateria, Carrera.Nombre as 'Carrera a la que pertenece' FROM Materia inner join Carrera  on Materia.IdCarrera = Carrera.Id")
            
            self.headerMaterias = self.cursorSql.description #header
            self.materias = self.cursorSql.fetchall() #datos materias
            
            self.cursorSql.execute("select Id, Nombre from Carrera")
            self.listaDeCarreras = self.cursorSql.fetchall()
            self.comboBoxCarrera["values"] = self.listaDeCarreras
            self.comboBoxCarrera.current(0) #para que seleccione al primero por default
            
        except:
            tkinter.messagebox.showerror(title="Error",message="Ups! error al conectar")

        
        #tabla de datos - treeview
        Utilitarios.generarTreeview(self.wrapper2, self.headerMaterias, self.materias, self.obtenerDatos)
        
        
        self.wrapper1.pack(fill="both", expand="yes", padx=10, pady=10)
        self.wrapper2.pack(fill="both", expand="yes", padx=10, pady=10)
        
        
    #metodo donde se obtiene los datos del row seleccionado seleccionada
    def obtenerDatos(self, event, tree):
        seleccion = tree.item(tree.focus())
        print(seleccion["values"])
        
        #matricula del estudiante seleccionado
        self.idMateriaAEditar = seleccion["values"][0]
            
        #seteamos el textBox
        self.textBoxMateria.delete(0,END) 
        self.textBoxMateria.insert(END, seleccion["values"][1])
        
        #seteamos los combobox
        nuevoValorCarrera = ""
        for i in range(len(self.listaDeCarreras)):
            if self.listaDeCarreras[i][1] == seleccion["values"][2]:
                nuevoValorCarrera = self.listaDeCarreras[i]            
        self.comboBoxCarrera.set(nuevoValorCarrera)
        
    #actualiza la ventana
    def actualizarVentana(self):
        self.top.destroy()
        self.__init__()
        
    def agregarMateria(self):
        if self.textBoxMateria.get() and self.textBoxMateria.get().strip():
            try:
                
                self.cursorSql.execute(f"INSERT INTO Materia VALUES(null, '{self.textBoxMateria.get()} ', {self.comboBoxCarrera.get().split(' ')[0]})")
                self.connection.commit()
                tkinter.messagebox.showinfo("Listo!", "Se ha agregado la materia")
                self.actualizarVentana()
            except:
                 tkinter.messagebox.showerror(title="Error",message="Ups! no se pudo agregar a la base de datos")
        else:
            tkinter.messagebox.showerror(title="Error",message="Ups! no se pudo agregar a la base de datos [debe agregar valores]")
    
    def modificarMateria(self):
        if self.idMateriaAEditar != 0:
            try:
                self.cursorSql.execute(f"UPDATE Materia set NombreMateria = '{self.textBoxMateria.get()}',   IdCarrera = {self.comboBoxCarrera.get().split(' ')[0]}  WHERE Id = {self.idMateriaAEditar}")
                self.connection.commit()
                tkinter.messagebox.showinfo("Listo!", "Se ha modificado la materia")
                self.actualizarVentana()
            except Exception as e:
                print(e)
                tkinter.messagebox.showerror(title="Error",message="Ups! no se pudo modificar de la base de datos")
        else:
            tkinter.messagebox.showerror(title="Error",message="Ups! no se pudo modificar de la base de datos [debe seleccionar]")
        
        

    def eliminarMateria(self):
        if self.idMateriaAEditar != 0:
            try:
                self.cursorSql.execute(f"DELETE from Materia WHERE Id = {self.idMateriaAEditar}")
                self.connection.commit()
                tkinter.messagebox.showinfo("Listo!", "Se ha borrado la materia")
                self.actualizarVentana()
            except:
                 tkinter.messagebox.showerror(title="Error",message="Ups! no se pudo eliminar de la base de datos")
        else:
             tkinter.messagebox.showerror(title="Error",message="Ups! no se pudo eliminar de la base de datos [debe seleccionar valores]")
           
                
class GestionCalificaciones:
    
    def __init__(self):
        
        self.connection = sqlite3.connect("bdPractica4")
        self.cursorSql = self.connection.cursor()
        
        self.top = Toplevel()
        self.top.grab_set()
        self.top.title("Gestion de calificaciones [asignando las notas a los estudiantes por materiaaa]")
        self.top.geometry("940x440")
        
        self.wrapper1 = LabelFrame(self.top, text="Datos calificacion")
        self.wrapper2 = LabelFrame(self.top, text="Tabla")
        
        #comboxes
        self.label = Label(self.wrapper1, text="Nombre del estudiante:")
        self.label.pack()
        
        self.comboboxEstudiante = ttk.Combobox(self.wrapper1, width = 27,state="readonly")
        self.comboboxEstudiante.pack()
        
        self.label = Label(self.wrapper1, text="Nombre de la materia:")
        self.label.pack()
        
        self.comboboxMateria = ttk.Combobox(self.wrapper1, width = 27,state="readonly")
        self.comboboxMateria.pack()
        
        self.frameBotones1 = Frame(self.wrapper1)
        self.frameBotones1.pack()
        
        self.frameBotones2 = Frame(self.wrapper1)
        self.frameBotones2.pack()

        #secciones de notas
        self.label = Label(self.frameBotones1, text="Practica 1: ")
        self.label.grid(row=0, column=0, padx=3, pady=5)       
        self.textBoxPractica1 = Entry(self.frameBotones1, width=20)
        self.textBoxPractica1.grid(row=0, column=1, padx=3, pady=5)         
        self.label = Label(self.frameBotones1, text="Practica 2: ")
        self.label.grid(row=1, column=0, padx=3, pady=5) 
        self.textBoxPractica2 = Entry(self.frameBotones1, width=20)
        self.textBoxPractica2.grid(row=1, column=1, padx=3, pady=5)   
        
        self.label = Label(self.frameBotones1, text="Foro 1: ")
        self.label.grid(row=0, column=2, padx=3, pady=5) 
        self.textBoxForo1 = Entry(self.frameBotones1, width=20)
        self.textBoxForo1.grid(row=0, column=3, padx=3, pady=5)        
        self.label = Label(self.frameBotones1, text="Foro 2: ")
        self.label.grid(row=1, column=2, padx=3, pady=5) 
        self.textBoxForo2 = Entry(self.frameBotones1, width=20)
        self.textBoxForo2.grid(row=1, column=3, padx=3, pady=5) 
        
        self.label = Label(self.frameBotones1, text="Primer parcial: ")
        self.label.grid(row=0, column=4, padx=3, pady=5) 
        self.textBoxPrimerParcial = Entry(self.frameBotones1, width=20)
        self.textBoxPrimerParcial.grid(row=0, column=5, padx=3, pady=5)         
        self.label = Label(self.frameBotones1, text="Segundo parcial: ")
        self.label.grid(row=1, column=4, padx=3, pady=5) 
        self.textBoxSegundoParcial = Entry(self.frameBotones1, width=20)
        self.textBoxSegundoParcial.grid(row=1, column=5, padx=3, pady=5) 
        
        self.label = Label(self.frameBotones1, text="Examen final: ")
        self.label.grid(row=0, column=6, padx=3, pady=5)
        self.textBoxExamenFinal = Entry(self.frameBotones1, width=20)
        self.textBoxExamenFinal.grid(row=0, column=7, padx=3, pady=5)
        
        #botones
        self.botonAgregarEstudiante = Button(self.frameBotones2,text="Agregar➕", command = self.agregarCalificacion)
        self.botonAgregarEstudiante.pack(side = LEFT)
        
        self.botonModificarEstudiante = Button(self.frameBotones2,text="Modificar", command = self.modificarCalificacion)
        self.botonModificarEstudiante.pack(side = LEFT)
        
        self.botonEliminarEstudiante = Button(self.frameBotones2,text="Eliminar−", command = self.eliminarCalificacion)
        self.botonEliminarEstudiante.pack(side = LEFT)
        
        #id de la calificacion a editar
        self.idCalificacionAEditar = 0
 
        #coneccion a tabla calificaciones y carga de data de comboboxes
        self.calificaciones = []
        self.headerCalificaciones = []
        
        try:    
            #agregamos los datos a los comboboxes
            self.cursorSql.execute("select Matricula, Nombre, IdCarrera from Estudiantes")
            self.listaDeEstudiantes = self.cursorSql.fetchall()
            self.comboboxEstudiante["values"] = self.listaDeEstudiantes
            self.comboboxEstudiante.current(0) #para que seleccione al primero por default
            
            self.cursorSql.execute(f"SELECT Id, NombreMateria FROM Materia WHERE IdCarrera = {self.listaDeEstudiantes[0][2]}")
            self.listaDeMaterias = self.cursorSql.fetchall()
            self.comboboxMateria["values"] = self.listaDeMaterias
            self.comboboxMateria.current(0) #para que seleccione al primero por default
            
            self.cursorSql.execute('''
                                select Calificaciones.Id, (Estudiantes.Nombre|| ' ' ||Estudiantes.Apellido) as 'Nombre', Materia.NombreMateria , Calificaciones.Practica1, Calificaciones.Practica2,
                                Calificaciones.Foro1, Calificaciones.Foro2, Calificaciones.Primer_parcial, Calificaciones.Segundo_parcial, 
                                Calificaciones.Examen_final from Calificaciones INNER JOIN 
                                Estudiantes on Calificaciones.Matricula_estudiante = Estudiantes.Matricula INNER JOIN
                                Materia on Calificaciones.Id_materia = Materia.Id
                                   ''')
            self.headerCalificaciones = self.cursorSql.description #header
            self.calificaciones = self.cursorSql.fetchall() #datos estudiantes
            
        except Exception as e:
            print(e)
            tkinter.messagebox.showerror(title="Error",message="Ups! error al conectar")
        
        self.comboboxEstudiante.bind("<<ComboboxSelected>>", self.seleccionComboBox)
        
        #tabla de datos - treeview
        Utilitarios.generarTreeview(self.wrapper2, self.headerCalificaciones, self.calificaciones, self.obtenerDatos)
        
        self.wrapper1.pack(fill="both", expand="no", padx=10, pady=10)
        self.wrapper2.pack(fill="both", expand="yes", padx=10, pady=10)
        


        
    def obtenerDatos(self, event, tree):
        seleccion = tree.item(tree.focus())
        self.cursorSql.execute(f"SELECT * FROM Calificaciones WHERE Id = {seleccion['values'][0]}")
            
        calificacion = self.cursorSql.fetchall() #datos calificacion
        
        print(seleccion["values"])
        
        #id de la materia  a editar
        self.idCalificacionAEditar = calificacion[0][0]
            
            
        #seteamos los textBox
        self.textBoxPractica1.delete(0,END) 
        self.textBoxPractica1.insert(END, str(calificacion[0][1]))
        self.textBoxPractica2.delete(0,END) 
        self.textBoxPractica2.insert(END, str(calificacion[0][2]))
        self.textBoxForo1.delete(0,END) 
        self.textBoxForo1.insert(END, str(calificacion[0][3]))
        self.textBoxForo2.delete(0,END) 
        self.textBoxForo2.insert(END, str(calificacion[0][4]))
        self.textBoxPrimerParcial.delete(0,END) 
        self.textBoxPrimerParcial.insert(END, str(calificacion[0][5]))
        self.textBoxSegundoParcial.delete(0,END) 
        self.textBoxSegundoParcial.insert(END, str(calificacion[0][6]))
        self.textBoxExamenFinal.delete(0,END) 
        self.textBoxExamenFinal.insert(END, str(calificacion[0][7]))
            
        #seteamos los combobox
        nuevoValorEstudiantes = ""
        for i in range(len(self.listaDeEstudiantes)):
            if self.listaDeEstudiantes[i][0] == calificacion[0][8]:
                nuevoValorEstudiantes = self.listaDeEstudiantes[i]            
        self.comboboxEstudiante.set(nuevoValorEstudiantes)
            
        nuevoValorMateria = ""
        for i in range(len(self.listaDeMaterias)):
            if self.listaDeMaterias[i][0] == calificacion[0][9]:
                nuevoValorMateria = self.listaDeMaterias[i]
        self.comboboxMateria.set(nuevoValorMateria)
    
    
    def seleccionComboBox(self, event): 
        #selecciona el IdCarrera del estudiante y busca las materias de esa carrera
        index = self.comboboxEstudiante.current()        
        self.cursorSql.execute(f"SELECT Id, NombreMateria FROM Materia WHERE IdCarrera = {self.listaDeEstudiantes[index][2]}")
        materias = self.cursorSql.fetchall()
        self.comboboxMateria["values"] = materias
        self.comboboxMateria.current(0)
    
    
    
    #actualiza la ventana
    def actualizarVentana(self):
        self.top.destroy()
        self.__init__()
        
    def agregarCalificacion(self):
        
        self.cursorSql.execute(f"SELECT count(*) FROM Calificaciones WHERE Calificaciones.Matricula_estudiante = {self.comboboxEstudiante.get().split(' ')[0]} AND Calificaciones.Id_materia = {self.comboboxMateria.get().split(' ')[0]}")
        cantMismaMateria = self.cursorSql.fetchall()
        print(cantMismaMateria[0][0])
        if cantMismaMateria[0][0] < 1: #revisa si ya este estudiante tiene esa materia en calificacion              
            try:
                self.cursorSql.execute(f'''
                                       INSERT INTO Calificaciones 
                                       VALUES(null,{self.textBoxPractica1.get()},
                                       {self.textBoxPractica2.get()},{self.textBoxForo1.get()},
                                       {self.textBoxForo2.get()},{self.textBoxPrimerParcial.get()},
                                       {self.textBoxSegundoParcial.get()},{self.textBoxExamenFinal.get()},
                                       {self.comboboxEstudiante.get().split(' ')[0]},
                                       {self.comboboxMateria.get().split(' ')[0]})
                                       ''')
                
                self.connection.commit()
                tkinter.messagebox.showinfo("Listo!", "Se ha agregado la calificacion")
                self.actualizarVentana()
            except:
                tkinter.messagebox.showerror(title="Error",message="Ups! no se pudo agregar a la base de datos")
        else:
            tkinter.messagebox.showerror(title="Error",message="Ups! no se pudo agregar a la base de datos [no se puede repetir la misma calificacion]")
    
    def modificarCalificacion(self):
        if self.idCalificacionAEditar != 0:
            try:
                self.cursorSql.execute(f'''
                                       UPDATE Calificaciones set Practica1 = {self.textBoxPractica1.get()},
                                       Practica2 = {self.textBoxPractica2.get()},
                                       Foro1 = {self.textBoxForo1.get()},
                                       Foro2 = {self.textBoxForo2.get()},
                                       Primer_parcial = {self.textBoxPrimerParcial.get()},
                                       Segundo_parcial = {self.textBoxSegundoParcial.get()},
                                       Examen_final = {self.textBoxExamenFinal.get()},
                                       Matricula_estudiante = {self.comboboxEstudiante.get().split(' ')[0]},
                                       Id_materia = {self.comboboxMateria.get().split(' ')[0]}
                                       WHERE Id = {self.idCalificacionAEditar}''')
                self.connection.commit()
                tkinter.messagebox.showinfo("Listo!", "Se ha modificado la calificacion")
                self.actualizarVentana()
            except:
                 tkinter.messagebox.showerror(title="Error",message="Ups! no se pudo modificar de la base de datos")
        else:
            tkinter.messagebox.showerror(title="Error",message="Ups! no se pudo modificar de la base de datos [debe seleccionar]")
        
        

    def eliminarCalificacion(self):
        if self.idCalificacionAEditar != 0:
            try:
                self.cursorSql.execute(f"DELETE from Calificaciones WHERE Id = {self.idCalificacionAEditar}")
                self.connection.commit()
                tkinter.messagebox.showinfo("Listo!", "Se ha borrado la calificacion")
                self.actualizarVentana()
            except:
                 tkinter.messagebox.showerror(title="Error",message="Ups! no se pudo eliminar de la base de datos")
        else:
            tkinter.messagebox.showerror(title="Error",message="Ups! no se pudo eliminar de la base de datos [debe seleccionar]")
           

        
class GeneracionNotas:
    
    def __init__(self):
        
        self.connection = sqlite3.connect("bdPractica4")
        self.cursorSql = self.connection.cursor()
        
        self.top = Toplevel()
        self.top.grab_set()
        self.top.title("Gestion de impresion de notas")
        self.top.geometry("720x340")
        
        #label
        self.label = Label(self.top, text="Estudiantes disponibles para generar calificaciones: ")
        self.label.config(font=(20))
        self.label.pack()
        #botones
        self.botonAgregarEstudiante = Button(self.top,text="General html➕",command= self.generarHtml)
        self.botonAgregarEstudiante.pack()
        
        #id de la matricula del estudiante
        self.idMatEstudiante = 0
        
        #coneccion a tabla estudiantes
        self.estudiantes = []
        self.headerEstudiantes = []
        try:
            
            self.cursorSql.execute("SELECT Estudiantes.* from Estudiantes INNER JOIN Calificaciones on Estudiantes.Matricula = Calificaciones.Matricula_estudiante GROUP BY Estudiantes.Matricula")
            
            self.headerEstudiantes = self.cursorSql.description #header
            self.estudiantes = self.cursorSql.fetchall() #datos estudiantes
            
        except:
            tkinter.messagebox.showerror(title="Error",message="Ups! error al conectar")
            
        #tabla de datos
        self.frame = Frame(self.top)
        self.frame.pack(fill=X, side=BOTTOM)
        
        #creacion tabla
        #Utilitarios.generarTabla(self.frame, self.estudiantes, self.headerEstudiantes, self.generarHtml)
        Utilitarios.generarTreeview(self.frame, self.headerEstudiantes, self.estudiantes, self.obtenerDatos)

    def obtenerDatos(self, event, tree):
        seleccion = tree.item(tree.focus())
        self.idMatEstudiante = seleccion["values"][0]
        print(seleccion["values"])
    
    #actualiza la ventana
    def actualizarVentana(self):
        self.top.destroy()
        self.__init__()
        
    def generarHtml(self):
        print("convirtiendo a html")
        try:
            self.cursorSql.execute(f'''
                                   SELECT Estudiantes.Matricula, Estudiantes.Nombre, Materia.NombreMateria ,Calificaciones.Practica1, Calificaciones.Practica2,
                                   Calificaciones.Foro1, Calificaciones.Foro2, Calificaciones.Primer_parcial, Calificaciones.Segundo_parcial, 
                                   Calificaciones.Examen_final from Estudiantes INNER JOIN Calificaciones on 
                                   Estudiantes.Matricula = Calificaciones.Matricula_estudiante INNER JOIN
                                   Materia on Calificaciones.Id_materia = Materia.Id
                                   where Calificaciones.Matricula_estudiante = {self.idMatEstudiante}
                                    ''')
            informacion = self.cursorSql.fetchall()
            #obtenemos los datos
            matricula = informacion[0][0]
            nombre = informacion[0][1]
            
            notas = []
            for i in range(len(informacion)):
                notas.append(informacion[i][2:])

            
        except:
            tkinter.messagebox.showerror(title="Error",message="Ups! error al cargar datos para generar HTML [debe seleccionar un estudiante]")
            
        
        #definicion del html
        html = f'''
        <!DOCTYPE html>
        <html lang="en">
        
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Calificaciones - Estudiante: {nombre}, Matricula: {matricula}</title>
        '''
        
        #agregamos los estilos de la pag
        html += '''
        <style>
            .title {
                text-align: center;
                font-weight: bold;
                margin-top: 1.5rem;
            }
        
            .date {
                margin-right: 1.5rem;
                text-align: end;
            }
        
            .table {
        
                width: 100%;
                margin-top: 20px;
                text-align: center;
                vertical-align: middle;
            }
        
            .literal {
                font-size: 80px;
                color: red;
        
            }
        
            th {
                border-bottom: 2px solid black;
                color: #2865c2;
            }
        
            td {
                padding-top: 5px;
            }
        </style>
        
        </head>
        '''
        #agregamos el contenido del titulo y los headers de la tabla
        html += f'''
        <body>
            <div class="title">
                <div>Sistema de Estudiantes</div>
                <div>Listado de Calificaciones de {nombre}</div>
            </div>
            <div class="date">Fecha: {datetime.date.today()}</div>
            <table cellspacing="0" class="table">
                <tr>
                    <th>Matricula</th>
                    <th>Nombre</th>
                    <th>NombreMateria</th>
                    <th>Calificaciones</th>
                    <th>Literal</th>
                </tr>
        '''
        
        html += f'''
                <tr>
                    <td>{matricula}</td>
                    <td>{nombre}</td>
        '''
        for i in range(len(informacion)):            
            #nombre de la materia
            materia = notas[i][0]
            #las notas a asignar
            practica1 = notas[i][1]
            practica2 = notas[i][2]
            
            foro1 = notas[i][3]
            foro2 = notas[i][4]
            
            primerParcial = notas[i][5]
            segundoParcial = notas[i][6]
            
            examenFinal = notas[i][7]
            
            #calculando el promedio final
            promPracticas = (practica1 + practica2)/2
            promForos = (foro1 + foro2)/2
            promParciales = (primerParcial + segundoParcial)/2 
            
            #el promedio final es redondeado
            promFinal = round((promPracticas + promForos + promParciales + examenFinal)/4)
            
            #asignando el valor a la literal 
            literal = '''
                <td class="literal" #literal>F</td>
            '''
            
            if promFinal > 89:
                literal = '''
                <td class="literal" #literal>A</td>
                '''
            elif promFinal > 79:
                literal = '''
                <td class="literal" #literal>B</td>
                '''
            elif promFinal > 69:
                literal = '''
                <td class="literal" #literal>C</td>
                '''
            elif promFinal > 59:
                literal = '''
                <td class="literal" #literal>D</td>
                '''
                
            
            html += f'''
                <td>{materia}</td>
                <td style="width: 20%;">
                    <table style="width: 100%;">
                        <tr>
                            <td style="text-align: left !important;">Practica1</td>
                            <td>{practica1}</td>
                            <td style="text-align: left !important;">Practica2</td>
                            <td>{practica2}</td>
                        </tr>
                        <tr>
                            <td style="text-align: left !important;">Foro1</td>
                            <td>{foro1}</td>
                            <td style="text-align: left !important;">Foro2</td>
                            <td>{foro2}</td>
                        </tr>
                        <tr>
                            <td style="text-align: left !important;">P. Parcial</td>
                            <td>{primerParcial}</td>
                            <td style="text-align: left !important;">S. Parcial</td>
                            <td>{segundoParcial}</td>
                        </tr>
                        <tr>
                            <td style="text-align: left !important;">Ex. Final</td>
                            <td>{examenFinal}</td>
                        </tr>
                        <tr>
                            <td style="text-align: left !important;">Promedio</td>
                            <td>{promFinal}</td>
                        </tr>
                    </table>
                </td>
                {literal}
            </tr>
            <tr>
                <td></td>
                <td></td>
            
            '''
        html += '''
                </table>
                <script type="text/javascript">
                    document.addEventListener('DOMContentLoaded', function () {
            
                        var elements = document.getElementsByClassName("literal");
                        for (var i = 0, length = elements.length; i < length; i++) {
                            if (elements[i].textContent === 'A') {
                                elements[i].style.color = "#0062ad";
                            } else if (elements[i].textContent === 'B') {
                                elements[i].style.color = "#2da14c";
                            } else if (elements[i].textContent === 'C') {
                                elements[i].style.color = "#ffbb33";
                            } else if (elements[i].textContent === 'D') {
                                elements[i].style.color = "#c959b9";
                            }
            
                        }
                    }, false);
                </script>
            </body>
            
            </html>    
        '''
        try:
            #creacion del documen  
            file = open(f"calificaciones_{matricula}_{nombre}.html", "w")
            
            #finalmente escribimos el archivo y los cerramos
            file.write(html)
            file.close()
            tkinter.messagebox.showinfo(title="Listo!",message="Se ha generado el html [Revisar Carpeta]")
            self.actualizarVentana
        except:
            tkinter.messagebox.showerror(title="Error",message="Ups! error al general el html")
        
class VentanaPrincipal:
    
    def __init__(self):
        #definimos la ventana
        ventana = Tk()
        
        ventana.geometry("520x280")
        ventana.resizable(0,0)
        ventana.title("Sistema de calificaciones de estudiantes")
        
        #menu
        menubar = Menu(ventana)
        ventana.config(menu=menubar)
        
        
        #gestion
        menuGestion = Menu(menubar)
        menubar.add_cascade(label="Gestion",menu=menuGestion)
        menuGestion.add_command(label = "Estudiantes", command=GestionEstudiantes)
        menuGestion.add_command(label = "Carreras", command=GestionCarreras)
        menuGestion.add_command(label = "Materias", command=GestionMaterias)
        menuGestion.add_command(label = "Calificaciones", command=GestionCalificaciones)
        
        #reportes
        menuReportes = Menu(menubar)
        menubar.add_cascade(label="Reportes", menu=menuReportes)
        menuReportes.add_command(label = "Generar notas [HTML]", command=GeneracionNotas)
        
        ##menu de botones
        #mb = Menubutton(ventana, text="Boton de menu de Gestion")
        #mb.menu = Menu(mb)
        #mb["menu"] = mb.menu
        
                  
        #mb.menu.add_command(label = "1) Estudiantes", command=GestionEstudiantesNew)
        #mb.menu.add_command(label = "2) Carreras", command=GestionCarreras)
        #mb.menu.add_command(label = "3) Materias", command=GestionMaterias)
        #mb.menu.add_command(label = "4) Calificaciones", command=GestionCalificacionesNew)
        #mb.menu.add_command(label = "Estudiantes", command=GestionEstudiantes) 
        #mb.menu.add_command(label = "Materias", command=GestionMaterias)
        #mb.menu.add_command(label = "Calificaciones", command=GestionCalificaciones)
        #mb.menu.add_command(label = "Generar notas [HTML]", command=GeneracionNotas)
        
        
        #mb.pack()
        
        
        ventana.mainloop()
        

#ejecucion programa
nVentanaPrincipal = VentanaPrincipal()