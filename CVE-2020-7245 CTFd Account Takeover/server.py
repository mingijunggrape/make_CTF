from flask import Flask, flash, request, session, g, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://guest:1234@localhost/user'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(24)
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.CHAR(20), nullable=False)  
    password = db.Column(db.CHAR(120), nullable=False)  

    def __repr__(self):
        return f'<User {self.username}>'


def init_db():
    db.create_all()

@app.route('/')
def hello_world():
    if "userID" in session:
        return render_template('hi.html')
    return render_template('login.html')

@app.route('/login/', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        useid = request.form.get("username").strip()
        usepw = request.form.get("password").strip()
        
        user = User.query.filter_by(username=useid, password=usepw).first()
        
        if user:
            session["userID"] = useid
            return render_template('hi.html',username=user.username, password=user.password)
        else:
            flash("Invalid username or password", "error")
            return render_template('login.html')
    
    return render_template('login.html')
@app.route('/change/')
def Change():
    user = User.query.filter_by(username=session["userID"]).first()
    return render_template('change.html', password = user.password)

@app.route('/logout/')
def logout():
    session.pop("userID", None)
    return redirect(url_for("login"))

@app.route('/register/', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        useid = request.form.get("username").strip()
        usepw = request.form.get("password").strip()

        existing_user = User.query.filter_by(username=useid).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'error')
            return render_template('register.html')

        new_user = User(username=useid, password=usepw)
        db.session.add(new_user)
        db.session.commit()

        flash('Register successful! You can now log in.', 'success')
        return redirect(url_for('login'))  
    else:
        return render_template('register.html')

if __name__ == '__main__':
    with app.app_context():
        init_db() 
    app.run(host='0.0.0.0', port=5000, debug=True)
