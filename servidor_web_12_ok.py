# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 11:54:43 2021

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
        elif os.path.exists('data'+ peticion[1]) == False:
            linea_error=("HTTP/1.0 404 Not Found" + "\n")
            linea_fecha=('Date: {}'.format(fecha)+ '\n')
            linea_servidor=('Server: localhost, '+ 'localhost')
            servidor2.send((linea_error + linea_fecha + linea_servidor+'\n\n').encode('UTF-8'))
        else:
            fichero = 'data'+peticion[1] 
            URL='data'+peticion[1]
            if peticion[0] == 'GET':
                if URL.endswith('.txt') or URL.endswith('.html'):
                    with open(fichero, 'rb') as f:
                        content = f.read()
                        linea_error=("HTTP/1.0 200 OK"+"\n")
                        linea_fecha=('Date: {}'.format(fecha)+"\n")
                        linea_servidor=('Server: localhost, '+'localhost'+"\n")
                        linea_longitud=('Content-Length: ' + str(os.path.getsize(fichero))+"\n")
                        linea_tipo=('Content-Type: '+ str(contenttype(fichero))+"\n")
                        linea_modificacion=('Last-Modified: '+ (datetime.datetime.fromtimestamp(os.path.getmtime(fichero)).strftime('%a, %d %b %Y %H:%M:%S %Z')))
                        servidor2.send((linea_error + linea_fecha + linea_servidor + linea_longitud + linea_tipo + linea_modificacion +'\n\n').encode('UTF-8'))
                        servidor2.send(content)
                        
                elif URL.endswith('.gif') or URL.endswith('.jpeg') or URL.endswith('.jpg'):
                    with open(fichero, 'rb') as f:
                        content = f.read()
                        linea_error=("HTTP/1.0 200 OK"+"\n")
                        linea_fecha=('Date: {}'.format(fecha)+"\n")
                        linea_servidor=('Server: localhost, '+'localhost'+"\n")
                        linea_longitud=('Content-Length: ' + str(os.path.getsize(fichero))+"\n")
                        linea_tipo=('Content-Type: ' + str(contenttype(fichero))+"\n")
                        linea_modificacion=('Last-Modified: '+ (datetime.datetime.fromtimestamp(os.path.getmtime(fichero)).strftime('%a, %d %b %Y %H:%M:%S %Z')))
                        servidor2.send((linea_error + linea_fecha + linea_servidor + linea_longitud + linea_tipo + linea_modificacion +'\n\n').encode('UTF-8'))
                        servidor2.send(content)
                        
                else:
                    with open(fichero, 'r') as f:
                        content = f.read()
                        linea_error=("HTTP/1.0 200 OK"+"\n")
                        linea_fecha=('Date: {}'.format(fecha)+"\n")
                        linea_servidor=('Server: localhost, '+'localhost'+"\n")
                        linea_longitud=('Content-Length: '+str(os.path.getsize(fichero))+"\n")
                        linea_tipo=('Content-Type: '+ str(contenttype(fichero))+"\n")
                        linea_modificacion=('Last-Modified: '+ (datetime.datetime.fromtimestamp(os.path.getmtime(fichero)).strftime('%a, %d %b %Y %H:%M:%S %Z')))
                        servidor2.send((linea_error + linea_fecha + linea_servidor + linea_longitud + linea_tipo + linea_modificacion +'\n\n'+ content).encode('UTF-8'))
                        
            elif peticion[0] == 'HEAD':
                if URL.endswith('.txt') or URL.endswith('.html'):
                    with open(fichero, 'r') as f:
                        content = f.read
                        linea_error=("HTTP/1.0 200 OK"+"\n")
                        linea_fecha=('Date: {}'.format(fecha)+'\n')
                        linea_servidor=('Server: localhost, '+'localhost'+'\n')
                        linea_longitud=('Content-Length: '+str(os.path.getsize(fichero))+ '\n')
                        linea_tipo=('Content-Type: '+ str(contenttype(fichero))+ '\n')
                        linea_modificacion=('Last-Modified: '+ str(datetime.datetime.fromtimestamp(os.path.getmtime(fichero)).strftime('%a, %d %b %Y %H:%M:%S %Z')))
                        servidor2.send((linea_error + linea_fecha + linea_servidor + linea_longitud + linea_tipo + linea_modificacion+'\n\n').encode('UTF-8'))
                elif URL.endswith('.jpg') or URL.endswith('.jpeg') or URL.endswith('.gif'):
                   with open(fichero, 'rb') as f:
                        content = f.read()
                        linea_error=("HTTP/1.0 200 OK"+ "\n")
                        linea_fecha=('Date: {}'.format(fecha)+'\n')
                        linea_servidor=('Server: localhost, '+'localhost'+'\n')
                        linea_longitud=('Content-Length: '+str(os.path.getsize(fichero))+ '\n')
                        linea_tipo=('Content-Type: '+ str(contenttype(fichero))+ '\n')
                        linea_modificacion=('Last-Modified: '+ (datetime.datetime.fromtimestamp(os.path.getmtime(fichero)).strftime('%a, %d %b %Y %H:%M:%S %Z')))
                        servidor2.send((linea_error + linea_fecha + linea_servidor + linea_longitud + linea_tipo + linea_modificacion+'\n\n').encode('UTF-8'))
                else:
                    with open(fichero, 'r') as f:
                        content = f.read
                        linea_error=("HTTP/1.0 200 OK"+ "\n")
                        linea_fecha=('Date: {}'.format(fecha)+'\n')
                        linea_servidor=('Server: localhost, '+'localhost'+'\n')
                        linea_longitud=('Content-Length: '+str(os.path.getsize(fichero))+ '\n')
                        linea_tipo=('Content-Type: '+ str(contenttype(fichero))+ '\n')
                        linea_modificacion=('Last-Modified: '+ str(datetime.datetime.fromtimestamp(os.path.getmtime(fichero)).strftime('%a, %d %b %Y %H:%M:%S %Z')))
                        servidor2.send((linea_error + linea_fecha + linea_servidor + linea_longitud + linea_tipo + linea_modificacion+ '\n\n').encode('UTF-8'))
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