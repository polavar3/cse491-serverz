import random
import socket
import time
import urlparse
import cgi
from StringIO import StringIO
from app import make_app

def main():
    s = socket.socket()    # Creating a socket object
    host = socket.getfqdn() # Get local machine name
    port = random.randint(8000, 9999)
    s.bind((host, port)) # Bind to the port

    print "Starting server on", host, port
    print "The Web server URL for this would be http://%s:%d/" % (host, port)

    s.listen(5)    # Now wait for client connection

    print "Entering infinite loop; hit CTRL-C to exit"

    while True:
        # Establish connection with client
        c, (client_host, client_port) = s.accept()
        handle_connection(c)

# Handles the connection
def handle_connection(conn):
    environ = {}
    request = conn.recv(1)

    while request[-4:] != '\r\n\r\n':
        request += conn.recv(1)

    request_info = request.split('\r\n')[0].split(' ')

    environ['REQUEST_METHOD'] = request_info[0]

    try:
        url_parsed = urlparse.urlparse(request_info[1])
        environ['PATH_INFO'] = url_parsed[2]
    except:
        pass

    def start_response(status, response_headers):
        conn.send('HTTP/1.0 ')
        conn.send(status)
        conn.send('\r\n')
        for pair in response_headers:
            key, header = pair
            conn.send(key + ':' + header + '\r\n')
        conn.send('\r\n')

    if environ['REQUEST_METHOD'] == 'POST':
        environ = parse_post_request(conn, request, environ)
    elif environ['REQUEST_METHOD'] == 'GET':
        environ['QUERY_STRING'] = url_parsed.query
    wsgi_app = make_app()
    conn.send(wsgi_app(environ, start_response))
    conn.close()

def parse_post_request(conn, request, environ):
    request_split = request.split("\r\n")

    for i in range(1, len(request_split) - 2):
        header = request_split[i].split(": ", 1)
        environ[header[0].lower()] = header[1]

    content_length = int(environ["content-length"])

    content = ''
    for i in range(0, content_length):
        content += conn.recv(1)

    environ["wsgi.input"] = StringIO(content)
    return environ

if __name__ == '__main__':
    main()












































