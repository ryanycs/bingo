import socket

MAX_BYTES = 65535

def reclient(text, num):
    
    numlist = []
    name = text.split(',')[0]
    for i in range(0,25):
        numlist.append(text.split(',')[i+1])

    message = name + ", You are the " + num + 'player\n'
    return message


def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((interface, port))
    print('Listening at', sock.getsockname())
    delay = 5.0  # seconds
    sock.settimeout(delay)
    num = 1
    #while True:
    try:
        data, address = sock.recvfrom(MAX_BYTES)
        text = data.decode('ascii')
        print(text)
        message = reclient(text, num)
        
        sock.sendto(message.encode('ascii'), address)
        
        num +=1
    except socket.timeout as exc:
        print('Timeout: I did not receive any message.')


