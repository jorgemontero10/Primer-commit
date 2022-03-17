# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 19:01:08 2022

@author: Jorge Montero
"""

import sys
import socket
import threading
import os
import datetime

def contenttype(file):
    if file.endswith('.txt'):
        return 'text/plain'
    elif file.endswith('.html'):
        return 'text/html'
    elif file.endswith('.gif'):
        return 'image/gif'
    elif file.endswith('.jpeg') or file.endswith('.jpg'):
        return 'image/jpeg'
    else:
        return 'application/octet-stream'
    
def multiserver(servidor2):
    try:
        mensaje=servidor2.recv(4096).decode('UTF-8').split('\n')
        peticion= mensaje[0].split(' ')
        if peticion[1] == "/":
            peticion[1] = "index.html"
        print(peticion)
        fecha=str(datetime.date.today())
        
        if len(peticion) !=3 or peticion[0] not in ['GET', 'HEAD']:
            linea_error=("HTTP/1.0 400 Bad Request" + "\n")
            linea_fecha=('Date: {}'.format(fecha) + '\n')
            linea_servidor=('Server: localhost, ' + 'localhost')
            servidor2.send((linea_error + linea_fecha + linea_servidor+'\n\n').encode('UTF-8'))
        elif os.path.exists('data'+ peticion[1]) ==False:
            linea_error=("HTTP/1.0 404 Not Found" + "\n")
            linea_fecha=('Date: {}'.format(fecha)+ '\n')
            linea_servidor=('Server: localhost, '+ 'localhost')
            servidor2.send((linea_error + linea_fecha + linea_servidor+'\n\n').encode('UTF-8'))
    except:
        linea_error = ("HTTP/1.0 400 Bad Request" + "\n")
        linea_fecha = ('Date: {}'.format(fecha)+'\n')
        linea_servidor=('Server: localhost, '+'localhost')
        servidor2.send=((linea_error + linea_fecha + linea_servidor+ '\n\n').encode('UTF-8'))
    finally:
        servidor2.close()
    
def main():
    if len(sys.argv)!=2:
        print('Formato ServidorTCPMultihilo {puerto}')
        sys.exit()
    try:
        puerto = int(sys.argv[1])
        socketServidor=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketServidor.bind(('localhost', puerto))
        socketServidor.settimeout(300)
        socketServidor.listen()
       
        while True :
            socketServidor2, address = socketServidor.accept()
            threading.Thread(target=multiserver, args=(socketServidor2, )).start()
  
    
    except socket.timeout:
        print('300 segundos sin recibir nada.')
    except: 
        print('Error: ', sys.exc_info()[0])
        raise
    finally:
        socketServidor.close()
        
    

if __name__ == "__main__":
    main()