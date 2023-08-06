import datetime
import time
from Pillow import Image
import numpy as np
import shutil
import subprocess

def copiarEncabezado(origen):
    try:
        #nombre = origen.split('/')[-1]
        #extension = nombre.split('.')[-1]
        #print (origen)
        #destino = "header."+extension
        #print (destino)
        destino = "header.jpg"
        shutil.copy2(origen, destino)
        return destino
    except shutil.Error as e:
        print("Error: %s" % e)
    except IOError as e:
        print("Error: %s" % e.strerror)

def moverFotos(fotos, tira):
    #copiar al pendrive
    try:
        usbnamebytes = subprocess.check_output(['ls', '/media/pi'])
        usbname = usbnamebytes.decode("utf-8")[:-1]
        #print (usbname)
        destinationFotos = '/media/pi/'+usbname+'/'
        destinationTiras = '/media/pi/'+usbname+'/'
        #print (destinationFotos)
        #print (destinationTiras)
        #print (fotos[0])
        #print (tira)

        #shutil.copy2(fotos[0], destinationFotos+fotos[0])
        #shutil.copy2(fotos[1], destinationFotos+fotos[1])
        #shutil.copy2(fotos[2], destinationFotos+fotos[2])
        #shutil.copy2(tira, destinationTiras+tira)
        shutil.move(fotos[0], destinationFotos+fotos[0])
        shutil.move(fotos[1], destinationFotos+fotos[1])
        shutil.move(fotos[2], destinationFotos+fotos[2])
        shutil.move(tira, destinationTiras+tira)

    except shutil.Error as e:
        print("Error: %s" % e)
    except IOError as e:
        print("Error: %s" % e.strerror)


def procesarFotos(listaFotos, header):
    #print (header)
    listaFotos.insert(0, header)
    print (listaFotos)
    imgs = [ Image.open(i) for i in listaFotos ]
    # pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
    min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
    # for a vertical stacking it is simple: use vstack
    imgs_comb = np.vstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )
    imgs_comb = Image.fromarray( imgs_comb)

    sourceTira = 'fotoTira_'+datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+'.jpg'
    imgs_comb.save( sourceTira )

    #enviar a imprimir
    listaFotos.pop(0)
    moverFotos(listaFotos, sourceTira)



#date = datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
#camera.capture("/home/pi/photobooth/"+ date + ".jpg")
