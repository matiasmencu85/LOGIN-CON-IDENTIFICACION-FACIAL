

#--------------------------------------Importamos librerias--------------------------------------------
# pip install torch-mtcnn desde cmd  o desde file--setting--project identification-- python interpreter-- +(install)-- torch-mtcnn
# pip install tkinter
# pip install opencv-python
# pip install matplotlib
# pip install mtcnn


from tkinter import *
import os
import cv2
from matplotlib import pyplot
from mtcnn.mtcnn import MTCNN

#import numpy as np

#------------------------ Crea funcion que se encargara de registrar el usuario ---------------------

def registrar_usuario():
    usuario_info = usuario.get() #Obtiene la informacion alamcenada en usuario
    contra_info = contra.get()    #Obtiene la informacion almacenada en contraseña

    archivo = open(usuario_info, "w") #Abre la informacion en modo escritura
    archivo.write(usuario_info + "\n")   #escribimos la info
    archivo.write(contra_info)
    archivo.close()

    #Limpia los text variable
    usuario_entrada.delete(0, END)
    contra_entrada.delete(0, END)

    #dice al usuario que su registro ha sido exitoso
    Label(pantalla1, text = "Registro Tradicional Exitoso", fg = "green", font = ("Calibri",20)).pack()
    

#--------------------------- Funcion para almacenar el registro facial --------------------------------------
    
def registro_facial():
    # capturar el rostro
    cap = cv2.VideoCapture(0)               #Elije la camara con la que vamos a hacer la deteccion
    while(True):
        ret,frame = cap.read()              #Lee el video
        cv2.imshow('Registro Facial',frame)         #Muestra el video en pantalla
        if cv2.waitKey(1) == 13:            #Cuando oprimamos "Enter" rompe el video
            break
    usuario_img = usuario.get()
    cv2.imwrite(usuario_img+".jpg",frame)       #Guarda la ultima captura del video como imagen y asignamos el nombre del usuario
    cap.release()                               #Cierra
    cv2.destroyAllWindows()

    usuario_entrada.delete(0, END)   #Limpia los text variables
    contra_entrada.delete(0, END)
    Label(pantalla1, text = "Registro Facial Exitoso", fg = "green", font = ("Calibri",20)).pack()

    #----------------- Detecta el rostro y exportamos los pixeles --------------------------
    
    def reg_rostro(img, lista_resultados):
        data = pyplot.imread(img)
        for i in range(len(lista_resultados)):
            x1,y1,ancho, alto = lista_resultados[i]['box']
            x2,y2 = x1 + ancho, y1 + alto
            pyplot.subplot(1, len(lista_resultados), i+1)
            pyplot.axis('off')
            cara_reg = data[y1:y2, x1:x2]
            cara_reg = cv2.resize(cara_reg,(150,200), interpolation = cv2.INTER_CUBIC) #Guarda la imagen con un tamaño de 150x200
            cv2.imwrite(usuario_img+".jpg",cara_reg)
            pyplot.imshow(data[y1:y2, x1:x2])
        pyplot.show()

    img = usuario_img+".jpg"
    pixeles = pyplot.imread(img)
    detector = MTCNN()
    caras = detector.detect_faces(pixeles)
    reg_rostro(img, caras)   
    
#------------------------Crea una funcion para asignar al boton registro --------------------------------
def registro():
    global usuario
    global contra  #Globaliza las variables para usarlas en otras funciones
    global usuario_entrada
    global contra_entrada
    global pantalla1

    pantalla1 = Toplevel(pantalla) #Esta pantalla es de un nivel superior a la principal
    pantalla1.title("Registro")
    pantalla1.geometry("900x500")  #Asigna el tamaño de la ventana
    pantalla1.config(bg ="black")

    #---------  crea las entradas de usuario y contraseña ----------------------------------------
    
    usuario = StringVar()
    contra = StringVar()

    Label(pantalla1, text="REGISTRO TRADICIONAL: 1) Debe asignar usuario y contraseña 2) Click en boton Login Tradicional").pack()
    Label(pantalla1, text="").pack()  # Dejamos un poco de espacio

    Label(pantalla1, text = "REGISTRO FACIAL: 1) Debe de asignar un usuario 2) Click en boton de Login Facial 3) Mire de frente 4) Teclee Enter 5) Guarde la foto correspondiente al nombre de usuario").pack()
    Label(pantalla1, text = "").pack()  #Dejamos un poco de espacio

    Label(pantalla1, text = "").pack()  #Dejamos un poco de espacio
    Label(pantalla1, text = "Usuario * ").pack()  #Muestra en la pantalla 1 el usuario
    usuario_entrada = Entry(pantalla1, textvariable = usuario) #Crea un text variable para que el usuario ingrese la info
    usuario_entrada.pack()
    Label(pantalla1, text = "Contraseña * ").pack()  #Muestra en la pantalla 1 la contraseña
    contra_entrada = Entry(pantalla1, textvariable = contra) #Crea un text variable para que el usuario ingrese la contra
    contra_entrada.pack()
    Label(pantalla1, text = "").pack()  #Dejamos un espacio para la creacion del boton
    Button(pantalla1, text = "Registro Tradicional", width = 20, height = 1,font = ("Calibri",20, "bold"), command = registrar_usuario).pack()  #Crea el boton

    #------------ Vamos a crear el boton para hacer el registro facial --------------------
    Label(pantalla1, text = "").pack()
    Label(pantalla1, text="").pack()

    Button(pantalla1, text = "Registro Facial", width = 20, height = 1, font = ("Calibri",20, "bold"), command = registro_facial).pack()

#------------------------------------------- Funcion para verificar los datos ingresados al login ------------------------------------
    
def verificacion_login():
    log_usuario = verificacion_usuario.get()
    log_contra = verificacion_contra.get()

    usuario_entrada2.delete(0, END)
    contra_entrada2.delete(0, END)

    lista_archivos = os.listdir()   #Vamos a importar la lista de archivos con la libreria os
    if log_usuario in lista_archivos:   #Comparamos los archivos con el que nos interesa
        archivo2 = open(log_usuario, "r")  #Abrimos el archivo en modo lectura
        verificacion = archivo2.read().splitlines()  #leera las lineas dentro del archivo ignorando el resto
        if log_contra in verificacion:
            print("Inicio de sesion exitoso")
            Label(pantalla2, text = "Inicio de Sesion Exitoso", fg = "green", font = ("Calibri",20)).pack()
        else:
            print("Contraseña incorrecta, ingrese de nuevo")
            Label(pantalla2, text = "Contraseña Incorrecta", fg = "red", font = ("Calibri",20)).pack()
    else:
        print("Usuario no encontrado")
        Label(pantalla2, text = "Usuario no encontrado", fg = "red", font = ("Calibri",20)).pack()
    
#--------------------------Funcion para el Login Facial --------------------------------------------------------
def login_facial():
#------------------------------Vamos a capturar el rostro-----------------------------------------------------
    cap = cv2.VideoCapture(0)               #Elegimos la camara con la que vamos a hacer la deteccion
    while(True):
        ret,frame = cap.read()              #Leemos el video
        cv2.imshow('Login Facial',frame)         #Mostramos el video en pantalla
        if cv2.waitKey(1) == 13:            #Cuando oprimamos "Enter" rompe el video
            break
    usuario_login = verificacion_usuario.get()    #Con esta variable vamos a guardar la foto pero con otro nombre para no sobreescribir
    cv2.imwrite(usuario_login+"LOG.jpg",frame)       #Guardamos la ultima caputra del video como imagen y asignamos el nombre del usuario
    cap.release()                               #Cerramos
    cv2.destroyAllWindows()

    usuario_entrada2.delete(0, END)   #Limpiamos los text variables
    contra_entrada2.delete(0, END)

    #----------------- Funcion para guardar el rostro --------------------------
    
    def log_rostro(img, lista_resultados):
        data = pyplot.imread(img)
        for i in range(len(lista_resultados)):
            x1,y1,ancho, alto = lista_resultados[i]['box']
            x2,y2 = x1 + ancho, y1 + alto
            pyplot.subplot(1, len(lista_resultados), i+1)
            pyplot.axis('off')
            cara_reg = data[y1:y2, x1:x2]
            cara_reg = cv2.resize(cara_reg,(150,200), interpolation = cv2.INTER_CUBIC) #Guardamos la imagen 150x200
            cv2.imwrite(usuario_login+"LOG.jpg",cara_reg)
            return pyplot.imshow(data[y1:y2, x1:x2])
        pyplot.show()

    #-------------------------- Detectamos el rostro-------------------------------------------------------
    
    img = usuario_login+"LOG.jpg"
    pixeles = pyplot.imread(img)
    detector = MTCNN()
    caras = detector.detect_faces(pixeles)
    log_rostro(img, caras)

    #-------------------------- Funcion para comparar los rostros --------------------------------------------
    def orb_sim(img1,img2):
        orb = cv2.ORB_create()  #Creamos el objeto de comparacion
 
        kpa, descr_a = orb.detectAndCompute(img1, None)  #Creamos descriptor 1 y extraemos puntos claves
        kpb, descr_b = orb.detectAndCompute(img2, None)  #Creamos descriptor 2 y extraemos puntos claves

        comp = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True) #Creamos comparador de fuerza

        matches = comp.match(descr_a, descr_b)  #Aplicamos el comparador a los descriptores

        regiones_similares = [i for i in matches if i.distance < 70] #Extraemos las regiones similares en base a los puntos claves
        if len(matches) == 0:
            return 0
        return len(regiones_similares)/len(matches)  #Exportamos el porcentaje de similitud
        
    #---------------------------- Importamos las imagenes y llamamos la funcion de comparacion ---------------------------------
    
    im_archivos = os.listdir()   #Vamos a importar la lista de archivos con la libreria os
    if usuario_login+".jpg" in im_archivos:   #Comparamos los archivos con el que nos interesa
        rostro_reg = cv2.imread(usuario_login+".jpg",0)     #Importamos el rostro del registro
        rostro_log = cv2.imread(usuario_login+"LOG.jpg",0)  #Importamos el rostro del inicio de sesion
        similitud = orb_sim(rostro_reg, rostro_log)
        if similitud >= 0.77:       # porcentaje de similitud de rostro ,cuando mas se acerque a 1 es mas efectivo
            Label(pantalla2, text = "Inicio de Sesion Exitoso", fg = "green", font = ("Calibri",20)).pack()
            print("Bienvenido al sistema usuario: ",usuario_login)
            print("Compatibilidad con la foto del registro: ",similitud)
        else:
            print("Rostro incorrecto, verifique su usuario")
            print("Compatibilidad con la foto del registro: ",similitud)
            Label(pantalla2, text = "Incompatibilidad de rostros", fg = "red", font = ("Calibri",20)).pack()
    else:
        print("Usuario no encontrado")
        Label(pantalla2, text = "Usuario no encontrado", fg = "red", font = ("Calibri",20)).pack()
            

#------------------------Funcion que asignaremos al boton login -------------------------------------------------
        
def login():
    global pantalla2
    global verificacion_usuario
    global verificacion_contra
    global usuario_entrada2
    global contra_entrada2
    
    pantalla2 = Toplevel(pantalla)
    pantalla2.title("Login")
    pantalla2.geometry("600x500")
    #Creamos la ventana de inicio de sesion
    Label(pantalla2, text="Login tradicional: debe asignar usuario y contraseña").pack()
    Label(pantalla2, text="").pack()  # Dejamos un poco de espacio
    Label(pantalla2, text = "Login facial: debe de asignar un usuario click en boton de Login Facial- mire de frente- teclee enter ").pack()
    Label(pantalla2, text="").pack()


    
    verificacion_usuario = StringVar()
    verificacion_contra = StringVar()
    
    #---------------------------------- Ingresamos los datos --------------------------
    Label(pantalla2, text = "Usuario * ").pack()
    usuario_entrada2 = Entry(pantalla2, textvariable = verificacion_usuario)
    usuario_entrada2.pack()

    Label(pantalla2, text = "Contraseña * ").pack()
    contra_entrada2 = Entry(pantalla2, textvariable = verificacion_contra)
    contra_entrada2.pack()

    # ------------ Vamos a crear el boton para hacer el login facial --------------------
    Label(pantalla2, text = "INGRESE NOMBRE DE USUARIO Y CONTRASEÑA").pack()
    Button(pantalla2, text = "Sesion Tradicional", width = 20, height = 2, font = ("Calibri",20,"bold" ),command = verificacion_login).pack()

    Label(pantalla2, text="").pack() # dejamos espacios


    Label(pantalla2, text = "INGRESE NOMBRE DE USUARIO").pack()
    Button(pantalla2, text = "Sesion Facial", width = 20, height = 2, font = ("Calibri",20,"bold" ), command = login_facial).pack()
        
#------------------------- Funcion de nuestra pantalla principal ------------------------------------------------
    
def pantalla_principal():
    global pantalla          #Globalizamos la variable para usarla en otras funciones
    pantalla = Tk()
    pantalla.geometry("600x500")  #Asignamos el tamaño de la ventana
    pantalla.title("SISTEMA IDENTIFICACION DE USUARIOS DE SISTEMA")       #Asignamos el titulo de la pantalla
    Label(text = "Login Inteligente", bg ="blue", width = "300", height = "3", font = ("Verdana", 20, "bold")).pack() #Asignamos caracteristicas de la ventana
    
#------------------------- Vamos a Crear los Botones ------------------------------------------------------
    
    Label(text = "").pack()  #Creamos el espacio entre el titulo y el primer boton
    Button(text = "Iniciar Sesion", height = "3", width = "30", command = login).pack()
    Label(text = "").pack() #Creamos el espacio entre el primer boton y el segundo boton
    Label(text="").pack()
    Button(text = "Registro", height = "3", width = "30", command = registro).pack()

    pantalla.mainloop()

pantalla_principal()