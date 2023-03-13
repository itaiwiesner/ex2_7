

def check_cmd(data):
    """
    Check if the command is defined in the protocol, including all parameters
    For example, DELETE c:\work\file.txt is good, but DELETE alone is not
    """
    # (3)

    command = data.split(' ')
    if len(command) == 1 and (command[0] == 'EXIT' or command[0] == 'SEND_PHOTO' or 'TAKE_SCREENSHOT'):
        return True

    if len(command) == 2 and (command[0] == 'DIR' or command[0] == 'DELETE' or command[0] == 'EXECUTE'):
        return True

    if len(command) == 3 and command[0] == 'COPY':
        return True

    return False


def get_len(data):
    """
    return the length field of the cmd
    """
    return str(len(data)).zfill(4)


def check_length_field(length):
    """
    check if length field is valid
    """
    try:
        int(length)

    except ValueError:
        return False

    else:
        return True
