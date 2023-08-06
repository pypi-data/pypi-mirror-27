import socket

def get():

    sock = socket.socket()
    sock.bind(('', 0))
    _, port = sock.getsockname()
    sock.close()
    return port


if __name__ == "__main__":
    print(get())