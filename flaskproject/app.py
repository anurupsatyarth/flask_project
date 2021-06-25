from flask import Flask, render_template,url_for, request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app= Flask(__name__)   
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///test.db'
db=SQLAlchemy(app)

class todo(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(200),nullable= False)
    completed = db.Column(db.Integer,default=0)
    date_created= db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id




@app.route('/',methods=['POST','GET'])

def index():
    if request.method == 'POST':
        task_content= request.form['content']
        new_task = todo(content=task_content)

        try: 
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your task"
    else:
        tasks= todo.query.order_by(todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete =todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'there is a problem in deleteing the task'


@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    task_to_update = todo.query.get_or_404(id)
    if request.method == "POST":
        task_to_update.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'there is a problem in updating the task'
    else:
        return render_template('update.html',task=task_to_update)

    

           

if __name__ == "__main__":
    app.run(debug=True)


