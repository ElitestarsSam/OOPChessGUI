import select
import socket
import pickle

headerSize = 8

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((socket.gethostname(), 6666))
serverSocket.listen()
socketList = [serverSocket]
clients = {}


def receiveMessage(clientSocket):
    try:
        messageHeader = clientSocket.recv(headerSize)
        if not len(messageHeader):
            return False
        messageLength = int(messageHeader.decode("utf-8"))
        return {"header": messageHeader, "data": clientSocket.recv(messageLength)}
    except:
        return False


while True:
    readSockets, _, exceptionSockets = select.select(socketList, [], socketList)
    for notifiedSocket in readSockets:
        if notifiedSocket == serverSocket:
            clientSocket, clientAddress = serverSocket.accept()
            user = receiveMessage(clientSocket)
            if not user:
                continue
            socketList.append(clientSocket)
            clients[clientSocket] = user
            print(
                f"Accepted new connection from {clientAddress[0]}:{clientAddress[1]}, Username: {user['data'].decode('utf-8')}")
        else:
            message = receiveMessage(notifiedSocket)
            if not message:
                print(f"Closed connection from {clients[notifiedSocket]['data'].decode('utf-8')}")
                socketList.remove(notifiedSocket)
                del clients[notifiedSocket]
                continue
            user = clients[notifiedSocket]
            print(f"Received message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")
            for clientSocket in clients:
                if clientSocket != notifiedSocket:
                    clientSocket.send(user['header'] + user['data'] + message['header'] + message['data'])
    for notifiedSocket in exceptionSockets:
        socketList.remove(notifiedSocket)
        del clients[notifiedSocket]
