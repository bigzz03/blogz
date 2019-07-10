from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    body = db.Column(db.Text)

    def __init__(self, title, body):
        self.title = title
        self.body = body


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
    if request.method == 'POST':
        entry_title = request.form['title']
        entry_date = request.form['date']
        entry_content = request.form['content']
        
        title_error = ''
        body_error = ''

        if len(entry_title) < 1:
            title_error = 'You must enter a title.'
            #return redirect('/addnew')
        if len(entry_content) < 1:
            body_error = 'You must enter a body'
            #return redirect('/addnew')

        entry = Blog(entry_title, entry_date, entry_content)
        db.session.add(entry)
        db.session.commit()

        return render_template('blog_entry.html', title= 'Blog Entry', entry= entry)

    else:
        return render_template('addnew.html')



if __name__ == '__main__':
    app.run()