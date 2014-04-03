import quixote
from quixote.directory import Directory, export, subdir

from . import html, image


#Username and Password Global Dictionary
accounts = {}
accounts["ari"] = "yolo"
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
        filetype = the_file.orig_filename.split('.')[1]
        if(filetype == 'tif' or filetype == 'tiff'):
            filetype = 'tiff'
        elif(filetype == 'jpeg' or filetype == 'jpg'):
            filetype == 'jpg'
        else:
            filetype == 'png'
        print 'received file of type: ' + filetype
        print dir(the_file)
        print 'received file with name:', the_file.base_filename
        data = the_file.read(int(1e9))

        image.add_image(data, filetype)

        return quixote.redirect('./')

    @export(name='image')
    def image(self):
        return html.render('image.html', globals())

    @export(name='image_raw')
    def image_raw(self):
        response = quixote.get_response()
        request = quixote.get_request()
        try:
            img = image.get_image(int(request.form['num']))
        except KeyError:
            img = image.get_latest_image()
        response.set_content_type('image/%s' % img[1])
        return img[0]

    @export(name = 'image_list')
    def image_list(self):
        return html.render('image_list.html')

    @export(name = 'image_count')
    def image_count(self):
        return len(image.images)
    
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


