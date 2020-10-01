

"""
Description: It is a basic CLI based chat application. Clients will send and receive chat messages
from the command line interface. Client will give their unique User Name in the Command Prompt and their message
will be recorded in a Dictionary.

Project Name: Python Chat App
Developed By: Brotecs Technology Limited.
Created : 01/10/2020
Updated : 01/10/2020 [Khandaker Habibul Amin Nabil]

For Suggestion and Query please mail to info@brotecs.com
"""


import socket
import sys
# import threading
# from datetime import datetime, timedelta

# needed constant value for socket connection
HEADER = 64
PORT = 1234
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "DISCONNECT!"
INITIATE_MESSAGE = "START"
TORRENT = "torrent"

class Client:

    # using constructor to initialize values
    """
    Function __init__ is the constructor of Client Class. It will initialize all the needed values.
    Input Parameters : valueOne->object;
    """
    def __init__(self):
        try:
            # taking input from command line prompt
            # and checking the value that it is empty or not
            # sys.argv[0] used for script/file name and sys.argv[1] used for 1st command line argument passed to it
            # as we take username input just after the script/file name so we are using sys.argv[1]
            self.user_name = sys.argv[1].replace(" ", "")

            if not self.user_name:
                raise ValueError("Username cannot be empty, give a valid name ")
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(ADDR)

        except Exception as e:
            print(e)
            # if got error then exit the program
            sys.exit()

    # work for sending msg to server
    """
    Function send is used for sending messages from client command prompt to server command prompt.
    Input Parameters : valueOne->object, valueOne-> string;
    """
    def send(self, msg):
        try:
            # storing user name
            user_name = self.user_name

            # saving username and whole msg in a string and encoded it
            message = f"{user_name} {msg}".encode(FORMAT)

            # saving length of the encoded message
            msg_length = len(message)

            # encoding the msg_length after converting it into string
            send_length = str(msg_length).encode(FORMAT)

            # if send_lenght length is less than HEADER length then
            # it can create problem that is why send_length length
            # is subtracted from HEADER length then if any space is empty
            # it will be filled up by ' '
            send_length = send_length + b' ' * (HEADER - len(send_length))

            # sending the length
            self.client.send(send_length)

            # sending the encoded message
            self.client.send(message)

            # client will listen now
            self.listen()

        except Exception as e:
            print(e)

    """
    Function listen is used for receiving messages from server to client command prompt. As well as it will
    check for unique User Name.
    Input Parameters : valueOne->object;
    """
    def listen(self):
        # client will receive 1024 byte size message
        msg = self.client.recv(1024)

        # decoding the message
        msg = msg.decode(FORMAT)

        # checking for unique username
        if msg != "Valid":
            print(msg)
            if msg == "This username is not available":
                # closing connection
                self.client.close()
                sys.exit()


# executing client file
if __name__ == "__main__":
    # creating Client object
    client1 = Client()

    # sending START msg so that client can initiating messaging
    client1.send(INITIATE_MESSAGE)

    # taking command line message input from client
    while True:
        client1.send(str(input()))

