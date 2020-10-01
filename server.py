

"""
Description: It is a basic CLI based chat application. Clients will send and receive chat messages
from the command line interface. Client will give their unique User Name in Command Prompt and their message
will be recorded in a Dictionary.

Project Name: Python Chat App
Developed By: Brotecs Technology Limited.
Created : 01/10/2020
Updated : 01/10/2020 [Khandaker Habibul Amin Nabil]

For Suggestion and Query please mail to info@brotecs.com
"""


import socket
import threading
import logging
import json
from datetime import datetime, timedelta

# needed constant value for socket connection
HEADER = 64
PORT = 1234
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "DISCONNECT!"
INITIATE_MESSAGE = "START"
TORRENT = "torrent"


class Server:

    # using constructor to initialize values

    """
    Function __init__ is the constructor of Server Class. It will initialize all the needed values.
    Input Parameters : valueOne->object;
    """

    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADDR)

        # for tracking user torrent info
        self.trackerUser = {}

        # for tracking user message info
        self.trackerUserMsg = {}

        # key in the trackerUserMsg dictionary and store message value
        self.countMsg = 1

        # storing json data in the dictionary
        self.json_object = {}

        # key in the json_object dictionary and store json value
        self.count = 1

    """
    Function handle_client is basically take connection , address and self object. handle_client is used for 
    handling each client who can send their message to server and server will print those 
    User Name with their message in the server command prompt.
     
    Input Parameters : valueOne->object, valueTwo->socket object, 
    valueThree-> address is the address bound to the socket on the other end of the connection;
    
    """

    def handle_client(self, conn, addr):
        user = None

        # using user_Name variable for checking unique user name letter
        user_name = False

        connected = True
        while connected:
            msg_length = conn.recv(HEADER).decode(FORMAT)

            # creating log file
            logging.basicConfig(filename='test.log', level=logging.DEBUG,
                                format='%(asctime)s: %(levelname)s: %(message)s')

            user = ""

            # checking if user send any message or not
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)

                # using split method to ge the user name from received message
                # user name insider user
                user = msg.split()[0]

                # using split method to ge the message from received message
                # message body inside msg
                msg = " ".join(msg.split()[1:])

                # checking that user giving any json data or not
                # if given then saving it to dictionary with serial index
                try:
                    if json.loads(msg):
                        self.json_object[self.count] = json.loads(msg)
                        self.count = self.count + 1
                        print(self.json_object)
                    else:
                        pass

                except Exception as e:
                    pass

                # if user_Name still false then we will check that
                # user name is in the trackerUser dictionary or not
                # if not then we will allow
                # if it is in the dictionary then we will not allow client
                # and close the connection for client
                if not user_name:
                    if user in self.trackerUser:
                        conn.send(
                            bytes("This username is not available", FORMAT))
                        conn.close()
                        return
                    user_name = True
                    self.trackerUser[user] = {}
                    self.trackerUserMsg[user] = {}
                    print(f"New Connection ---- {addr} connected")

                # initiating messaging
                if msg == INITIATE_MESSAGE:
                    conn.send(bytes("Welcome to the server", FORMAT))

                # checking that user is blocked for sending torrent file for 3 times or not
                elif "blocked" in self.trackerUser[user]:
                    # checking how much time left to unblock an user
                    difference = (self.trackerUser[user]["blocked"] - datetime.now()).total_seconds()

                    conn.send(bytes("You are blocked now. Wait 10 mins", FORMAT))

                    # checking that if user waited for 10 min or not
                    # and also checking that message does not contain any torrent
                    # if waited for 10 min then server will set user value to empty {}
                    # then user can chat again
                    if difference <= 0 and msg != "torrent":
                        print(f"{user} are now free to chat again ")
                        conn.send(bytes("You is now free to chat again ", FORMAT))

                        # self.trackerUser[user] value set to empty
                        # and previous "blocked" word removed
                        self.trackerUser[user] = {}


                        # sending Valid word so that message does not go to username collision condition
                        conn.send(bytes("Valid", FORMAT))

                        # storing the msg from user in dictionary
                        self.trackerUserMsg[user][self.countMsg] = msg
                        self.countMsg = self.countMsg + 1
                        # print(self.trackerUserMsg)

                        # printing msg in the server console
                        print(f"{user} --> {msg}")

                elif msg == DISCONNECT_MESSAGE:
                    connected = False

                # checking torrent keyword in msg
                elif "torrent" in msg:

                    # checking 1st time entry of torrent keyword
                    if "torrent1" not in self.trackerUser[user]:

                        # saving current time in user tracker so that we can
                        # calculating the time difference when 1st torrent keyword has been entered
                        self.trackerUser[user]["torrent1"] = datetime.now()

                        conn.send(bytes("You cannot provide any torrent link or files, you attempted once", FORMAT))
                        logging.debug(f" {user} sent a torrent link 1 times ")

                    # checking 2nd time entry of torrent keyword
                    elif "torrent2" not in self.trackerUser[user]:

                        # updating the difference between 1st time torrent keyword entered
                        # difference_Time value converting into seconds with total_seconds()
                        difference = (datetime.now() - self.trackerUser[user]["torrent1"]).total_seconds()

                        # checking that user entered 2nd torrent file or link
                        # after 5 min or not, if entered 2nd torrent after 5 min
                        # then it will work as same torrent1
                        if difference > 5: # 60 * 5 min er jonno
                            self.trackerUser[user] = {"torrent1": datetime.now()}

                            conn.send(bytes("You cannot provide any torrent link or files, you attempted once", FORMAT))
                            logging.debug(f" {user} sent a torrent link 1 times ")

                        # otherwise if its between 5 min then it will
                        # updated as torrent2 and its entry time
                        else:
                            self.trackerUser[user]["torrent2"] = datetime.now()

                            conn.send(bytes("You cannot provide any torrent link or files, you attempted twice", FORMAT))
                            logging.debug(f" {user} sent a torrent link 2 times ")

                    # checking 3rd time entry of torrent keyword
                    elif "torrent3" not in self.trackerUser[user]:

                        # updating the difference between 1st time torrent keyword entered
                        difference = (datetime.now() - self.trackerUser[user]["torrent1"]).total_seconds()

                        # checking that user entered 3rd torrent file or link
                        # after 5 min or not, if entered 3rd torrent after 5 min
                        # then it will work as same torrent1
                        if difference > 5: # 60 * 5 min er jonno
                            self.trackerUser[user] = {"torrent1": datetime.now()}

                            conn.send(bytes("You cannot provide any torrent link or files, you attempted once", FORMAT))
                            logging.debug(f" {user} sent a torrent link 1 times ")

                        # otherwise if its between 5 min then it will
                        # updated as torrent3 and its entry time and
                        # blocked the user for next 10 min with timedelta function
                        else:
                            self.trackerUser[user]["torrent3"] = datetime.now()

                            # set the block time value for next 10 min with current time and timedelta function
                            self.trackerUser[user]["blocked"] = datetime.now() + timedelta(seconds=10) # minutes=10 min er jonno dibo

                            conn.send(bytes("You cannot provide any torrent link or files, you attempted 3 times "
                                            "and your id is blocked for 10 min", "utf-8"))
                            logging.debug(f" {user} sent a torrent link 3 times ")

                # else it is a normal message and server will allow it
                else:
                    conn.send(bytes("Valid", FORMAT))
                    self.trackerUserMsg[user][self.countMsg] = msg
                    self.countMsg = self.countMsg + 1
                    # print(self.trackerUserMsg)
                    print(f"{user} --> {msg}")

        # closing connection
        self.closeConnection(conn, user)

    """
    Function start is  used for starting the server and using Threading for handling multiple client. 
    Input Parameters : valueOne->object;
    """

    def start(self):
        try:
            self.server.listen()
            print(f"Server is listening on {SERVER}")
            while True:
                conn, addr = self.server.accept()
                thread = threading.Thread(target=self.handle_client, args=(conn, addr))

                thread.start()

        except Exception as e:
            print(e)

    """
    Function closeConnection is  used for closing connection from server to client. Client will be disconnected.
    Input Parameters : valueOne->object, valueTwo->socket object, 
    valueThree-> address is the address bound to the socket on the other end of the connection;
    """

    def closeConnection(self, conn, user):
        # closing connection
        conn.close()
        # deleting user history from trackUser dictionary
        del self.trackerUser[user]
        print(f"{user} Disconnected from the server")


# executing server file
if __name__ == "__main__":
    # creating Server object
    server1 = Server()
    print("Server is starting...")

    # starting the connection with client
    server1.start()
