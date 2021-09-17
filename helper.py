"""
======================================================================
|   Client - Server Chat Room (helper)
|
|   Name: helper.py
|
|   Written by: Devon Ladd - February 2021
|
|   Purpose: To allow multiple users to chat
|
|   usage: from helper import *
|
|   Description of parameters:
|      n/a
|
|   Subroutines/libraries required:
|      See include statements
|
|------------------------------------------------------------------
"""
import select
import struct
import time
from collections import namedtuple
from enum import IntEnum

# Version number for assignment 4
VERSION_NUMBER = 4

PACKET_TUPLE = int, int, str, str, IntEnum, int, str

# Defines the values in the packet
PACKET_FORMAT = "i i 32s 32s i i ? 256s"

PACKET_SIZE = 337

TIMEOUT = 0.5

# Verb enum
class Verb(IntEnum):
    ERROR = 0
    BROADCAST = 1
    PRIVATE_MESSAGE = 2
    WHO = 3
    LOGIN = 4
    QUIT = 5
    RESEND = 6
    CONFIRM = 7
    SHUTDOWN = 8

def debug_log(log):
    print("Debug log updated")
    f = open("./output.log", "a")
    format = "%d/%m/%Y %H:%M:%S"
    f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}] {log}")
    f.close()

def calculate_checksum(text, from_name):
    checksum = 0
    for c in text:
        checksum += int(ord(c))

    return checksum

# Standardized way to send messages between client and server
def send_message(from_name, to_name, verb, text, socket, encrypted=False, packet_number=1, modified=False):
    if modified:
        print(f"Message from will have the wrong checksum")
        checksum_mod = 1
    else:
        checksum_mod = 0

    # packs all values into a struct and sends to socket
    header = struct.pack(PACKET_FORMAT, packet_number, VERSION_NUMBER, from_name.encode(
        'utf-8'), to_name.encode('utf-8'), int(verb), calculate_checksum(text, from_name)+checksum_mod, encrypted, text.encode('utf-8'))

    socket.send(header)



# Standardized way to unpack received messages
def unpack_message(message):
    # If unpacking fails, throw error
    try:
        packet_number, vn, from_name, to_name, verb, checksum, encrypted, text = struct.unpack(
            PACKET_FORMAT, message)
        text = text.decode('utf-8')
        from_name = from_name.decode('utf-8')
        to_name = to_name.decode('utf-8')
        verb = Verb(verb)
    except Exception as e:
        debug_log(f"\nUNPACK ERROR:\n{e}\n\t{message}")
        packet_number = 0
        vn = 0
        checksum = 0
        text = "ERROR"
        from_name = "ERROR"
        to_name = "ERROR"
        verb = Verb(0)
        raise ValueError("WEIRD MESSAGE TERMINATE SOCKET CONNECTION")

    return packet_number, vn, from_name, to_name, verb, checksum, encrypted, text
