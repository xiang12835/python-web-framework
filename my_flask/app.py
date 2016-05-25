from flask import Flask,request,url_for,redirect,render_template,flash,abort
from models import *
from wtforms import Form,TextField,PasswordField,validators


class LoginForm(Form):
    username = TextField('username',[validators.Required()])
    password = PasswordField('password',[validators.Required()])


app = Flask(__name__)
app.secret_key = '123'


# 4 exception
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')

@app.route('/abort/<id>')
def abort(id):
    user = None
    if int(id) == 1:
        user = User(1,'yx')
        return render_template('if.html',usr=user)
    else:
        abort(404)


# 3 flash
@app.route('/')
def index():
    flash('Hello yx')
    return redirect(url_for('login'))


@app.route('/login',methods=['GET','POST'])
def login():
   # un = request.form.get('username')
   # pw = request.form.get('password')
    content = 'Hello Login'
    myForm = LoginForm(request.form)
    
    # if request.method=='POST':
    #     un = myForm.username.data
    #     pw = myForm.password.data
    #     if not un:
    #         flash('please input your username!')
    #     if not pw:
    #         flash('please input your password!')
    #     if un == 'yx' and pw == '35' and myForm.validate():
    #         flash('login success')
    #     else:
    #         flash('username or password is wrong!')
    
    if request.method=='POST':
        u = UserDB(myForm.username.data,myForm.password.data)
        if u.isExisted():
            flash('login success')
        else:
            flash('username or password is wrong!')

    return render_template('index.html',cnt=content,fm=myForm)

@app.route("/register",methods=['GET','POST'])
def register():
    content = 'Hello register'
    myForm = LoginForm(request.form)
    if request.method == 'POST':
        u = UserDB(myForm.username.data,myForm.password.data)
        u.add()
        return "Register Successfully"
    return render_template("index.html",cnt=content,fm=myForm)


# 2 template
@app.route('/template_if/<id>')
def template_if(id):
    user = None
    if int(id) == 1:
        user = User(1,'yx')
    return render_template('if.html',usr=user)

@app.route('/template_for')
def template_for():
    users = []
    for i in range(1,11):
        user = User(i,'yx'+str(i))
        users.append(user)
    return render_template('for.html',usrs=users)

@app.route('/one')
def one():
    return render_template('one.html')

@app.route('/two')
def two():
    return render_template('two.html')


# 1 route
@app.route('/hello')
def hello():
    return 'hello flask'

@app.route('/users/<id>')
def users(id):
    return 'hello user:' + id

@app.route('/query_user')
def query_user():
    id = request.args.get('id')
    return 'query user: ' + id

@app.route('/query_url')
def query_url():
    return 'query url: ' + url_for('query_user')


if __name__=='__main__':
    app.run(host='0.0.0.0',port=5050,debug=True)
