#!/usr/bin/python
import time
import socket
import _thread
import os
import sqlite3
from tqdm import tqdm

address = ('localhost', 7410)

# Create sockets
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect sockets
server_socket.bind(address)
server_socket.listen(1)

def get_name(name, username):
    new_name = name.decode().split(".")
    new_name[1] = "." + new_name[1]
    return (new_name[0] + new_name[1])


def check_file_existence(username, file_name):
    with sqlite3.connect("USERS.db") as db:
        cursor = db.cursor()
    find_file = ("SELECT files.filename, files.filesize FROM files INNER JOIN user ON files.user_id = user.userID AND files.filename = ? AND user.username = ? ;")
    cursor.execute(find_file,[(file_name),(username)])
    results = cursor.fetchone()
    if(results):
        print("You have already uploaded this file!!")
        return True
    else:
        return False


def save_path_file_db(username, userID, file_path, file_name, file_size):

    with sqlite3.connect("USERS.db") as db:
        cursor = db.cursor()
    insertData = '''INSERT INTO files(fullpath,filename,filesize,user_id) VALUES(?,?,?,?)'''
    cursor.execute(insertData,[(file_path),(file_name),(file_size),(userID)])
    db.commit()
    

def upload_files(server_input, address):

    while True:
        
        file_size = server_input.recv(1024)
        file_size = file_size.decode()
        if(file_size == "Sair"):
            print("Connection terminated from ", address)
            server_input.close()
            break
        file_size = int(file_size)
        
        userID = server_input.recv(1024)
        userID = int(userID.decode())
        username = server_input.recv(1024)
        username = username.decode()
        file_name = server_input.recv(1024)
        new_file_name = get_name(file_name,username) 

        client_folder = os.getcwd() + "/Server Files/" + username
        if(not os.path.isdir(client_folder)):
            os.mkdir(client_folder)
        
        save_path = client_folder + "/" + new_file_name
        
        result = check_file_existence(username,new_file_name)

        server_input.send(str(result).encode())
        if(not result):

            save_path_file_db(username,userID,save_path,new_file_name,file_size)
            new_file = open(save_path,'wb')
            aux_size = 0
            print("Uploading file...")
            while aux_size < file_size:
                data = server_input.recv(1024)
                new_file.write(data)
                aux_size += len(data)
            
            new_file.close()
            print("Successfully Uploaded by ", username)
            print()


def client_thread(server_input, address):

    instruction = server_input.recv(1024)

    if(instruction.decode() == "Upload"):
        upload_files(server_input, address)

def create_files_folder():
    folder = os.getcwd()
    folder += "/Server Files"
    if(not os.path.isdir(folder)):
        os.mkdir(folder)


create_files_folder()
# Create New Threads
while True:
    server_input, address = server_socket.accept()
    print ("New connection received from", address)
    _thread.start_new_thread(client_thread, (server_input, address))