#!/usr/bin/python

import socket
import _thread
import os

address = ('localhost', 7402)

# Create sockets
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect sockets
server_socket.bind(address)
server_socket.listen(1)

def client_thread(server_input, address):

    while True:
        new_file = open("b.mkv",'wb')
        while True:
            data = server_input.recv(1024)
            if(not data):
                break
            new_file.write(data)
            

        if data == "sair" or not data:
            print (address, "se desconectou.")
            server_input.close()
            return
        print (address, end = "")
        print ("Upload feito com sucesso")
        new_file.close()

# Create New Threads
while True:
    server_input, address = server_socket.accept()
    print ("Nova conexao recebida de", address)
    _thread.start_new_thread(client_thread, (server_input, address))