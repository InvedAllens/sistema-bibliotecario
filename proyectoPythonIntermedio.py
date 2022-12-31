
#Proyecto python intermedio
#Sistema de prestamo bibliotecario con bases de datos
#Aldo Allende Sanchez 

import sqlite3
import getpass

conexion=sqlite3.connect("biblioteca.db")#conexion a biblioteca.db
cursor=conexion.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS alumno(alumno_id INTEGER PRIMARY KEY AUTOINCREMENT,nombre VARCHAR(20),apellidos VARCHAR(50),edad INTEGER,nombre_usuario VARCHAR(30) UNIQUE,contraseña VARCHAR(30))")
cursor.execute("CREATE TABLE IF NOT EXISTS libro (libro_id INTEGER PRIMARY KEY AUTOINCREMENT,nombre VARCHAR(50) UNIQUE,autor VARCHAR(30),año DATE,disponible BOOLEAN)")

bandera=True
while bandera:
    try:#menu principal
        print("\n\t-----Selecciona una opción-----")
        print("\n\t1.-Dar de alta a un usuario")
        print("\t2.-Iniciar sesion como usuario")
        print("\t3.-Terminar el programa")
        opcion=int (input("\t=>"))
        
        if opcion==1:

            nombre = input("\n\tDame el nombre:")
            apellido= input("\tDame los apellidos:")
            edad= int (input("\tDame la edad:"))
            nombreUsuario = input("\tDame el nombre de usuario:")
            contraseña = getpass.getpass("\tDame una contraseña:")
            cursor.execute("INSERT INTO alumno (nombre,apellidos,edad,nombre_usuario,contraseña) VALUES ('%s','%s','%d','%s','%s')"%(nombre,apellido,edad,nombreUsuario,contraseña))
            continue

        elif opcion==2:
            nombreUsuario=input("\n\tIntroduzca su nombre de usuario:")
            contrasena=getpass.getpass("\tIntroduzca su contraseña:") 
            cursor.execute("SELECT * FROM alumno  WHERE nombre_usuario ='%s' AND contraseña ='%s' " %(nombreUsuario,contrasena))           
            usuario=cursor.fetchone()
            bandera2=True
            if usuario != None:
                while bandera2:#menu inicio de sesion
                    print("\n\t-----Bienvenido(a) ",usuario[1],"-----")
                    print("\n\t-----Selecciona una opcion-----")
                    print("\n\t1.-Agregar libro")
                    print("\n\t2.-Actualizar usuario")
                    print("\n\t3.-Mostrar libros disponibles")
                    print("\n\t4.-Prestamo de libro")
                    print("\n\t5.-Devolver libro")
                    print("\n\t6.-Mostrar libros prestados")
                    print("\n\t7.-Salir")
                    opcion=int (input("\t=>"))

                    if opcion==1:
                        try:#Alta  de un registro en la tabla libro
                            nombre_libro=input("Dame el nombre del libro:")
                            autor=input("Dame el autor del libro:")
                            año=input("Dame la fecha del libro en el formato yyyy/mm/dd:")
                            cursor.execute("INSERT INTO libro (nombre,autor,año,disponible) VALUES ('%s','%s','%s','True')"%(nombre_libro,autor,año))
                        except Exception:
                            print("-----No se pudo realizar la inserccion-----")
                        else:
                            print("\n\t-----Libro insertado correctamente-----")
                        
                    elif opcion==2:
                        try:#Actualizar usuario
                            nombre = input("\n\tDame el nuevo nombre:")
                            apellido= input("\tDame los nuevos apellidos:")
                            edad= int (input("\tDame la nueva edad:"))
                            nombre_Usuario = input("\tDame el nuevo nombre de usuario:")
                            contraseña = getpass.getpass("\tDame la nueva contraseña:")
                            cursor.execute("UPDATE alumno SET nombre='%s',apellidos='%s',edad='%d',nombre_usuario='%s',contraseña='%s' WHERE nombre_usuario= '%s'"%(nombre,apellido,edad,nombre_Usuario,contraseña,nombreUsuario))
                        except Exception:
                            print("------No se pudo realizar la actualizacion-----")
                        else:
                            print("\n\t-----Se actualizo correctamente el usuario-----")    
                    elif opcion==3:#selecion e impresion de libros disponibles
                        cursor.execute("SELECT * FROM libro WHERE disponible='True'")
                        libros=cursor.fetchall()
                        if libros != []:
                            print("\n\t-----Libros disponibles-----")
                            for ejemplar in libros:
                                print("\n\tNombre:",ejemplar[1])
                                print("\tAutor:",ejemplar[2])
                                print("\tAño:",ejemplar[3])
                                print("-------------------------------------------------------")
                        else:
                            print("-----No hay libros disponibles-----")
                    elif(opcion==4):#Solicitar un libro para ser prestado
                        libroSolicitado=input("\n\tDame el nombre del libro: ")
                        cursor.execute("SELECT * FROM libro WHERE nombre='%s' AND disponible='True'"%(libroSolicitado))
                        lib=cursor.fetchone()
                        if lib !=None:
                            print("\n\tNombre:",lib[1],)
                            print("\n\tAutor:",lib[2],)
                            print("\n\tAño:",lib[3],)    
                            cursor.execute("UPDATE libro SET disponible='False' WHERE nombre='%s'"%(libroSolicitado))
                            print("\n\t---Se ha realizado el prestamo correctamente---")    
                        else:
                            print("\n\t---No se encontro algun libro con el nombre indicado o no se encuentra disponible---")
                    elif(opcion==5):#solicitar una devolucion de un libro
                        libroDevuelto=input("\n\tDame el nombre del libro: ")
                        cursor.execute("SELECT * FROM libro WHERE nombre='%s' AND disponible='False'"%(libroDevuelto))
                        lib=cursor.fetchone()
                        if lib !=None:
                            print("\n\tNombre:",lib[1],)
                            print("\n\tAutor:",lib[2],)
                            print("\n\tAño:",lib[3],)    
                            cursor.execute("UPDATE libro SET disponible='True' WHERE nombre='%s'"%(libroDevuelto))
                            print("\n\t---Se ha realizado la devolucion correctamente---")    
                        else:
                            print("\n\t---No se encontro algun libro con el nombre indicado o se encuentra disponible---")
                    elif(opcion==6):#Selecion e impresion de libros no disponibles
                        cursor.execute("SELECT * FROM libro WHERE disponible='False'")
                        libros=cursor.fetchall()
                        if libros != []:
                            print("\n\t-----Libros No disponibles-----")
                            for ejemplar in libros:
                                print("\n\tNombre:",ejemplar[1])
                                print("\tAutor:",ejemplar[2])
                                print("\tAño:",ejemplar[3])
                                print("-------------------------------------------------------")
                        else:
                            print("\n\t-----No hay libros no disponibles-----")
                    elif(opcion==7):    
                        bandera2=False


            else:
                print("\n\tusuario o contraseña incorrectos")


        elif opcion==3:

            bandera=False
    
    except Exception:
	    print("Error en la ejecución")
            
conexion.commit()
conexion.close()