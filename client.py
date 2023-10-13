import socket
import sys
import errno

headerSize = 8
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    clientSocket.connect((socket.gethostname(), 6666))
except ConnectionRefusedError as e:
    print("Could not connect to server " + str(e))
    sys.exit()
clientSocket.setblocking(False)

username = input("Username > ").encode("utf-8")
usernameHeader = f"{len(username):<{headerSize}}".encode("utf-8")
clientSocket.send(usernameHeader + username)
clientUsername = username.decode("utf-8")

while True:
    message = input(f"{clientUsername} > ")
    if message:
        message = message.encode("utf-8")
        messageHeader = f"{len(message):<{headerSize}}".encode("utf-8")
        clientSocket.send(messageHeader + message)
    try:
        while True:
            usernameHeader = clientSocket.recv(headerSize)
            if not len(usernameHeader):
                print("Connection closed by the server.")
                sys.exit()
            usernameLength = int(usernameHeader.decode("utf-8"))
            username = clientSocket.recv(usernameLength).decode("utf-8")
            messageHeader = clientSocket.recv(headerSize)
            messageLength = int(messageHeader.decode("utf-8"))
            message = clientSocket.recv(messageLength).decode("utf-8")
            print(f"{username} > {message}")
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print("Reading error " + str(e))
            sys.exit()
        continue
    except Exception as e:
        print("General error " + str(e))
        sys.exit()
