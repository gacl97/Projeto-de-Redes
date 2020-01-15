import socket
import os
import sqlite3
import time
from tqdm import tqdm
from getpass import getpass

address = ('localhost', 2036)

# Create sockets
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def login():


    while True:

        clear()
        
        print("------------- User Login -------------")
        print()
        username = input("Enter username: ")
        print()
        password = getpass("Enter password: ")
        print()
        with sqlite3.connect("USERS.db") as db:
            cursor = db.cursor()
        find_user = ("SELECT * FROM user WHERE username = ? AND password = ?")
        cursor.execute(find_user,[(username),(password)])
        results = cursor.fetchall()

        if(results):
            clear()
            print("Login successfully!")
            time.sleep(0.2)
            return results
        else:
            print("Username or password is incorrect!")
            again = input("Do you want to try again? [y/n]")
            if(again.lower() == 'n'):
                clear()
                print("Returning to main menu!!")
                print()
                print()
                time.sleep(0.2)
                return "Fail"
        
def create_user():

    while True:
        clear()
        print("------------- User registration -------------")
        print()

        username = input("Enter username: ")
        with sqlite3.connect("USERS.db") as db:
            cursor = db.cursor()
        find_user = ("SELECT * FROM user WHERE username = ?")
        cursor.execute(find_user,[(username)])
        
        if(cursor.fetchall()):
            clear()
            again = input("This username already exists, do you want to try again? [y,n]")
            if(again.lower() == 'n'):
                clear()
                print("Returning to main menu!!")
                time.sleep(1)
                return
        else:
            break
    print()
    password = input("Enter password: ")
    print()
    password1 = input("Enter again your password: ")

    while(password != password1):
        print("Your passwords didn't match, try again!!")
        password = input("Enter password: ")
        password1 = input("Enter again your password: ")
        
    insertData = '''INSERT INTO user(username,password) VALUES(?,?)'''
    cursor.execute(insertData,[(username),(password)])
    db.commit()
    print()
    clear()
    print("Successful registration!!")
    print()
    print()
    time.sleep(0.2)

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
            clear()
            print("Returning to menu!!")
            print()
            time.sleep(1)
            return [False,False]
        clear()

def progress_bar(file_size):

    for i in tqdm(range(file_size)):
        i += 1024
    
def main_menu():
    while True:

        print("[1]- Login: ")
        print("[2]- Register")
        print("[3]- Close the program")
        op = exception_option()
        if(op == '1'):
            username = login()
            if(username != "Fail"):
                print()
                transfer_files(username)
                break
        elif(op == '2'):
            create_user()
        else:
            print("Bye!!")
            time.sleep(1)
            break

def menu():

    print("[1]- Show available files: ")
    print("[2]- Upload")
    print("[3]- Download")
    print("[4]- Log out")


def upload_files(username):

    print("------------- Upload File -------------")
    print()
    file, file_name = exception_files()

    if(not file): 
        return
    aux_size = os.stat(file_name)

    # Diretório
    aux_file_name = file_name.split("/")
    file_name = aux_file_name[-1]
    
    client_socket.send("Upload".encode())
    time.sleep(0.2)
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
        clear()
        print("Successfully Uploaded!!")
        print()
        print()
        time.sleep(0.1)
    else:
        clear()
        print("You have already uploaded this file!!")
        print()
        print()
        time.sleep(0.1)
    file.close()


def download_files(username):

    show_client_files(username[0][1])
    print()
    client_socket.send("Download".encode())
    file_name = input("Enter the file name: ")

    client_socket.send(str(username[0][1]).encode())
    time.sleep(0.1)
    client_socket.send(file_name.encode())
    time.sleep(0.1)
    
    result = client_socket.recv(1024)

    if(result.decode() == "False"):
        print("File not found!!")
        print()
        time.sleep(0.2)
        return

    file_size = int(client_socket.recv(1024).decode())

    client_folder = os.getcwd() + "/Download " + username[0][1] + "/" + file_name

    aux_size = 0
    
    new_file = open(client_folder,'wb')

    while aux_size < file_size:
        data = client_socket.recv(1024)
        new_file.write(data)
        aux_size += len(data)
        
    new_file.close()
    clear()
    print("Downloaded successfully, your file is in your folder!!")
    print()
    print()
    time.sleep(0.2)


  
def clear():
    
    os.system('cls' if os.name == 'nt' else 'clear')


def transfer_files(username):

    print("-----------------------------")
    print()
    print("Welcome: ", username[0][1])
    print()
    print("-----------------------------")
    client_socket.connect(address)
    while True:
        try:
            menu()
            op = exception_option()
            if(op == '1'):
                clear()
                show_client_files(username[0][1])
            elif(op == '2'):
                clear()
                upload_files(username)
            elif(op == '3'):
                clear()
                download_files(username)
            elif (op == '4'):
                client_socket.send("Sair".encode())
                print("Bye!!")
                time.sleep(0.5)
                client_socket.close()
                break
        except:
            print("The server has been disabled.")
            client_socket.close()
            break
main_menu()