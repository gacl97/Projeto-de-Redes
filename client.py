import socket
import re
import os
import sqlite3
import time
from tqdm import tqdm
from getpass import getpass

address = ('localhost', 2045)

# Create sockets
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def login():
    
    while True:

        clear()
        
        print("------------- User Login -------------")
        print()
        username = input("Enter username: ")
        client_socket.send(username.encode())
        time.sleep(0.2)
        print()
        password = getpass("Enter password: ")
        client_socket.send(password.encode())
        time.sleep(0.2)
        print()

        results = client_socket.recv(1024)
        time.sleep(0.2)
        if(results.decode() == "Fail"):
            clear()
            print("Username or password is incorrect!")
            print("Returning to main menu!!")
            print()
            print()
            time.sleep(0.2)
            return "Fail"

        results1 = client_socket.recv(1024)
        time.sleep(0.2)
        results2 = client_socket.recv(1024)
        time.sleep(0.2)

        return [results.decode(), results1.decode(), results2.decode()]
        
def create_user():

    clear()
    print("------------- User registration -------------")
    print()

    username = input("Enter username: ")
    client_socket.send(username.encode())
    time.sleep(0.2)

    result = client_socket.recv(1024).decode()
    if(result == "Fail"):
        clear()
        print("Returning to main menu!!")
        time.sleep(1)
        return
    
    print()
    password = input("Enter password: ")
    client_socket.send(password.encode())
    time.sleep(0.2)
    print()
    password1 = input("Enter again your password: ")
    client_socket.send(password1.encode())
    time.sleep(0.2)

    while(password != password1):
        print("Your passwords didn't match, try again!!")
        print()
        password = input("Enter password: ")
        client_socket.send(password.encode())
        time.sleep(0.2)
        print()
        password1 = input("Enter again your password: ")
        client_socket.send(password1.encode())
        time.sleep(0.2)
        
    print()
    clear()
    line_interface("1")
    print("Successful registration!!")
    line_interface("2")
    time.sleep(0.2)

def show_client_files(username):

    client_socket.send("Show".encode())
    time.sleep(0.2)
    client_socket.send(username.encode())
    time.sleep(0.2)
    print("-------------- "+ username +" FILES -------------")
    
    results = int(client_socket.recv(1024).decode())
    time.sleep(0.2)
    if(results != 0):
        for i in range(results):
            name = client_socket.recv(1024).decode()
            time.sleep(0.2)
            size = int(client_socket.recv(1024).decode())
            time.sleep(0.2)
            print("Name: ",name, " Size:", size/1000000, "mb (",size,"bytes )")
    else:
        print()
        print("You don't have any files yet!!")
        print()
    print("------------------------------------------")
    print()


def exception_option():

    while True:
        try:
            option = int(input())
            
            return str(option)
        except:
            pass
        print("Option not available!")

def exception_files():

    while True:
        try:
            file_name = input("Enter file or directory name: ")
            file = open(file_name,"rb")
            return [file,file_name]
        except:
            pass
        print("File or directory not available!")
        again = input("Try again? [y,n]")
        if(again.lower() == 'n'):
            clear()
            print("Returning to menu!!")
            print()
            time.sleep(1)
            return [False,False]
        clear()

def progress_bar(file_size):

    for i in tqdm(range(file_size)):
        i += 1024

def line_interface(side):
    if(side == "1"):
        print("-------------------------------")
        print()
    else:
        print()
        print("-------------------------------")
        print()
        print()

def upload_files(username):

    print("------------- Upload File -------------")
    print()
    file, file_name = exception_files()

    if(not file): 
        return
    aux_size = os.stat(file_name)

    # Diretório
    if(os.name == 'nt'):
        aux_file_name = re.split('\\\\' , file_name)
        file_name = aux_file_name[-1]
    else:
        aux_file_name = file_name.split("/")
        file_name = aux_file_name[-1]
    
    client_socket.send("Upload".encode())
    time.sleep(0.2)
    file_size = str(aux_size.st_size)
    client_socket.send(file_size.encode())
    time.sleep(0.2)
    client_socket.send(str(username[0]).encode())
    time.sleep(0.2)
    client_socket.send(username[1].encode())
    time.sleep(0.2)
    client_socket.send(file_name.encode())
    time.sleep(0.2)
    result = client_socket.recv(1024)
    
    if(result.decode() == "False"):
        client_socket.send(file.read(aux_size.st_size))
        progress_bar(aux_size.st_size)
        clear()
        line_interface("1")
        print("Successfully Uploaded!!")
        line_interface("2")
        time.sleep(0.1)
    else:
        clear()
        line_interface("1")
        print("You have already uploaded this file!!")
        line_interface("2")
        time.sleep(0.1)
    file.close()


def download_files(username):

    show_client_files(username[1])
    print()
    client_socket.send("Download".encode())
    file_name = input("Enter the file name: ")
    client_socket.send(str(username[1]).encode())
    time.sleep(0.1)
    client_socket.send(file_name.encode())
    time.sleep(0.1) 
    result = client_socket.recv(1024)

    if(result.decode() == "False"):
        line_interface("1")
        print("File not found!!")
        line_interface("2")
        time.sleep(0.2)
        return

    file_size = int(client_socket.recv(1024).decode())
    client_folder = os.getcwd() + "/Download " + username[1] + "/" + file_name
    aux_size = 0
    new_file = open(client_folder,'wb')

    while aux_size < file_size:
        data = client_socket.recv(1024)
        new_file.write(data)
        aux_size += len(data)
        
    new_file.close()
    clear()
    line_interface("1")
    print("Downloaded successfully, your file is in your folder!!")
    line_interface("2")
    time.sleep(0.2)

def delete_file(username):

    show_client_files(username[1])
    print()

    client_socket.send("Delete".encode())
    file_name = input("Enter the file name: ")
    client_socket.send(str(username[1]).encode())
    time.sleep(0.1)
    client_socket.send(file_name.encode())
    time.sleep(0.1)

    result = client_socket.recv(1024)

    if(result.decode() == "False"):
        line_interface("1")
        print("File not found!!")
        line_interface("2")
        time.sleep(0.2)
        return
    clear()
    line_interface("1")
    print("File successfully deleted!!")
    line_interface("2")

def clear():
    
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    client_socket.connect(address)
    while True:

        print("[1]- Login: ")
        print("[2]- Register")
        print("[3]- Close the program")
        op = exception_option()
        if(op == '1'):
            client_socket.send('Login'.encode())
            username = login()
            if(username != "Fail"):
                print()
                transfer_files(username)
                break
        elif(op == '2'):
            client_socket.send("Register".encode())
            create_user()
        else:
            client_socket.send("Close".encode())
            print("Bye!!")
            time.sleep(1)
            client_socket.close()
            break
    

def menu():

    print("[1]- Show available files: ")
    print("[2]- Upload")
    print("[3]- Download")
    print("[4]- Delete a file")
    print("[5]- Log out")

def transfer_files(username):

    print("-----------------------------")
    print()
    print("Welcome: ", username[1])
    print()
    print("-----------------------------")
    while True:
        try:
            menu()
            op = exception_option()
            if(op == '1'):
                clear()
                show_client_files(username[1])
            elif(op == '2'):
                clear()
                upload_files(username)
            elif(op == '3'):
                clear()
                download_files(username)
            elif(op == '4'):
                clear()
                delete_file(username)
            elif (op == '5'):
                client_socket.send("Close".encode())
                print("Bye!!")
                time.sleep(0.5)
                client_socket.close()
                break
        except:
            print("The server has been disabled.")
            client_socket.close()
            break

main_menu()