import quixote
from quixote.directory import Directory, export, subdir
from quixote.util import StaticFile
import os.path

from . import html, image

class RootDirectory(Directory):
    _q_exports = []

    @export(name='')
    def index(self):
        return html.render('index.html')

    @export(name='jquery')
    def jquery(self):
        return open('jquery-1.11.0.min.js').read()

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

        return quixote.redirect('./')

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
        return html.render('image.html')

    @export(name='image_list')
    def image_list(self):
        return html.render('image_list.html')

    @export(name='image_count')
    def image_count(self):
        return len(image.images)

    @export(name='image_raw')
    def image_raw(self):
        response = quixote.get_response()
        request = quixote.get_request()
        try:
            img = image.get_image(int(request.form['num']))
        except KeyError:
            img = image.get_latest_image()
        if img[0].split('.')[-1].lower() in ('jpg', 'jpeg'):
            response.set_content_type('image/jpeg')
        elif img[0].split('.')[-1].lower() in ('tif', 'tiff'):
            response.set_content_type('image/tiff')
        else:
            response.set_content_type('image/png')
        return img[1]
