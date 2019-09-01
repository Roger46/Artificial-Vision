# https://realpython.com/python-sockets/
import socket

HOST = '84.88.129.201'	# Adrreça IP del robot
PORT = 2000 # Port que hem definit en el socket del robot

def enviarDades(message):
	# Preparar el missatge amb el protocol definit
	# Protocol: X;Y;A. La varialbe A que es l'altura la definim nosaltres
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect((HOST, PORT))
	m = message.encode('utf-8')
	client.send(m)
	client.close()
