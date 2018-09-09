#!coding=utf8
import hashlib
import itertools
import json
import mimetools
import mimetypes
import random
import time
import urllib2


class MultiPartForm(object):
    """Accumulate the data to be used when posting a form."""

    def __init__(self):
        self.form_fields = []
        self.files = []
        self.boundary = mimetools.choose_boundary()
        return

    def get_content_type(self):
        return 'multipart/form-data; boundary=%s' % self.boundary

    def add_field(self, name, value):
        """Add a simple field to the form data."""
        self.form_fields.append((name, value))
        return

    def add_file(self, fieldname, filename, body, mimetype=None):
        """Add a file to be uploaded."""
        #body = fileHandle.read()
        if mimetype is None:
            mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'

        self.files.append((fieldname, filename, mimetype, body))
        return

    def __str__(self):
        """Return a string representing the form data, including attached files."""
        # Build a list of lists, each containing "lines" of the
        # request.  Each part is separated by a boundary string.
        # Once the list is built, return a string where each
        # line is separated by '\r\n'.
        parts = []
        part_boundary = '--' + self.boundary

        # Add the form fields
        parts.extend(
            [part_boundary,
             'Content-Disposition: form-data; name="%s"' % name,
             '',
             value,
             ]
            for name, value in self.form_fields
        )

        # Add the files to upload
        parts.extend(
            [part_boundary,
             'Content-Disposition: file; name="%s"; filename="%s"' %\
             (field_name, filename),
             'Content-Type: %s' % content_type,
             '',
             body,
             ]
            for field_name, filename, content_type, body in self.files
        )



        # Flatten the list and add closing boundary marker,
        # then return CR+LF separated data

        flattened = list(itertools.chain(*parts))
        flattened.append('--' + self.boundary + '--')
        flattened.append('')

        body = [str(seg) for seg in flattened]

        return '\r\n'.join(body)

class CDNService(object):
    APP_KEY = 'wireless'
    APP_SECRET = "B9E24D792F448FAD901CBAB0C226928904FC5EFF30"
    SERVER = '10.103.20.192'

    ERROR_DICT = {
        -7:u"上传文件大小超出限制",
        -1008:u"上传相同文件太过频繁，请稍等再上传"
    }

    @classmethod
    def server_path(cls):
        return 'http://%s/res2/file/upload' % cls.SERVER

    @classmethod
    def get_error_desc(cls,code):
        return cls.ERROR_DICT.get(code,u"")


    @classmethod
    def get_upload_file(cls, files):
        incoming_file = files.file
        return incoming_file

    @classmethod
    def gen_sign(cls, timestamp):
        m = hashlib.md5()
        sign = "{0}&{1}&{2}".format(cls.APP_KEY, cls.APP_SECRET, timestamp)
        m.update(sign)
        return m.hexdigest()

    @classmethod
    def gen_filename(cls, name):
        return "%s%s " % (random.randint(0, 100000), name)


    @classmethod
    def send(cls, filename, body, uid="321",resize = False,size = ""):
        timestamp = int(time.time())
        sign = cls.gen_sign(timestamp)

        form = MultiPartForm()
        form.add_field('uid', uid)
        form.add_field("appkey", cls.APP_KEY)
        form.add_field("sign", sign)
        form.add_field("timestamp", timestamp)
        form.add_field("filter","mobile")
        form.add_field("maxsize", 100*1024*1024)
        #form.add_field("typelimit", "jpg,png,gif,mp3,amr")
        


        if resize:
            crpoptions = "act=resize&size=%s" % size
            form.add_field("crpoptions",crpoptions)

        form.add_file('file', cls.gen_filename(filename), body)


        request = urllib2.Request(cls.server_path())
        request.add_header('User-agent', 'Youku:Wireless')
        body = str(form)
        request.add_header('Content-type', form.get_content_type())
        request.add_header('Content-length', len(body))
        request.add_data(body)
        #print(form.get_content_type())

        #        print 'OUTGOING DATA:'
        #        print request.get_data()
        response = urllib2.urlopen(request).read()

        #print 'SERVER RESPONSE:'
        #print response
        return json.loads(response)