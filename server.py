#!/usr/bin/env python
import random
import socket
import time
import urlparse
import cgi
import jinja2
from StringIO import StringIO

# @CTB please be sure to spaces rather than tabs for indentation.
# what editor are you using? You can usually set it up to
# do the right thing.

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

def handle_connection(conn):
    loader = jinja2.FileSystemLoader('./templates')
    env = jinja2.Environment(loader=loader)

    request = conn.recv(1)

    # Getting all the headers
    while request[-4:] != '\r\n\r\n':
        request += conn.recv(1)

    first_line_of_request_split = request.split('\r\n')[0].split(' ')

    # Path is the second element in the first line of the request separated by whitespace.
    # GET/POST is first (Between GET and HTTP/1.1)
    http_method = first_line_of_request_split[0]

    try:
        parsed_url = urlparse.urlparse(first_line_of_request_split[1])
        path = parsed_url[2]
    except:
        not_found(conn, '', env)
        return

    if http_method == 'POST':
        headers_dict, content = parse_post_request(conn, request)
        environ = {}
        environ['REQUEST_METHOD'] = 'POST'

        # Printing the request
        print request + content
        form = cgi.FieldStorage(headers = headers_dict, fp = StringIO(content), environ = environ)

        if path == '/':
                handle_index(conn, '', env)
        elif path == '/submit':
                # POST has parameters at the end of content body
                handle_submit_post(conn, form, env)
        else:
                not_found(conn, '', env)
    else:
        print request
        if path == '/':
                handle_index(conn, '', env)
        elif path == '/content':
                handle_content(conn, '', env)
        elif path == '/file':
                handle_file(conn, '', env)
        elif path == '/image':
                handle_image(conn, '', env)
        elif path == '/submit':
                handle_submit_get(conn, parsed_url[4], env)
        else:
                not_found(conn, '', env)
    conn.close()

def handle_index(conn, params, env):
    toSend  = 'HTTP/1.0 200 OK\r\n' + \
	       'Content-type: text/html\r\n' + \
               '\r\n' + \
               env.get_template("index_result.html").render()
    
    conn.send(toSend)

def handle_content(conn, params, env):
    toSend = 'HTTP/1.0 200 OK\r\n' + \
	     'Content-type: text/html\r\n\r\n' + \
             env.get_template("content_result.html").render()

    conn.send(toSend)

def handle_file(conn, params, env):
    toSend = 'HTTP/1.0 200 OK\r\n' + \
	     'Content-type: text/html\r\n' + \
             '\r\n' + \
             env.get_template("file_result.html").render()

    conn.send(toSend)

def handle_image(conn, params, env):
    toSend = 'HTTP/1.0 200 OK\r\n' + \
	     'Content-type: text/html\r\n' + \
             '\r\n' + \
             env.get_template("image_result.html").render()
 
    conn.send(toSend)

def handle_submit_post(conn, form, env):
    try:
             firstname = form['firstname'].value
    except KeyError:
             firstname = ''
    try:
             lastname = form['firstname'].value
    except KeyError:
             lastname = ''

    vars = dict(firstname = firstname, lastname = lastname)
    template = env.get_template("submit_result.html")
 
    toSend = 'HTTP/1.0 200 OK\r\n' + \
             'Content-type: text/html\r\n' + \
             '\r\n' + \
             env.get_template("submit_result.html").render(vars)

    conn.send(toSend)

def handle_submit_get(conn, params, env):
    params = urlparse.parse_qs(params)

    try:
             firstname = params['firstname'][0]
    except KeyError:
             firstname = ''
    try:
             lastname = params['lastname'][0]
    except KeyError:
             lastname = ''

    vars = dict(firstname = firstname, lastname = lastname)
    template = env.get_template("submit_result.html")
 
    toSend = 'HTTP/1.0 200 OK\r\n' + \
             'Content-type: text/html\r\n' + \
             '\r\n' + \
             env.get_template("submit_result.html").render(vars)

    conn.send(toSend)

def not_found(conn, params, env):
    toSend = 'HTTP/1.0 404 Not Found \r\n' + \
	     'Content-type: text/html\r\n' + \
             '\r\n' + \
             env.get_template("not_found.html").render()

    conn.send(toSend)

def parse_post_request(conn, request):
    # Takes in a string request, parses it and returns a dictionary
    # of header name => header value
    # returns a string built from content of the request
    
    header_dict = dict()

    request_split = request.split('\r\n')
    
    # Headers are separated from the content by '\r\n' which, after the split is just ''.
    # First line isn't a header but everything else upto the empty line is. 
    # Names are separated by ':'
    
    for i in range(1, len(request_split) - 2):
             header = request_split[i].split(":", 1)
             header_dict[header[0].lower()] = header[1]

    content_length = int(header_dict['content-length'])

    content = ''
    for i in range(0, content_length):
             content += conn.recv(1)

    return header_dict, content

if __name__ == '__main__':
    main()
