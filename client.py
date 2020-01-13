import socket
import os
import sqlite3
import time
from tqdm import tqdm
from getpass import getpass

address = ('localhost', 7410)

# Create sockets
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def login():
    while True:

        username = input("Enter username:")
        password = getpass("Enter password:")
        with sqlite3.connect("USERS.db") as db:
            cursor = db.cursor()
        find_user = ("SELECT * FROM user WHERE username = ? AND password = ?")
        cursor.execute(find_user,[(username),(password)])
        results = cursor.fetchall()

        if(results):
            print()
            print("Login successfully!")
            return results
        else:
            print("Username or password is incorrect!")
            again = input("Do you want to try again?(y/n)")
            if(again.lower() == 'n'):
                print("Returning to main menu!!")
                time.sleep(1)
                return "Fail"
        
def create_user():

    while True:
        username = input("Enter username:")
        with sqlite3.connect("USERS.db") as db:
            cursor = db.cursor()
        find_user = ("SELECT * FROM user WHERE username = ?")
        cursor.execute(find_user,[(username)])
        
        if(cursor.fetchall()):
            again = input("This username already exists, do you want to try again? [y,n]")
            if(again.lower() == 'n'):
                print("Returning to main menu!!")
                time.sleep(1)
                return
        else:
            break
    password = input("Enter password:")
    print()
    password1 = input("Enter again your password:")
    while(password != password1):
        
        print("your passwords didn't match, try again")
        password = input("Enter password:")
        password1 = input("Enter again your password:")
    insertData = '''INSERT INTO user(username,password) VALUES(?,?)'''
    cursor.execute(insertData,[(username),(password)])
    db.commit()
    print()
    print("Successful registration!!")

def main_menu():
    while True:

        print("[1]- Login: ")
        print("[2]- Register")
        print("[3]- Exit")
        op = exception_option()
        if(op == '1'):
            username = login()
            if(username != "Fail"):
                print()
                print()
                print()
                transfer_files(username)
                break
        elif(op == '2'):
            create_user()
        else:
            print("Bye!!")
            time.sleep(1)
            break

def show_client_files(username):

    with sqlite3.connect("USERS.db") as db:
        cursor = db.cursor()
    find_file = ("SELECT files.filename, files.filesize FROM files INNER JOIN user ON files.user_id = user.userID AND user.username = ?;")
    cursor.execute(find_file,[(username)])
    results = cursor.fetchall()
    print("-------------- "+ username +" FILES -------------")

    if(len(results) != 0):
        for result in results:
            print("Name: ",result[0], " Size:", result[1]/1000000, "mb (",result[1],"bytes )")
    else:
        print("You don't have any files yet!!")
    
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
            print("Returning to menu!!")
            time.sleep(1)
            return [False,False]

def progress_bar(file_size):

    for i in tqdm(range(file_size)):
        i += 1024
    

def menu():

    print("[1]- Show available files: ")
    print("[2]- Upload")
    print("[3]- Close the program")


def upload_files(username):
    file, file_name = exception_files()

    if(not file):
        return
    aux_size = os.stat(file_name)

    aux_file_name = file_name.split("/")
    file_name = aux_file_name[-1]
    
    client_socket.send("Upload".encode())
    time.sleep(0.1)
    file_size = str(aux_size.st_size)
    client_socket.send(file_size.encode())
    time.sleep(0.2)
    client_socket.send(str(username[0][0]).encode())
    time.sleep(0.2)
    client_socket.send(username[0][1].encode())
    time.sleep(0.2)
    client_socket.send(file_name.encode())
    time.sleep(0.2)

    result = client_socket.recv(1024)
    
    if(result.decode() == "False"):
        client_socket.send(file.read(aux_size.st_size))
        progress_bar(aux_size.st_size)
        print("Successfully Uploaded!!")
        print()
        time.sleep(0.1)
    else:
        print("You have already uploaded this file!!")
    file.close()



def transfer_files(username):
    # Echo
    print("Bem-vindo: ", username[0][1])
    client_socket.connect(address)
    while True:
        try:
            menu()
            op = exception_option()
            if(op == '1'):
                show_client_files(username[0][1])
            elif(op == '2'):

                upload_files(username)
            elif (op == '3'):
                client_socket.send("Sair".encode())
                client_socket.close()
                break
        except:
            print("O servidor foi desativado.")
            client_socket.close()
            break
main_menu()