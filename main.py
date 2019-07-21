from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    date = db.Column(db.String(10))
    content = db.Column(db.String(50000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, date, content, owner):
        self.title = title
        self.date = date
        self.content = content
        self.owner = owner

    def __repr__(self):
        return '<Blog %r>' % self.title, self.date, self.content

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = sb.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.before_request
def require_login():
    allowed_routes = ['login', 'index', 'blog', 'signup', 'static']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/', methods=['POST', 'GET'])
def index():
    user = User.query.all()
    return render_template('index.html', user=users)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'username' in session:
        flash('You are currently logged in')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.passwsord == password:
            session['username'] = username
            flash('You are now logged in')
            return redirect('/addnew')
        else:
            flash('Password is incorrect, or user does not exist', 'error')
    return render_template('login.html', title="Login Page")

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if 'username' in session:
        flash("You are currently logged in")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        if not username or not password:
            flash('Username and Password are required')
            return redirect('signup')
        if len(username) < 3 or len(password < 3):
            flash('Username and password must contain 3 or more characters', 'error')
            return redirect('signup')
        if password != verify:
            flash('Passwords do not match', 'error')
            return redirect('signup')
        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/addnew')
        else:
            flash('User already exists', 'error')
            return redirect('/signup')
    return render_template('signup.html', title="User signup")

@app.route('/blog', methods=['GET', 'POST'])
def blog():
    blog_post = Blog.query.all()
    users = User.query.all()
    entry_id = request.args.get('id')
    user_id = request.args.get('user_id')

    if entry_id:
        blog_post = Blog.query.filter_by(id=blog_id).all()
        for blog in blog_post:
            user_id = blog.owner_id
            user = User.query.filter_by(id=user_id).first()

        return render_template('blog_entry.html', blog_post=blog_post, user=user)
    if user_id:
        user = User.query.filter_by(id=user_id).first()
        blog_post = Blog.query.filter_by(owner_id=user_id).all()
        return render_template('placeholder.html', blog_post=blog_post, users=users)

    else:
        return render_template('blog.html', blog_post=blog_post, user=user)



@app.route('/addnew', methods=['POST', 'GET'])
def addnew():
    owner = User.query.filter_by(username=session['username']).first()
    if request.method == 'GET':
        return render_template('addnew.html', title= "New Entry")

    else:
        entry_title = request.form['title']
        entry_date = request.form['date']
        entry_content = request.form['content']
        if (not entry_title) or (not entry_content):
            flash("Title and Content are required", 'error')
            return redirect('/addnew')
        else:
            blog = Blog(entry_title, entry_date, entry_content, owner)
            db.session.add(blog)
            db.session.commit()
            username = User.query.filter_by(id=blog.owner.id).first()
            return render_template('blog.entry.html', blog=blog)


@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')




if __name__ == '__main__':
    app.run()