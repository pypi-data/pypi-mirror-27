from tkinter import *
import RPi.GPIO as GPIO
import time
from threading import Thread
from sacarfoto import *
from armartira import *
from myconfig import *

def config_buttons():
    while True:
        input_state = GPIO.input(16)
        if input_state == False:
            time.sleep(0.2)
            do_photobooth()
            time.sleep(0.2)
        input_state = GPIO.input(20)
        if input_state == False:
            time.sleep(0.2)
            do_something()
            time.sleep(0.2)
            

def do_something():
    filename = filedialog.askopenfilename(filetypes = [("Imagen", "*.jpg")])
    if not filename:
        myLabel.config(text="CANCELADO")
    else:
        header = copiarEncabezado(filename)
        cfg = MyConfig.leerConfig()
        cfg.header = header
        cfg.escribirConfig()
        myLabel.config(text=filename)
    
def do_photobooth():
    cfg = MyConfig.leerConfig()    
    if not cfg.header:
        print("debe configurar el encabezado")
        myLabel.config(text="debe configurar el encabezado")
    else:    
        print("iniciando tira de fotos")
        myLabel.config(text="iniciando tira de fotos")
        fotos = tomarFotosPiCamera(camera, 21)
        procesarFotos(fotos, cfg.header)
        myLabel.config(text="LISTO")

camera = PiCamera()
header = ""

root = Tk()
root.attributes("-fullscreen", True)
myLabel = Label(text="Hello World")
myLabel.pack()
Button(text="btn FOTO", command=do_photobooth).pack()
Button(text="btn Config", command=do_something).pack()

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)

Thread(target=config_buttons).start()
root.mainloop()
