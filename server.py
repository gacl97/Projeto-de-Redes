#!/usr/bin/python
import time
import socket
import _thread
import os
import sqlite3
from tqdm import tqdm

address = ('localhost', 2034)

# Create sockets
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect sockets
server_socket.bind(address)
server_socket.listen(1)

def check_upload_file(username, file_name):

    with sqlite3.connect("USERS.db") as db:
        cursor = db.cursor()
    find_file = ("SELECT files.filename, files.filesize FROM files INNER JOIN user ON files.user_id = user.userID AND files.filename = ? AND user.username = ?;")
    cursor.execute(find_file,[(file_name),(username)])
    results = cursor.fetchone()
    if(results):
        print("You have already uploaded this file!!")
        return True
    else:
        return False

def check_download_file(username, file_name):

    with sqlite3.connect("USERS.db") as db:
        cursor = db.cursor()
    find_file = ("SELECT files.fullpath, files.filesize FROM files INNER JOIN user ON files.user_id = user.userID AND user.username = ? AND files.filename = ?;")
    cursor.execute(find_file,[(username),(file_name)])
    results = cursor.fetchone()

    if(results):
        return results
    else:
        return False

def check_file_to_delete(username, file_name):

    with sqlite3.connect("USERS.db") as db:
        cursor = db.cursor()
    find_file = ("SELECT files.fileID FROM files INNER JOIN user ON files.user_id = user.userID AND user.username = ? AND files.filename = ?;")
    cursor.execute(find_file,[(username),(file_name)])
    results = cursor.fetchone()

    if(results):
        return results
    else:
        return False

def save_path_file_db(username, userID, file_path, file_name, file_size):

    with sqlite3.connect("USERS.db") as db:
        cursor = db.cursor()
    insertData = '''INSERT INTO files(fullpath,filename,filesize,user_id) VALUES(?,?,?,?)'''
    cursor.execute(insertData,[(file_path),(file_name),(file_size),(userID)])
    db.commit()
    
def upload_files(server_input):

    file_size = int(server_input.recv(1024).decode())
    
    userID = int(server_input.recv(1024).decode())
    username = server_input.recv(1024)
    username = username.decode()
    new_file_name = server_input.recv(1024).decode()

    client_folder = os.getcwd() + "/Server Files/" + username
    if(not os.path.isdir(client_folder)):
        os.mkdir(client_folder)
    
    save_path = client_folder + "/" + new_file_name
    result = check_upload_file(username,new_file_name)
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

def delete_file_db(fileID):

    with sqlite3.connect("USERS.db") as db:
        cursor = db.cursor()
    delete_file = '''DELETE FROM files WHERE fileID = ?'''
    cursor.execute(delete_file,[(fileID)])
    db.commit()

def download_files(server_input):

    username = server_input.recv(1024).decode()
    file_name = server_input.recv(1024).decode()
    result = check_download_file(username, file_name)
    time.sleep(0.2)

    if(result):
        
        server_input.send("True".encode())
        client_folder = os.getcwd() + "/Download " + username

        if(not os.path.isdir(client_folder)):
            os.mkdir(client_folder)
        
        server_input.send(str(result[1]).encode())
        new_file = open(result[0],'rb')
        server_input.send(new_file.read(result[1]))
        new_file.close()
        print("Downloaded successfully by: ", username)
    else:
        server_input.send("False".encode())

def delete_file(server_input):

    username = server_input.recv(1024).decode()
    file_name = server_input.recv(1024).decode()
    result = check_file_to_delete(username, file_name)
    time.sleep(0.2)

    if(result):
        
        client_file_delete = os.getcwd() + "/Server Files/" + username + '/' + file_name
        os.remove(client_file_delete)
        delete_file_db(result[0])
        print("File successfully deleted by: ", username)
        server_input.send("True".encode())
    else:
        server_input.send("False".encode())


def client_thread(server_input, address):

    while True:

        instruction = server_input.recv(1024)

        if(instruction.decode() == "Upload"):
            upload_files(server_input)
        elif(instruction.decode() == "Download"):
            download_files(server_input)
        elif(instruction.decode() == "Delete"):
            delete_file(server_input)
        elif(instruction.decode() == "Sair"):
            print("Connection terminated from ", address)
            server_input.close()
            break


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