#coding:utf-8

import tornado.web

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get_one_poem(self, ids):
        return self.db.get("SELECT * FROM authors WHERE id = %s", int(ids))

    def get_all(self):
        return self.db.query("select * from authors")

class IndexHandler(BaseHandler):
    def get(self):
        greeting = self.get_argument('greeting', 'Hello')
        self.write(greeting + ' tornado!')

class LoginHandler(BaseHandler):
    def get(self):
        self.render('index.html')

class PoemPageHandler(BaseHandler):
    def post(self):
        name = self.get_argument('name')
        email = self.get_argument('email')
        verb = self.get_argument('verb')
        noun3 = self.get_argument('noun3')
        self.db.execute('INSERT INTO authors (name, email) VALUES(%s,%s)', name, email)
        ret = self.db.get('SELECT * from authors WHERE email = %s', email)
        self.render('poem.html', roads=name, wood=email, made=verb,
                difference=noun3, id=ret["id"])

class ShowHandler(BaseHandler):
    def get(self):
        ids = self.get_argument('id', 1)
        ret = self.get_one_poem(ids)
        if not ret:
            raise tornado.web.HTTPError(404)
        self.render('show.html', title = ret['email'], update = ret['name'])
