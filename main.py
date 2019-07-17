from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    date = db.Column(db.String(10))
    content = db.Column(db.String(50000))

    def __init__(self, title, date, content):
        self.title = title
        self.date = date
        self.content = content

    def __repr__(self):
        return '<Blog %r>' % self.title, self.date, self.content


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html',title="Build-a-blog")



@app.route('/blog', methods=['GET', 'POST'])
def blog():
    entry_id = request.args.get('id')

    if (entry_id):
        entry = Blog.query.get(entry_id)
        return render_template('blog_entry.html', title= 'Blog Entry', entry= entry)
    else:
        blogs= Blog.query.all()
    return render_template('blog.html', title= 'Blog Posts', blogs= blogs)



@app.route('/addnew', methods=['POST', 'GET'])
def addnew():
    if request.method == 'GET':
        return render_template('addnew.html', title= "New Entry")

    if request.method == 'POST':
        entry_title = request.form['title']
        entry_date = request.form['date']
        entry_content = request.form['content']
        entry = Blog(entry_title, entry_date, entry_content)

        title_error = ''
        body_error = ''

        if len(entry_title) == 0:
            title_error = "You must enter a title for your post."
        if len(entry_content) == 0:
            body_error = "You must enter some text for the body."

        if not title_error and not body_error:    
            db.session.add(entry)
            db.session.commit()
            return redirect('/blog?id={}'.format(entry.id))

        else:
            blogs= Blog.query.all()
            return render_template('addnew.html', title= 'Add new post...', blogs= blogs,
                entry_title= entry_title, title_error= title_error,
                entry_content= entry_content, body_error= body_error)



if __name__ == '__main__':
    app.run()