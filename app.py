from flask import Flask, render_template, request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160))
    content = db.Column(db.Text)
    complete = db.Column(db.Boolean)

@app.route('/index')
@app.route('/')
def index():
    todo = ToDo.query.all()
    return render_template('index.html',todos=todo)

@app.route('/add',methods=["POST"])
def addToDo():
    title = request.form.get('title')
    content = request.form.get('content')
    newTodo = ToDo(title=title,content=content,complete=False)
    db.session.add(newTodo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/complete/<string:id>')
def completeToDo(id):
    veri = ToDo.query.filter_by(id=id).first()
    if veri==None: redirect(url_for('index'))
    if veri.complete==False:
        veri.complete = True
    else:
        veri.complete = False
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<string:id>')
def deleteToDo(id):
    veri = ToDo.query.filter_by(id=id).first()
    db.session.delete(veri)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/detail/<string:id>')
def detailToDo(id):
    todo = ToDo.query.filter_by(id=id).first()
    print(todo)
    if todo == None : return redirect(url_for('index'))
    return render_template('detail.html',todo=todo)

if __name__ == '__main__':
    app.run()