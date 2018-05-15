import socket
import threading
import time

Me = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Me.bind(('0.0.0.0', 9999))
Me.listen(5)
print('Waiting for connection..')


def tcplink(sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    # print(addr)
    buffer = []
    sock.send(b'Welcome')
    while True:
        buffer = sock.recv(1024)
        time.sleep(2)
        print(len(buffer))
        print()
        print(buffer)
        # buffer.append(data)
        # print(data)
        if not buffer or buffer.decode('utf-8') == 'exit':
            break
        # sock.send(('hello,%s!'%data.decode('utf-8')).encode('utf-8'))
    sock.close()
    print('Connect %s:%s closed.' % addr)


while True:
    Sock_Him, Addr_Him = Me.accept()

    t = threading.Thread(target=tcplink, args=(Sock_Him, Addr_Him))
    t.start()
