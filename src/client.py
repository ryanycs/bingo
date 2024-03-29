from utils import *
from colors import *
import socket


def print_card(card, card_status):
    print('+----------------+')
    for i in range(5):
        print('| ', end='')
        for j in range(5):
            if card_status[i*5+j]:
                print(fgRed + '{:2s}'.format(card[i*5+j]) + endColor, end=' ')
            else:
                print('{:2s}'.format(card[i*5+j]), end=' ')
        print('|')
    print('+----------------+')


def client(network, port):
    # create socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # set bingo list
    card_status = [False] * 25
    
    # prompt
    print(fgYellow + """
______ _                   
| ___ (_)                  
| |_/ /_ _ __   __ _  ___  
| ___ \ | '_ \ / _` |/ _ \ 
| |_/ / | | | | (_| | (_) |
\____/|_|_| |_|\__, |\___/ 
                __/ |      
               |___/       
            """ + endColor)
    name = input('Enter your name to join the game: ')
    card = get_card()
    text = name + ',' + ','.join([i for i in card])

    # print bingo card
    print()
    print(f'Hello {name}. Here is your bingo card:')
    print_card(card, card_status)

    # send name & numbers to server
    sock.sendto(text.encode('ascii'), (network, port))

    # receive user_id & start_sec from server
    data, address = sock.recvfrom(MAX_BYTES)
    user_id, start_sec = data.decode('ascii').split(',')
    print(f"You are the {user_id} player in the game.")
    print(f"Game will be started in {start_sec} second(s).")

    data, address = sock.recvfrom(MAX_BYTES)
    message = data.decode('ascii')
    print(message)   

    # start listen to server to get the lucky number
    while True:
        data, address = sock.recvfrom(MAX_BYTES)
        message = data.decode('ascii')
        
        if message.split(',')[0] == 'Bingo': # someone has bingo, game over
            # print('Somebody has Bingo. Game Over!')
            print(fgMagenta + message + endColor) # who wins
            print("Game Over.")
            break
        elif message == "Game Over!":
            print("Game Over. No one wins.")
            break
        else: # message is digit
            if message in card:
                idx = card.index(message)
                card_status[idx] = True
                print(message) # card number the server send this time
                print_card(card, card_status)
            
            if check(card_status): # Bingo!        
                sock.sendto('Bingo'.encode('ascii'), (network, port))
                # server check
                data, address = sock.recvfrom(MAX_BYTES)
                message = data.decode('ascii')
                print(message)
                if message == "You are wrong.":
                    continue
                else:
                    print(bgYellow +'Bingo! You win!' + endColor) 
                    break
