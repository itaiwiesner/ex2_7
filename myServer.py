
import socket
import glob
import os
import shutil
from PIL import Image
import pyautogui
import myProtocol

IP = '127.0.0.1'
PHOTO_PATH = f'{os.path.abspath(os.getcwd())}\\screenshot.jpg'


def check_client_request(cmd):
    """
    Break cmd to command and parameters
    Check if the command and params are good.

    For example, the filename to be copied actually exists

    Returns:
        valid: True/False
        command: The requested cmd (ex. "DIR")
        params: List of the cmd params (ex. ["c:\\cyber"])
    """
    # (6)

    # Use protocol.check_cmd first
    if not myProtocol.check_cmd(cmd):
        return False, '', []
    # Then make sure the params are valid
    data = cmd.split()
    command = data[0]
    params = data[1:]

    # commands which requires no params
    if command == 'EXIT' or command == 'TAKE_SCREENSHOT':
        return True, command, params

    if command == 'DIR':
        try:
            glob.glob(params[0])

        except Exception:
            return False, command, params

        else:
            return True, command, params

    if command == 'DELETE':
        if os.path.exists(params[0]):
            return True, command, params
        return False, command, params

    if command == 'EXECUTE':
        try:
            os.startfile(params[0])

        except Exception:
            return False, command, params

        else:
            return True, command, params

    if command == 'COPY':
        try:
            shutil.copy(params[0], params[1])

        except Exception:
            return False, command, params

        else:
            if os.path.isdir(params[1]):
                return True, command, params
            return False, command, params

    if command == 'SEND_PHOTO':
        try:
            # check if path is an image
            _ = Image.open(PHOTO_PATH)

        except Exception:
            return False, command, params

        else:
            return True, command, params

    return False, command, params


def handle_client_request(command, params=[]):
    """Create the response to the client, given the command is legal and params are OK

    For example, return the list of filenames in a directory
    Note: in case of SEND_PHOTO, only the length of the file will be sent

    Returns:
        response: the requested data

    """

    # (7)
    if command == 'DIR':
        path = params[0] + r'\*.*'
        return ''.join(glob.glob(path))

    if command == 'COPY':
        shutil.copy(params[0], params[1])
        return 'COPIED successfully'

    if command == 'DELETE':
        if os.path.isfile(params[0]):
            os.remove(params[0])
        elif os.path.isdir(params[0]):
            shutil.rmtree(params[0])
        return 'DELETED successfully'

    if command == 'EXECUTE':
        os.startfile(params[0])
        return 'EXECUTED successfully'

    if command == 'TAKE_SCREENSHOT':
        image = pyautogui.screenshot()
        image.save(PHOTO_PATH)
        return 'SCREEN SHOT was taken successfully'

    if command == 'SEND_PHOTO':
        if os.path.exists(PHOTO_PATH):
            return str(os.path.getsize(PHOTO_PATH))


def main():
    # open socket with client

    # (1)
    server_socket = socket.socket()
    server_socket.bind(("0.0.0.0", 8820))
    server_socket.listen(1)
    print("Server is up and running")
    client_socket, client_address = server_socket.accept()
    print("Client connected")

    is_exit = False
    while not is_exit:
        length = int(client_socket.recv(4).decode())
        data = client_socket.recv(length).decode()

        # check if the command is according to the protocol
        # if myProtocol.check_cmd(data):
        valid, command, params = check_client_request(data)
        if valid:
            if command == 'EXIT':
                is_exit = True

            else:
                msg = handle_client_request(command, params)
                length = myProtocol.get_len(msg)
                client_socket.send(length.encode())
                client_socket.send(msg.encode())

                if command == 'SEND_PHOTO':
                    with open(PHOTO_PATH, 'rb') as f:
                        client_socket.send(f.read())

        else:
            msg = 'params not ok, try again'
            client_socket.send(myProtocol.get_len(msg).encode())
            client_socket.send(msg.encode())

    client_socket.close()
    server_socket.close()


if __name__ == '__main__':
    main()
