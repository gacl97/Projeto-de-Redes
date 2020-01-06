import socket
import os
import sqlite3
import time

address = ('localhost', 7401)

# Create sockets
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(address)

def login():
    while True:

        username = input("Enter username:")
        password = input("Enter password:")
        with sqlite3.connect("USERS.db") as db:
            cursor = db.cursor()
        find_user = ("SELECT * FROM user WHERE username = ? AND password = ?")
        cursor.execute(find_user,[(username),(password)])
        results = cursor.fetchall()

        if(results):
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
            again = input("This username already exists, do you want to try again?(y,n)")
            if(again.lower() == 'n'):
                print("Returning to main menu!!")
                time.sleep(1)
                return
        else:
            break
    password = input("Enter password:")
    password1 = input("Enter again your password:")
    while(password != password1):
        
        print("your passwords didn't match, try again")
        password = input("Enter password:")
        password1 = input("Enter again your password:")
    insertData = '''INSERT INTO user(username,password) VALUES(?,?)'''
    cursor.execute(insertData,[(username),(password)])
    db.commit()
    print("Successful registration!!")


def menu():
    while True:

        print("[1]- Login: ")
        print("[2]- Register")
        print("[3]- Exit")
        op = input()
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



def transfer_files(username):
    # Echo
    print("Bem-vindo: ", username[0][1])
    while True:
        try:

            text = input("Informe o arquivo: ")
            file = open(text,"rb")
            aux_size = os.stat(text)
            file_size = str(aux_size.st_size)
            client_socket.send(file_size.encode())
            time.sleep(0.5)
            client_socket.send(text.encode())
            client_socket.send(file.read(aux_size.st_size))
            file.close()
            if (text == "sair"):
                client_socket.close()
                break
        except:
            print("O servidor foi desativado.")
            client_socket.close()
            break
menu()