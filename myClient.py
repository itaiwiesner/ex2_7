import myProtocol
import protocol
import socket
import os


IP = '127.0.0.1'
# The path + filename where the copy of the screenshot at the client should be saved
SAVED_PHOTO_LOCATION = f'{os.path.abspath(os.getcwd())}\\received.jpg'
print(SAVED_PHOTO_LOCATION)
# optional working commands:
# DIR D:/PycharmProjects
# DELETE D:/delete_me
# COPY D:/file.txt D:/dest
# EXECUTE C:\ProgramData\Microsoft\Windows\StartMenu\Programs\Word2016.lnk


def handle_server_response(my_socket, cmd):
    """
    Receive the response from the server and handle it, according to the request
    For example, DIR should result in printing the contents to the screen,
    Note- special attention should be given to SEND_PHOTO as it requires and extra receive
    """
    command = cmd.split()[0]
    params = cmd.split()[1:]
    # (8) treat all responses except SEND_PHOTO
    length = int(my_socket.recv(4).decode())
    data = my_socket.recv(length).decode()
    # (10) treat SEND_PHOTO
    if command == 'SEND_PHOTO':
        print(data)
        data = int(data)
        with open(SAVED_PHOTO_LOCATION, 'wb') as f:
            image_chunk = my_socket.recv(data)
            f.write(image_chunk)

    else:
        print(data)


def main():
    # open socket with the server

    # (2)

    my_socket = socket.socket()
    my_socket.connect(("127.0.0.1", 8820))

    # print instructions
    print('Welcome to remote computer application. Available commands are:\n')
    print('TAKE_SCREENSHOT\nSEND_PHOTO\nDIR\nDELETE\nCOPY\nEXECUTE\nEXIT')

    # loop until user requested to exit
    is_exit = False
    while not is_exit:
        cmd = input("Please enter command:\n")
        # check if the command is according to the protocol
        if protocol.check_cmd(cmd):
            my_socket.send(myProtocol.get_len(cmd).encode())
            my_socket.send(cmd.encode())
            if cmd == 'EXIT':
                is_exit = True
            else:
                handle_server_response(my_socket, cmd)

        else:
            print('Not a valid command, or missing parameters')

    my_socket.close()


if __name__ == '__main__':
    main()
