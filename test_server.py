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

def test_handle_connection():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")

    server.handle_connection(conn)

    assert 'HTTP/1.0 200' in conn.sent and 'form' in conn.sent, \
    'Got: %s' % (repr(conn.sent),)

def test_handle_connection_content():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")

    server.handle_connection(conn)

    assert 'HTTP/1.0 200' in conn.sent and 'content' in conn.sent, \
    'Got: %s' % (repr(conn.sent),)

def test_handle_connection_file():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")

    server.handle_connection(conn)

    assert 'HTTP/1.0 200' in conn.sent and 'file' in conn.sent, \
    'Got: %s' % (repr(conn.sent),)

def test_handle_connection_image():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>So many images!</h1>'

    server.handle_connection(conn)
    print conn.sent

    assert 'HTTP/1.0 200' in conn.sent and 'image' in conn.sent, \
    'Got: %s' % (repr(conn.sent),)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_submit():
    conn = FakeConnection("GET /submit?firstname=Bill&lastname=Nye" + \
            "HTTP/1.1\r\n\r\n")

    server.handle_connection(conn)

    assert 'html' in conn.sent and 'Bill' in conn.sent \
      and 'Nye' in conn.sent, 'Got: %s' % (repr(conn.sent),)

def test_handle_submit_no_first_name():
    conn = FakeConnection("GET /submit?firstname=%lastname=Nye" + \
            "HTTP/1.1\r\n\r\n")

    server.handle_connection(conn)

    assert 'html' in conn.sent and 'Nye' in conn.sent, \
            'Got: %s' % (repr(conn.sent),)

def test_handle_submit_no_last_name():
    conn = FakeConnection("GET /submit?firstname=Bill&lastname=" + \
            "HTTP/1.1\r\n\r\n")

    server.handle_connection(conn)

    assert 'html' in conn.sent and 'Bill' in conn.sent, \
            'Got: %s' % (repr(conn.sent),)

def test_handle_not_found():
    conn = FakeConnection("GET /fake HTTP/1.0\r\n\r\n")

    server.handle_connection(conn)

    assert 'HTTP/1.0 404' in conn.sent, \
            'Got: %s' % (repr(conn.sent),)



# Testing POST connections

def test_handle_connection_post():
    conn = FakeConnection("POST / HTTP/1.0\r\n" + \
            "Content-length: 0\r\n\r\n")

    server.handle_connection(conn)

    assert 'HTTP/1.0 200' in conn.sent and 'form' in conn.sent, \
            'Got: %s' % (repr(conn.sent),)

def test_handle_submit_post():
    conn = FakeConnection("POST /submit HTTP/1.1\r\n" + \
            "Content-Length: 31\r\n\r\n" + \
            "firstname=Bill&lastname=Nye")

    server.handle_connection(conn)

    assert 'HTTP/1.0 200' in conn.sent and 'Hello' in conn.sent, \
            'Got: %s' % (repr(conn.sent),)

def test_handle_submit_post_multipart_and_form_data():
    conn = FakeConnection("POST /submit " + \
            "HTTP/1.1\r\nContent-Length: 246\r\n\r\n------" + \
            "WebKitFormBoundaryAaa127xQakMcNYm\r\n" + \
            "Content-Disposition: form-data; name='firstname'\r\n\r\nBill" + \
            "\r\n------WebKitFormBoundaryAaa127xQakxMcNYm\r\n" + \
            "Content-Disposition: form-data; name='lastname'\r\n\r\nNye" + \
            "\r\n------WebKitFormBoundaryAaa127xWakxMcNYm--')")

    server.handle_connection(conn)

    assert 'HTTP/1.0 200' in conn.sent and 'Hello' in conn.sent, \
            'Got: %s' % (repr(conn.sent),)

def test_handle_not_found_post():
    conn = FakeConnection("POST /nada HTTP/1.1\r\n" + \
            "Content-Length: 32\r\n\r\n" + \
            "firstname=Bill&lastname=Nye")

    server.handle_connection(conn)

    assert 'HTTP/1.0 404' in conn.sent, \
            'Got: %s' % (repr(conn.sent),)

def test_handle_long_request():
    firstname = lastname = "asdfasdfasdfasdfasdf" * 100
    conn = FakeConnection("POST /submit HTTP/1.1\r\n" + \
            "Content-Length: 4020\r\n\r\n" + \
            "firstname=%s&lastname=%s" % (firstname, lastname))

    server.handle_connection(conn)

    assert 'HTTP/1.0 200' in conn.sent and 'Hello' in conn.sent, \
            'Got: %s' % (repr(conn.sent),)

def test_handle_empty_request():
    conn = FakeConnection("\r\n\r\n")

    server.handle_connection(conn)

    assert 'HTTP/1.0 404' in conn.sent, \
            'Got: %s' % (repr(conn.sent),)

