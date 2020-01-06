#!/usr/bin/python

import socket
import _thread
import os

address = ('localhost', 7401)

# Create sockets
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect sockets
server_socket.bind(address)
server_socket.listen(1)

def get_name(name):
    new_name = name.decode().split(".")
    new_name[0] += "_"
    new_name[1] = "." + new_name[1]
    return (new_name[0] + new_name[1])

def client_thread(server_input, address):

    while True:
        file_size = server_input.recv(1024)
        file_size = file_size.decode()
        file_size = int(file_size)

        file_name = server_input.recv(1024)
        new_file_name = get_name(file_name) 

        new_file = open(new_file_name,'wb')
        aux_size = 0
        while aux_size < file_size:
            data = server_input.recv(1024)
            new_file.write(data)
            aux_size += len(data)
        new_file.close()
            
        if (data == "sair"):
            print (address, "se desconectou.")
            server_input.close()
            return
        print("Upload feito com sucesso por: ", end = "")
        print(address)

# Create New Threads
while True:
    server_input, address = server_socket.accept()
    print ("Nova conexao recebida de", address)
    _thread.start_new_thread(client_thread, (server_input, address))