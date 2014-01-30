import server

class FakeConnection(object):
    """
    A fake connection class that mimics a real TCP socket for the purpose
    of testing socket I/O.
    """
    def __init__(self, to_recv):
        self.to_recv = to_recv
        self.sent = ""
        self.is_closed = False

    def recv(self, n):
        if n > len(self.to_recv):
            r = self.to_recv
            self.to_recv = ""
            return r
            
        r, self.to_recv = self.to_recv[:n], self.to_recv[n:]
        return r

    def send(self, s):
        self.sent += s

    def close(self):
        self.is_closed = True

# Test a basic GET call.

def test_handle_index():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n\r\n' + \
                      '<body bgcolor = "green">' + \
                      '<h1>Hello, world.</h1>' + \
                      'This is polavar3\'s Web server.' + \
                      '<br>' + \
                      '<a href="/content">Content</a><br>' + \
                      '<a href="/file">File</a><br>' + \
                      '<a href="/image">Image</a><br>' + \
		      '<a href="/form">Form</a><br>' + \
                      '</body>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_content():
    content_conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n\r\n' + \
                      '<h1><marquee>Look at all this content!</marquee></h1>'

    server.handle_connection(content_conn)

    assert content_conn.sent == expected_return, 'Got: %s' % (repr(content_conn.sent),)

def test_handle_file():
    file_conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n\r\n' + \
                      '<h1>This is polavar3\'s file page.</h1>'
    server.handle_connection(file_conn)

    assert file_conn.sent == expected_return, 'Got: %s' % (repr(file_conn.sent),)

def test_handle_image():
    image_conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n\r\n' + \
                      '<h1>This is polavar3\'s image page.</h1>'
    server.handle_connection(image_conn)

    assert image_conn.sent == expected_return, 'Got: %s' % (repr(image_conn.sent),)

def test_handle_form():
    form_conn = FakeConnection("GET /form HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
		      'Content-type: text/html\r\n' + \
		      '\r\n' + \
		      '<form action="/submit" method="GET">' + \
		      'First Name:<input type="text" name="firstName">' + \
		      'Last Name:<input type="text" name="lastName">' + \
		      '<input type="submit" value="Submit Get">' + \
		      '</form>\r\n\>' + \
		      '<form action="/submit" method="POST">' + \
		      'First Name:<input type="text" name="firstName">' + \
		      'Last Name:<input type="text" name="lastName">' + \
		      '<input type="submit" value="Submit Post">' + \
		      '</form>\r\n\>'

    server.handle_connection(form_conn)

    assert form_conn.send == expected_return, 'Got: %s' % (repr(form_conn.sent),)

def test_post_request():
    post_conn = FakeConnection("POST /image HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
		      'Content-type: text/html\r\n\r\n' + \
		      '<h1>Hello, world.</h1>'

    server.handle_connection(post_conn)

    assert post_conn.send == expected_return, 'Got: %s' % (repr(post_conn.sent),)

def test_handle_get_submit():
    submit_conn = FakeConnection("GET /submit?firstName=Ari&lastName=Polavarapu HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
		      'Content-type: text/html\r\n\r\n' + \
		      '<p>' + \
		      'Hello Mr. Ari Polavarapu.' + \
		      '</p>'

    server.handle_connection(submit_conn)

    assert submit_conn.send == expected_return, 'Got: %s' % (repr(submit_conn.sent),)

def test_handle_post_submit():
    submit_conn = FakeConnection("POST /submit HTTP/1.0\r\n\r\nfirstName=Ari&lastName=Polavarapu")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
		      'Content-type: text/html\r\n\r\n' + \
		      '<p>' + \
		      'Hello Mr. Ari Polavarapu.' + \
		      '</p>'

    server.handle_connection(submit_conn)

    assert submit_conn.send == expected_return, 'Got: %s' % (repr(submit_conn.sent),)



	
