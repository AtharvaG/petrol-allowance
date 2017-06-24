from flask import Flask
import mysql.connector
from flask import render_template
from flask import request, redirect, url_for
# from flask import jsonify
# from Flask import jsonify


app = Flask(__name__)

# cnx = mysql.connector.connect(user='root', password='gomya', database ='Petrol')
# cursor = cnx.cursor(buffered = True)

@app.route('/')
def index():
	return render_template('add.html')

@app.route("/post_college", methods = ['POST', 'GET'])
def post_college():
	# college_id = request.form['college_id']
	college_name = request.form['college_name']
	cnx = mysql.connector.connect(user='root', password='gomya', database ='Petrol')
	cursor = cnx.cursor(buffered = True)
	add_college = ("INSERT INTO Colleges (Name)"
	" VALUES( %(col_name)s)")
	data_college = {
	'col_name' : college_name}
	cursor.execute(add_college, data_college)
	# mydict = {}

	cnx.commit()
	cursor.close()
	cnx.close()
	return redirect(url_for('index'))

@app.route("/post_student", methods = ['POST', 'GET'])
def post_student():
	cnx = mysql.connector.connect(user='root', password='gomya', database ='Petrol')
	cursor = cnx.cursor(buffered = True)
	# student_id = request.form['student_id']
	student_name = request.form['student_name']
	student_mobile = request.form['student_mobile']
	add_student = ("INSERT INTO Students (Name,Mob) "
		"VALUES ( %(stud_name)s, %(stud_mob)s)")
	data_student = {
	# 'stud_id' : student_id,
	'stud_name' : student_name,
	'stud_mob' : student_mobile}
	cursor.execute(add_student,data_student)
	cnx.commit()
	cursor.close()
	cnx.close()
	return redirect(url_for('index'))

@app.route("/test", methods = ['POST', 'GET'])
def test():
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

@app.route("/temp", methods = ['POST', 'GET'])
def temp():
	cnx = mysql.connector.connect(user='root', password='gomya', database ='Petrol')
	cursor = cnx.cursor(buffered = True)
	col_name = request.form.get('Colleges')
	query = (" INSERT INTO Colleges(Name) VALUES (%(colleges_name)s) ") 
	query_data = {
	'colleges_name' : col_name
	}
	cursor.execute(query, query_data)
	cnx.commit()
	cursor.close()
	cnx.close()	

	return render_template(url_for('test'))

@app.route("/group", methods = ['POST', 'GET'])
def group():
	
	cnx = mysql.connector.connect(user='root', password='gomya', database ='Petrol')
	cursor = cnx.cursor(buffered = True)
	if request.method == 'POST':	
		stud1 = request.form.get('student1')
		stud2 = request.form.get('student2')
		stud3 = request.form.get('student3')
		stud4 = request.form.get('student4')

		query = (" SELECT StudentID FROM Students "
			" WHERE Name = '%s' OR Name = '%s' OR Name = '%s' OR Name = '%s'" %(stud1,stud2,stud3,stud4))
		cursor.execute(query)
	
		data = cursor.fetchall()
		# cursor.close()
		# cnx.close()
		# print data[0]

		mylist = []
		for row in data:
			mylist.append(' '.join(str(x) for x in row))

		# print mylist
		# stu1 = mylist[0]
		# stu2 = mylist[1]
		# stu3 = mylist[2]
		# stu4 = mylist[3]
	# cnx = mysql.connector.connect(user='root', password='gomya', database ='Petrol')
	# cursor = cnx.cursor(buffered = True)
	# if request.method == 'POST':

		_query = (" INSERT INTO Groups( Student1, Student2, Student3, Student4) VALUES ( %(st1)s, %(st2)s, %(st3)s, %(st4)s ) ")
		data_query = {
		'st1' : mylist[0],
		'st2' : mylist[1],
		'st3' : mylist[2],
		'st4' : mylist[3]
		}
		# print _query
		cursor.execute(_query, data_query)
		cnx.commit()
		cursor.close()
		cnx.close()
		return render_template('add_num.html')


	
# cursor.close()
# cnx.close()

if __name__=="__main__":
	app.run()
