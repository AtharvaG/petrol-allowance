from flask import Flask
import mysql.connector
from flask import render_template
from flask import request, redirect, url_for


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
	# 'col_id' : college_id,
	'col_name' : college_name}
	cursor.execute(add_college, data_college)
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
	
# cursor.close()
# cnx.close()

if __name__=="__main__":
	app.run()


