import socket
import threading

HOST = 'localhost'
PORT = 9900

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []
nicknames = []

#broadcast
def broadcast(message):
    for client in clients:
        client.send(message)

#handle
def handle(client):
    while True:
        try: 
            message = client.recv(1024).decode('utf-8')
            print(f'{message}')
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close() 
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break

#receive
def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024)
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client : {nickname}')
        broadcast(f'{nickname} is connected to the server\n'.encode('utf-8'))
        client.send("Connected to the server\n".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

if __name__ == '__main__':
    print("Server is running...")
    receive()