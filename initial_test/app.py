from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, LoginManager, login_user, current_user, logout_user, login_required
from datetime import datetime
import os, json
import random
app = Flask(__name__)
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user="rasp",pw="postgresFun12",url="127.0.0.1:5432",db="test")
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SECRET_KEY'] = 'you-will-never-guess'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
# login_manager.login_message_category = 'info'

class Users(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(200), nullable=False)
	email = db.Column(db.String(200), nullable=False)
	password = db.Column(db.String(200), nullable=False)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)

	def set_password(self, password):
		self.password = bcrypt.generate_password_hash(password).decode('UTF-8')

	def check_password(self, password):
		return bcrypt.check_password_hash(self.password, password)
	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.id}')"

@login_manager.user_loader
def load_user(id):
	return Users.query.get(int(id))

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		if current_user.is_authenticated:
			return redirect(url_for('/'))
		else:
			email = request.form['email']
			passw = request.form['pass']
			user = Users.query.filter_by(email=email).first()
			print(user)
			if user is not None and user.check_password(passw):
				login_user(user, remember=True)
				next_page = request.args.get('next')
				if not next_page:
					next_page = url_for('/')
				return redirect(next_page)
			else:
				return 'Error'
	else:
		if current_user.is_authenticated:
			return redirect(url_for('/'))
		else:
			return render_template('login.html')

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		if current_user.is_authenticated:
			return redirect(url_for('index'))
		username = request.form['username']
		email = request.form['email']
		passw = request.form['pass']

		user = Users(username=username, email=email)
		user.set_password(passw)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('login'))
	else:
		if current_user.is_authenticated:
			return redirect(url_for('index'))
		else:
			return render_template('register.html')

@app.route('/', methods=['POST', 'GET'])
@login_required
def index():
	if current_user.is_authenticated:
		return render_template('loggedin.html', user=current_user.username)
	else:
		return redirect('/login')

@app.route('/summary')
def summary():
	f= open("./static/files/vars.txt","r")
        lines = f.readlines()
        light = lines[0]
        f.close()
        print(light)
        data = {"ON":bool(light[6:10])}
	response = app.response_class(
		response = json.dumps(data),
		status=200,
		mimetype='application/json'
	)
	return response
#
# @app.route('/', methods=['POST', 'GET'])
# def index():
#     return render_template('login.html')


# @app.route('/delete/<int:id>')
# def delete(id):
#     task_to_delete = Todo.query.get_or_404(id)
#
#     try:
#         db.session.delete(task_to_delete)
#         db.session.commit()
#         return redirect('/')
#     except:
#         return 'There was a problem deleting that task'
#
# @app.route('/update/<int:id>', methods=['GET', 'POST'])
# def update(id):
#     task = Todo.query.get_or_404(id)
#
#     if request.method == 'POST':
#         task.content = request.form['content']
#
#         try:
#             db.session.commit()
#             return redirect('/')
#         except:
#             return 'There was an issue updating your task'
#
#     else:
#         return render_template('update.html', task=task)
#
# @app.route("/logout")
# def logout():
#     logout_user()
#     return redirect(url_for('home'))

if __name__ == "__main__":
	app.run(debug=True)
