"""
======================================================================
|   Client - Server Chat Room (server)
|
|   Name: server.py
|
|   Written by: Devon Ladd - February 2021 - 
|
|   Purpose: To allow multiple users to chat
|
|   usage: python3 server.py
|
|   Description of parameters:
|      n/a
|
|   Subroutines/libraries required:
|      See include statements
|
|------------------------------------------------------------------
"""

import errno
import socket
import sys
from threading import *

from helper import *

# Set up host and port
host = socket.getfqdn()
port = 53289

# Initialize client dictionary
client_socket_dict = {}

# Initialize socket
server_socket = socket.socket()
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((host, port))
server_socket.listen()

running = True

# Searches dictionary for value and returns key
def search_dict(value):
    for key in client_socket_dict:
        if client_socket_dict[key] == value:
            return key

# Determines type of message and deals with accordingly
def rout_message(message, client_socket):
    # unpack values
    packet_number, VERSION_NUMBER, from_name, to_name, verb, checksum, encrypted, text = unpack_message(message)

    # Evaluate checksum to determine message integrity
    while checksum != calculate_checksum(text, "server"):
        print("Checksums didn't match, requesting packet again...")
        # Request resending of message
        send_message("server", from_name, verb.RESEND, "Checksums didn't match, requesting packet again", client_socket)
        #Wait for response
        try:
            print("Waiting...")
            message = client_socket.recv(PACKET_SIZE)
            print("Received...")
        except:
            print("error")

        packet_number, VERSION_NUMBER, from_name, to_name, verb, checksum, encrypted, text = unpack_message(message)

    print("Checksums matched")
    send_message("server", from_name, verb.CONFIRM, "Checksums matched", client_socket)

    # login
    if verb == Verb.LOGIN:
        client_socket_dict[client_socket] = from_name

    print(f"From: {from_name}, To: {to_name}, Contents: {text}, Verb: {verb.name}")

    # message that will go to everyone
    if verb == Verb.BROADCAST or verb == Verb.LOGIN:
        for client_socket in client_socket_dict:
            send_message(from_name, to_name, verb, text, client_socket, encrypted=encrypted)
    # PM
    elif verb == Verb.PRIVATE_MESSAGE:
        print(f"{to_name}: {search_dict(to_name)}")
        ## Send the message to the person it's going to and the person it came from
        send_message(from_name, to_name, verb, text, search_dict(to_name), encrypted=encrypted)
        send_message(from_name, to_name, verb, text, search_dict(from_name), encrypted=encrypted)
    # who
    elif verb == Verb.WHO:
        who_string = ", ".join(client_socket_dict.values())
        print(who_string)
        send_message(from_name, "server", verb, who_string, client_socket)
    # Client disconnecting
    elif verb == Verb.QUIT:
        print(f"{from_name} disconnected.\n")
        client_socket_dict.pop(client_socket)
        client_socket.close()
        for client_socket in client_socket_dict:
            print(f"Sending disconnect message to {to_name}")
            send_message(from_name, to_name, verb, text, client_socket)


# Waits for message from client
def listen_to_client(client_socket):
    thread_running = True
    while thread_running:
        try:
            # Try to receive and route message
            message = client_socket.recv(PACKET_SIZE)
            rout_message(message, client_socket)
        except OSError as e: # catch when client disconnects
            if e.errno == errno.EBADF:
                print("DISCONNECTED")
                client_socket.close()
                thread_running = False
            else:
                raise
        except Exception as e:
            # Other errors
            print("=====================\n"
                 f"Error: {e}\n"
                  "=====================\n")
            thread_running = False
    print(f"No longer listening to {client_socket}")

def close_safely():
    print("Messaging all clients...")
    for client_socket in client_socket_dict:
        send_message("server", "all", Verb.SHUTDOWN, "Server shutting down...", client_socket)
    print("Closing all sockets...")
    for socket in client_socket_dict:
        socket.close()

    server_socket.close

    print("Done. Goodbye.")
    sys.exit()

try:
    # Loops while running, connects new clients
    while(running):
        # accept connections
        client_socket, client_address = server_socket.accept()
        # send a connection message
        rout_message(client_socket.recv(PACKET_SIZE), client_socket)
        # Daemon to listen to client
        listen_thread = Thread(target=listen_to_client,
                            args=(client_socket,), daemon=True)
        listen_thread.start()
except KeyboardInterrupt:
    close_safely()
