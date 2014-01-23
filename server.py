#!/usr/bin/env python
import random
import socket
import time

def main():
     s = socket.socket()         # Create a socket object
     host = socket.getfqdn() # Get local machine name
     port = random.randint(8000, 9999)
     s.bind((host, port))        # Bind to the port

     print 'Starting server on', host, port
     print 'The Web server URL for this would be http://%s:%d/' % (host, port)

     s.listen(5)                 # Now wait for client connection.

     print 'Entering infinite loop; hit CTRL-C to exit'

     while True:
        # Establish connection with client.    
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port
        handle_connection(c)
     return

def handle_connection(conn):
    request = conn.recv(1000)
    method = request.split('\n')[0].split(' ')[0]
    path = request.split('\n')[0].split(' ')[1]
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n')
    conn.send('\r\n')
    # Sending a response
    if method == 'POST':
            conn.send('hello world')
            return
    elif path == '/':
            conn.send('<body bgcolor = "green">')
            conn.send('<h1>Hello, world.</h1>')
            conn.send('This is polavar3\'s Web server.')
            conn.send('<br>')
            conn.send('<a href="/content">Content</a><br>')
            conn.send('<a href="/file">File</a><br>')
            conn.send('<a href="/image">Image</a><br>')
            conn.send('</body>')
    elif path == '/content':
            conn.send('<h1><marquee>Look at all this content!</marquee></h1>')
    elif path == '/file':
            conn.send('<h1>This is polavar3\'s file page.</h1>')
    elif path == '/image':
            conn.send('<h1>This is polavar3\'s image page.</h1>')
    conn.close()
    return

if __name__ == '__main__':
    main()
