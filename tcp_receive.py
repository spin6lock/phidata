# encoding: utf-8
import errno
import select
import socket
import time

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listener.bind(('0.0.0.0', 9000))
listener.listen(128)
listener.setblocking(False)

poller = select.poll()
poller.register(listener, select.POLLIN)
connections = {}
print('Waiting for connection...')

while True:
    for fd, events in poller.poll():
        if fd == listener.fileno():
            if events & (select.POLLERR | select.POLLHUP | select.POLLNVAL):
                raise RuntimeError('Listener failed')
            try:
                sock, addr = listener.accept()
            except socket.error as exc:
                if exc.errno in (errno.EAGAIN, errno.EWOULDBLOCK, errno.EINTR):
                    continue
                raise
            sock.setblocking(False)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            connections[sock.fileno()] = sock
            poller.register(sock, select.POLLIN)
            continue

        sock = connections[fd]
        try:
            data = sock.recv(1024)
        except socket.error as exc:
            if exc.errno in (errno.EAGAIN, errno.EWOULDBLOCK, errno.EINTR):
                if not events & (select.POLLERR | select.POLLHUP | select.POLLNVAL):
                    continue
            data = b''
        if not data:
            poller.unregister(fd)
            del connections[fd]
            sock.close()
            continue

        data = data.decode('utf-8', 'ignore').replace('#END#', '').strip()
        if data:
            now = time.localtime()
            timestamp = time.strftime('%Y-%m-%d %X', now)
            date = time.strftime('%Y-%m-%d', now)
            with open(date + '.txt', 'ab') as output:
                output.write((timestamp + data + '\n').encode('utf-8'))
