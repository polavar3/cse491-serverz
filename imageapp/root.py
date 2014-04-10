import quixote
from quixote.directory import Directory, export, subdir

from . import html, image


#Username and Password Global Dictionary
accounts = {}
accounts["justin"] = "yolo"
current_user = '' 
welcome_message = "No User Currently Logged In"
comment_block = ''

class RootDirectory(Directory):
    _q_exports = []

    @export(name='')                    # this makes it public.
    def index(self):
        global welcome_message
        if current_user == '':
            welcome_message = "No User Currently Logged In"
        else:
            welcome_message = "Welcome, " + current_user
        return html.render('index.html', globals())

    @export(name='upload')
    def upload(self):
        return html.render('upload.html')

    @export(name='upload_receive')
    def upload_receive(self):
        request = quixote.get_request()
        print request.form.keys()

        the_file = request.form['file']
        print dir(the_file)
        print 'received file with name:', the_file.base_filename
        data = the_file.read(the_file.get_size())

        image.add_image(the_file.base_filename, data)

        return html.render('index.html',globals())

    @export(name='upload2')
    def upload2(self):
        return html.render('upload2.html')

    @export(name='upload2_receive')
    def upload2_receive(self):
        request = quixote.get_request()
        print request.form.keys()

        the_file = request.form['file']
        print dir(the_file)
        print 'received file with name:', the_file.base_filename
        data = the_file.read(the_file.get_size())

        image.add_image(the_file.base_filename, data)

        return html.render('upload2_received.html')

    @export(name='image')
    def image(self):
        return html.render('image.html', globals())

    @export(name='image_raw')
    def image_raw(self):
        response = quixote.get_response()
        request = quixote.get_request()

        try:
            i = int(request.form['num'])
        except:
            i = -1

        img = image.retrieve_image(i)

        filename = img.filename
        if filename.lower() in ('jpg', 'jpeg'):
            response.set_content_type('image/jpeg')
        elif filename.lower() in ('tif',' tiff'):
            response.set_content_type('image/tiff')
        else: # Default to .png for reasons
            response.set_content_type('image/png')
        return img.data  
 
    @export(name = 'image_list')
    def image_list(self):
        return html.render('image_list.html')

    @export(name = 'image_count')
    def image_count(self):
        return image.get_num_images()
 
    @export(name='jquery')
    def jquery(self):
        return open('jquery-1.11.0.min.js').read()

    @export(name='login')
    def login(self):
        login_message = "Enter username and password: "
        return html.render('login.html', locals())

    @export(name='submit_login')
    def submit_login(self):
        global current_user
        request = quixote.get_request()
        print request.form.keys()
        user = request.form['username']
        pass_word = request.form['password']
        if current_user != '':
            login_message = "An account is already currently logged in"
            return html.render("login.html", locals())
        if user == '' or pass_word == '':
            login_message = "Required Field is Blank"
            return html.render("login.html", locals())
        if user in accounts and accounts[user] == pass_word:
            current_user = user
            return html.render("success_login.html", request.form)
        else:
            login_message = "Invalid Username or Password"
            return html.render("login.html", locals())
        print accounts
    
    @export(name='create_login')
    def create_login(self):
        global current_user, accounts
        request = quixote.get_request()
        print request.form.keys()
        user = request.form['username']
        pass_word = request.form['password']
        if current_user != '':
            message = "An account is already logged in"
            return html.render("create_account.html", locals())

        if user == '' or pass_word == '':
            message = "Required Field is Blank"
            return html.render("create_account.html", locals())

        if user in accounts:
            message = "account already exists"
            return html.render("create_account.html", locals())
        else:
            accounts[user] = pass_word
            current_user = user
            return html.render("success_login.html", request.form)
        print accounts

    @export(name='create_account')
    def create_account(self):
        request = quixote.get_request()
        message = "It appears you don't have an account with us yet, try making one below"
        if "result" in request.form and request.form["result"] == "failure":
            message = "acount already exists"
        return html.render("create_account.html", locals())

    @export(name = 'success_login')
    def success_login(self):
        return html.render("success_login.html")

    @export(name = 'submit_logout')
    def submit_logout(self):
        global current_user
        if current_user != '':
            current_user = ''
            login_message = "Successfully logged out"
            return html.render("login.html", locals())
        else:
            login_message = "No user currently logged in"
            return html.render("login.html", locals())
            
    @export(name = 'submit_comment')
    def submit_comment(self):
        global current_user, comment_block
        request = quixote.get_request()
        yolo_comment = request.form['comment']
        if current_user != '':
            yolo_comment = current_user + ': ' +yolo_comment+"<br>"
        else :
            yolo_comment = "Anonymous: " +yolo_comment+"<br>"
            
        comment_block += yolo_comment
        return html.render("image.html", globals())

    @export(name='get_comments')
    def get_comments(self):
        response = quixote.get_response()
        request = quixote.get_request()

        try:
            i = int(request.form['num'])
        except:
            i = -1

        all_comments = []
        for comment in image.get_comments(i):
            all_comments.append("""\
    <comment>
     <text>%s</text>
    </comment>
    """ % (comment))

        xml = """
    <?xml version="1.0"?>
    <comments>
    %s
    </comments>
    """ % ("".join(all_comments))

        return xml

    @export(name='add_comment')
    def add_comment(self):
        response = quixote.get_response()
        request = quixote.get_request()

        try:
            i = int(request.form['num'])
        except:
            i = -1

        try:
            comment = request.form['comment']
        except:
            return

        image.add_comment(i, comment)

    @export(name='get_score')
    def get_score(self):
        response = quixote.get_response()
        request = quixote.get_request()

        try:
            i = int(request.form['num'])
        except:
            i = -1

        return image.get_image_score(i)

    @export(name='increment_score')
    def increment_score(self):
        response = quixote.get_response()
        request = quixote.get_request()

        try:
            i = int(request.form['num'])
        except:
            i = -1

        image.increment_image_score(i)

    @export(name='decrement_score')
    def decrement_score(self):
        response = quixote.get_response()
        request = quixote.get_request()

        try:
            i = int(request.form['num'])
        except:
            i = -1

        image.decrement_image_score(i)
