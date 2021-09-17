"""
======================================================================
|   Client - Server Chat Room (client)
|
|   Name: client.py
|
|   Written by: Devon Ladd - February 2021
|
|   Purpose: To allow multiple users to chat
|
|   usage: python3 client.py
|          then input usename when requested
|
|   Description of parameters:
|      n/a
|
|   Subroutines/libraries required:
|      See include statements
|
|------------------------------------------------------------------
"""

import random
import socket
import sys
from select import select
from threading import *

from encrypt import *
from helper import *

# Set up host / server
host = socket.getfqdn()
port = 53289
# get client username
name = input("Username: ")

# connect to server
client_socket = socket.socket()
client_socket.connect((host, port))
client_socket.setblocking(0)

running = True

# Buffer holding last message sent
last_message = tuple

# Waits for a message from the server and then outputs it accordingly
def receive_messages():
    while running:
        try:
            ready = select.select([client_socket], [], [])
            if ready[0]:
                message = client_socket.recv(PACKET_SIZE)
        except Exception as e:
            print("=====================\n"
                  f"Error: {e}\n"
                  "=====================\n")

        try:
            # Unpack values
            packet_number, VERSION_NUMBER, from_name, to_name, verb, checksum, encrypted, text = unpack_message(
                message)
        except:
            debug_log(f"\nCLIENT ERROR:\n\t{message}")
        
        # If the message says it's encrypted
        if encrypted:
            #Dencrypt it
            text= unrot13(text)
        # If it's a message, print in form
        if verb == Verb.BROADCAST or verb == Verb.PRIVATE_MESSAGE:
            print(f"\nTO: {to_name}\nFROM: {from_name}\n{text}\n")
        # If it's a notification (just text) print text
        elif verb == Verb.LOGIN or verb == Verb.QUIT or verb == Verb.WHO:
            print(f"\n{text}\n")
        # Let user know that the message was properly delivered
        elif verb == Verb.CONFIRM:
            print("Message confirmed")
        # Resend last message if it was requested
        elif verb == Verb.RESEND:
            send_message(last_message[0], last_message[1],
                         last_message[2], last_message[3], last_message[4], encrypted=True)
        # Server tells all clients to shutdown 
        elif verb == Verb.SHUTDOWN:
            print("Server shut down")
            client_socket.close()
            sys.exit()
        elif verb == Verb.ERROR:
            print("Server had an issue")

# Let the server know the client is closing and close socket
def client_quit():
    print("See ya")
    if client_socket:
        send_message(name, "ALL", Verb.QUIT,
                        f"{name} has disconnected.", client_socket)
        client_socket.close()

# Tell server client connected
send_message(name, "ALL", Verb.LOGIN, f"{name} has connected.", client_socket)
last_message = (name, "ALL", Verb.LOGIN,
                f"{name} has connected.", client_socket)

# Create and start daemon thread
receive_messages_thread = Thread(target=receive_messages, daemon=True)
receive_messages_thread.start()
print("Connected")

try:
    # loops while client still connected
    while running:
        # client input
        value = input("")
        # disconnect
        if value.lower() == "bye":
            client_quit()
            running = False
        # who
        elif value.lower() == "who":
            # do stuff
            send_message(name, "ALL", Verb.WHO, "", client_socket)
        # messages
        else:
            try:
                # get command and message
                split_value = value.split(":", 1)
                # all message
                if split_value[0].lower() == "all":
                    verb = Verb.BROADCAST
                # PM
                else:
                    verb = Verb.PRIVATE_MESSAGE

                # Simulate packet degeneration
                modified = False
                if random.random() >= 0.5:
                    modified = True

                #Encrypt it
                split_value[1] = rot13(split_value[1])

                # Save message and to server
                last_message = (
                    name, split_value[0], verb, split_value[1], client_socket)

                send_message(name, split_value[0],
                            verb, split_value[1], client_socket, encrypted=True, modified=modified)
            # Typed something else
            except:
                print("That is not a valid command / message")
except KeyboardInterrupt:
    client_quit()
