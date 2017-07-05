from flask import Flask
import mysql.connector
from flask import render_template
from flask import request, redirect, url_for, session, flash
from functools import wraps


app = Flask(__name__)

app.secret_key = "my precious"



def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args,**kwargs)
		else:
			flash('you need to login first')
			return redirect(url_for('login'))
	return wrap

@app.route('/')
@login_required
def index():
	return render_template('index.html')

@app.route("/post_college", methods = ['POST', 'GET'])
@login_required
def post_college():

	cnx = mysql.connector.connect(user='root', password='gomya', database ='Petrol')
	cursor = cnx.cursor(buffered = True)

	college_name = request.form['college_name']
	
	add_college = ("INSERT INTO Colleges (Name)"
	" VALUES( %(col_name)s)")
	data_college = {
	'col_name' : college_name}
	
	cursor.execute(add_college, data_college)
	cnx.commit()
	
	cursor.close()
	cnx.close()
	return redirect(url_for('index'))





@app.route("/select", methods = ['POST', 'GET'])
@login_required
def select():
	cnx = mysql.connector.connect(user='root', password='gomya', database ='Petrol')
	cursor = cnx.cursor(buffered = True)

	query = ("""SELECT Name FROM Colleges""")
	cursor.execute(query)
	data = cursor.fetchall()

	mylist = []
	for row in data:
		mylist.append(' '.join(str(x) for x in row))

	cursor.close()
	cnx.close()

	return render_template('add_num.html', mylist = mylist)

@app.route("/submit", methods = ['POST', 'GET'])
def submit():
	cnx = mysql.connector.connect(user='root', password='gomya', database ='Petrol')
	cursor = cnx.cursor(buffered = True)

	if request.method == 'POST':
	
		col_name = request.form.get('Colleges')
			
		query_coll = (" SELECT CollegeID FROM Colleges WHERE Name = '%s'" %(col_name)) 
		cursor.execute(query_coll)
			
		coll = cursor.fetchall()
		col_id_list = [] 

		for row in coll:
			col_id_list.append(' '.join(str(x) for x in row))

		print col_id_list[0]
		

		stud1 = request.form.get('student1')
		stud2 = request.form.get('student2')
		stud3 = request.form.get('student3')
		stud4 = request.form.get('student4')

		query_stud = (" SELECT StudentID FROM Students "
			" WHERE Name = '%s' OR Name = '%s' OR Name = '%s' OR Name = '%s'" %(stud1,stud2,stud3,stud4))
		cursor.execute(query_stud)

		data = cursor.fetchall()
		mylist = []
		
		for row in data:
			mylist.append(' '.join(str(x) for x in row))

		print mylist

		query_group = ("SELECT GroupID FROM Groups"
			" WHERE Student1 = '%s' AND Student2 = '%s' AND Student3 = '%s' AND Student4 = '%s'" %(mylist[0],mylist[1],mylist[2],mylist[3]))
		cursor.execute(query_group)

		check_data = cursor.fetchall()
		list_id = []
		for row in check_data:
			list_id.append(' '.join(str(x) for x in row))

		print list_id

		if not list_id:
			print mylist[0]
			_query = (" INSERT INTO Groups( Student1, Student2, Student3, Student4) VALUES ( %(st1)s, %(st2)s, %(st3)s, %(st4)s ) ")
			data_query = {
			'st1' : mylist[0],
			'st2' : mylist[1],
			'st3' : mylist[2],
			'st4' : mylist[3]
			}
			print mylist[2]
			cursor.execute(_query, data_query)
			cnx.commit()
			print mylist[1]

			get_id = ("SELECT GroupID FROM Groups"
				"WHERE (Student1 = '%s' AND Student2 = '%s' AND Student3 = '%s' AND Student4 = '%s')`2" %(mylist[0],mylist[1],mylist[2],mylist[3]))
			cursor.execute(get_id)

			data_id = cursor.fetchall()

			id_list = []
			for row in data:
				id_list.append(' '.join(str(x) for x in row))

			print id_list

			query_visit = ("INSERT INTO Visit(GroupID, CollegeID) VALUES (%(idg)s, %(idc)s)")
			data_visit = {
			'idg' : id_list[0],
			'idc' : col_id_list[0]
			}
			cursor.execute(query_visit,data_visit)
			cnx.commit()

		else:
			query_visit = ("INSERT INTO Visit(GroupID, CollegeID) VALUES (%(idg)s, %(idc)s)")
			data_visit = {
			'idg' : list_id[0],
			'idc' : col_id_list[0]
			}
			cursor.execute(query_visit,data_visit)
			cnx.commit()



		cursor.close()
		cnx.close()	

		return render_template('add_num.html')

@app.route('/welcome')
def welcome():
	return render_template('welcome.html')

@app.route('/login', methods =['POST', 'GET'])
def login():
	error = None 
	if request.method == 'POST':
		if request.form['username'] != 'admin' or request.form['password'] != 'admin' :
			error = 'Invalid Credentials'
		else:
			session['logged_in'] = True
			flash('logged in')
			return redirect(url_for('index'))
	return render_template('login.html', error = error)

@app.route('/logout')
@login_required
def logout():
	session.pop('logged_in', None)
	return redirect(url_for('welcome'))

if __name__=="__main__":
	app.run()

# @app.route("/group", methods = ['POST', 'GET'])
# def group():
	
# 	cnx = mysql.connector.connect(user='root', password='gomya', database ='Petrol')
# 	cursor = cnx.cursor(buffered = True)
# 	if request.method == 'POST':	
# 		stud1 = request.form.get('student1')
# 		stud2 = request.form.get('student2')
# 		stud3 = request.form.get('student3')
# 		stud4 = request.form.get('student4')

# 		query = (" SELECT StudentID FROM Students "
# 			" WHERE Name = '%s' OR Name = '%s' OR Name = '%s' OR Name = '%s'" %(stud1,stud2,stud3,stud4))
# 		cursor.execute(query)
	
# 		data = cursor.fetchall()
# 		mylist = []
		

# 		for row in data:
# 			mylist.append(' '.join(str(x) for x in row))

		
# 		_query = (" INSERT INTO Groups( Student1, Student2, Student3, Student4) VALUES ( %(st1)s, %(st2)s, %(st3)s, %(st4)s ) ")
# 		data_query = {
# 		'st1' : mylist[0],
# 		'st2' : mylist[1],
# 		'st3' : mylist[2],
# 		'st4' : mylist[3]
# 		}
# 		cursor.execute(_query, data_query)
# 		cnx.commit()
# 		cursor.close()
# 		cnx.close()
# 		return render_template('add_num.html')

# @app.route("/post_student", methods = ['POST', 'GET'])
# def post_student():
# 	cnx = mysql.connector.connect(user='root', password='gomya', database ='Petrol')
# 	cursor = cnx.cursor(buffered = True)
# 	# student_id = request.form['student_id']
# 	student_name = request.form['student_name']
# 	student_mobile = request.form['student_mobile']
# 	add_student = ("INSERT INTO Students (Name,Mob) "
# 		"VALUES ( %(stud_name)s, %(stud_mob)s)")
# 	data_student = {
# 	# 'stud_id' : student_id,
# 	'stud_name' : student_name,
# 	'stud_mob' : student_mobile}
# 	cursor.execute(add_student,data_student)
# 	cnx.commit()
# 	cursor.close()
# 	cnx.close()
# 	return redirect(url_for('index'))