def rot13(message: str):
    out = ""
    for c in message:
        new_val = ord(c) + 13
        if new_val>126:
            new_val = new_val - 95
        out = out + chr(new_val)
    return(out)

def unrot13(message: str):
    out = ""
    message.strip('\x00')
    for c in message:
        if ord(c) != 0:
            new_val = ord(c) - 13
            if new_val<32:
                new_val = new_val + 95
            out = out + chr(new_val)
    return(out)

def rot_test():
    # test = '!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'
    # test = " !\"#$%&'()*+,-./012345"
    test = "mnopqrstuvwxyz{|}~"
    encode = rot13(test)
    print(encode)
    decode = unrot13(encode)
    print(decode)
    print(test==decode)
